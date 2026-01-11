# modules/db_manager.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from contextlib import contextmanager
import config
from .exceptions import DatabaseError
from db.models import Base, DeviceProfile, Method, ToolConfig, Log, UrlPlaceholder, AiTailoredOption, DbMetadata
import datetime
import logging

logger = logging.getLogger("ACRD")

engine = create_engine(f'sqlite:///{config.DB_PATH}')
Session = sessionmaker(bind=engine)

def reset_engine():
    """Reset the database engine (useful for testing)."""
    global engine, Session
    engine = create_engine(f'sqlite:///{config.DB_PATH}')
    Session = sessionmaker(bind=engine)

@contextmanager
def get_session():
    """Provide a transactional scope around a series of operations."""
    session = Session()
    try:
        yield session
        session.commit()
    except SQLAlchemyError as e:
        session.rollback()
        raise DatabaseError(f"Database operation failed: {e}")
    finally:
        session.close()

def init_db():
    """Initialize the database with the defined schema."""
    try:
        Base.metadata.create_all(engine)
        with get_session() as session:
            # Set initial schema version
            schema_version = session.query(DbMetadata).filter_by(key='schema_version').first()
            if not schema_version:
                session.add(DbMetadata(key='schema_version', value='1'))

            # Sample data insertion
            methods = [
                {
                    'name': 'Magisk',
                    'description': 'Systemless root via boot image patching; installs as an app/module system.',
                    'pros': 'Stable, large module ecosystem, handles dm-verity automatically.',
                    'cons': 'Requires bootloader unlock; hiding needs extra modules.',
                    'compatibility': 'Android 14-16; 90%+ success on most devices.',
                    'requirements': '{"bootloader_unlock": true, "tools": ["adb", "fastboot"]}'
                },
                {
                    'name': 'KernelSU',
                    'description': 'Kernel-based root integrating directly into the device kernel.',
                    'pros': 'Better at bypassing detection (Play Integrity); no fingerprint spoofing needed.',
                    'cons': 'Requires GKI kernels (5.10+); manual superuser setup.',
                    'compatibility': 'Android 14+ on GKI devices; 80% success.',
                    'requirements': '{"bootloader_unlock": true, "tools": ["adb", "fastboot"]}'
                },
                {
                    'name': 'APatch',
                    'description': 'Hybrid kernel patching tool focusing on systemless modifications.',
                    'pros': 'Flexible for complex setups; good for evading detections.',
                    'cons': 'Less mainstream; stability varies; requires precise kernel matching.',
                    'compatibility': 'Android 14-16; 75% success.',
                    'requirements': '{"bootloader_unlock": true, "tools": ["adb", "fastboot"]}'
                },
                {
                    'name': 'Kitsune Mask',
                    'description': 'Enhanced Magisk fork with improved hiding features.',
                    'pros': 'Better root hiding than vanilla Magisk; maintains Magisk ecosystem.',
                    'cons': 'Smaller community than original Magisk.',
                    'compatibility': 'Android 14+; 85% success.',
                    'requirements': '{"bootloader_unlock": true, "tools": ["adb", "fastboot"]}'
                },
                {
                    'name': 'Samsung-Specific',
                    'description': 'Magisk patching adapted for Samsung via Odin tool.',
                    'pros': 'Tailored for Samsung ecosystem; avoids fastboot limitations.',
                    'cons': 'Trips Knox (permanent); requires exact ROM match.',
                    'compatibility': 'Android 14+ on Samsung; 70% success.',
                    'requirements': '{"bootloader_unlock": true, "tools": ["odin"]}'
                }
            ]

            for m_data in methods:
                method = session.query(Method).filter_by(name=m_data['name']).first()
                if method:
                    # Update existing method
                    for key, value in m_data.items():
                        setattr(method, key, value)
                else:
                    # Add new method
                    session.add(Method(**m_data))
    except SQLAlchemyError as e:
        raise DatabaseError(f"Database initialization failed: {e}")


def add_tool_config(tool_name, path, version, source_url):
    """Adds or updates a tool configuration in the database."""
    with get_session() as session:
        tool = session.query(ToolConfig).filter_by(tool_name=tool_name).first()
        if tool:
            tool.path = path
            tool.version = version
            tool.source_url = source_url
        else:
            session.add(ToolConfig(tool_name=tool_name, path=path, version=version, source_url=source_url))

def insert_device_profile(info: dict):
    """Insert or update a device profile."""
    with get_session() as session:
        device = session.query(DeviceProfile).filter_by(model=info.get('model')).first()
        if device:
            device.brand = info.get('brand')
            device.serial = info.get('serial')
            device.os_version = info.get('os_version')
            device.firmware = info.get('firmware')
            device.security_patch = info.get('security_patch')
            device.boot_mode = info.get('boot_mode')
            device.last_quarried = datetime.datetime.utcnow()
        else:
            # Filter info to only include keys that are in the model
            valid_keys = [c.name for c in DeviceProfile.__table__.columns]
            filtered_info = {k: v for k, v in info.items() if k in valid_keys}
            session.add(DeviceProfile(**filtered_info))

def query_methods(os_version):
    """Query root methods by compatibility."""
    with get_session() as session:
        methods = session.query(Method).filter(Method.compatibility.like(f'%{os_version}%')).all()
        return [
            {
                'name': m.name,
                'description': m.description,
                'pros': m.pros,
                'cons': m.cons,
                'compatibility': m.compatibility,
                'requirements': m.requirements
            } for m in methods
        ]

def store_urls(model, structure):
    """Store URLs/placeholders for a model."""
    with get_session() as session:
        for comp, urls in structure.items():
            for typ, url in urls.items():
                session.add(UrlPlaceholder(model=model, component=comp, url=url, type=typ))

def get_url(model, component, type):
    """Gets a URL for a specific component and type."""
    with get_session() as session:
        url_obj = session.query(UrlPlaceholder).filter_by(model=model, component=component, type=type).first()
        if url_obj:
            # Convert to dict to avoid DetachedInstanceError
            return {
                'url': url_obj.url,
                'checksum': url_obj.checksum,
                'verified': url_obj.verified,
                'component': url_obj.component,
                'type': url_obj.type
            }
        return None

def set_url_verified(model, component, type, verified=True):
    """Updates the verified status of a URL."""
    with get_session() as session:
        url = session.query(UrlPlaceholder).filter_by(model=model, component=component, type=type).first()
        if url:
            url.verified = verified

def store_tailored_options(model, option, tailored_data):
    """Stores AI-tailored options in the database."""
    with get_session() as session:
        session.add(AiTailoredOption(model=model, option=option, tailored_data=tailored_data))

def log_operation(model, operation, log_data, status):
    """Log an operation."""
    logger.info(f"Operation: {operation} | Model: {model} | Status: {status} | Data: {log_data}")
    with get_session() as session:
        session.add(Log(model=model, operation=operation, log_data=log_data, status=status))

def get_schema_version():
    """Get current schema version."""
    with get_session() as session:
        meta = session.query(DbMetadata).filter_by(key='schema_version').first()
        return int(meta.value) if meta else 0

def prune_logs(days=30):
    """Prunes logs older than a certain number of days."""
    with get_session() as session:
        limit = datetime.datetime.utcnow() - datetime.timedelta(days=days)
        session.query(Log).filter(Log.timestamp < limit).delete()
        session.execute("VACUUM")