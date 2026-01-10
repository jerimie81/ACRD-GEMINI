To integrate Alembic for migrations, follow these steps in the project root (ACRD-GEMINI/):

Add to requirements.txt:textalembic
sqlalchemy  # Required for Alembic with SQLite
Initialize Alembic (Run once via command line):textalembic init migrationsThis creates alembic.ini and migrations/ folder with env.py, script.py.mako, etc.
Configure alembic.ini:
Edit alembic.ini:text[alembic]
script_location = migrations
sqlalchemy.url = sqlite:///./db/acrd.db  # Adjust path if needed
Modify migrations/env.py for SQLAlchemy + SQLite:
Add imports and configure target_metadata:Pythonfrom sqlalchemy import MetaData, create_engine
import config  # Assuming config.DB_PATH

target_metadata = MetaData()

# Reflect existing tables into target_metadata
def run_migrations_offline():
    """Offline mode config."""
    url = config.get_section(config.config_ini_section)['sqlalchemy.url']
    context.configure(url=url, target_metadata=target_metadata, literal_binds=True)

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    """Online mode."""
    connectable = create_engine(config.get_section(config.config_ini_section)['sqlalchemy.url'])
    with connectable.connect() as connection:
        # Reflect current DB schema
        target_metadata.reflect(bind=connection)
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()

# ... (rest of env.py remains)Note: Since schema is raw SQLite, reflect existing tables for autogenerate. For full SQLAlchemy ORM, define models in a separate file (e.g., models.py) and import to env.py: from models import Base; target_metadata = Base.metadata.
Create Initial Migration (After init_db):textalembic revision --autogenerate -m "Initial schema"
alembic upgrade headThis generates a migration script in migrations/versions/ with up() and down() for the expanded schema.
Integrate into setup.py:
Add to setup.py:Pythonimport subprocess

def setup_migrations():
    try:
        subprocess.run(['alembic', 'upgrade', 'head'], check=True)
    except subprocess.CalledProcessError:
        print("Migration failed; check alembic config.")

# In main setup:
# ...
init_db()  # First create if not exists
setup_migrations()  # Then apply any pending
For Future Migrations:
Modify schema in code (e.g., add column via db_manager).
Run alembic revision --autogenerate -m "Add new field".
Edit generated script if needed.
Apply with alembic upgrade head.
