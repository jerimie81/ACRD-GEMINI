from __future__ import annotations

from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class DeviceProfile(Base):
    __tablename__ = "device_profiles"

    id = Column(Integer, primary_key=True)
    model = Column(String(255), unique=True, nullable=False)
    brand = Column(String(255))
    serial = Column(String(255))
    os_version = Column(String(64))
    firmware = Column(String(255))
    security_patch = Column(String(64))
    boot_mode = Column(String(64))
    last_quarried = Column(DateTime, default=datetime.utcnow)


class Method(Base):
    __tablename__ = "methods"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), unique=True, nullable=False)
    description = Column(Text)
    pros = Column(Text)
    cons = Column(Text)
    compatibility = Column(String(255))
    requirements = Column(Text)


class ToolConfig(Base):
    __tablename__ = "tool_configs"

    id = Column(Integer, primary_key=True)
    tool_name = Column(String(255), unique=True, nullable=False)
    path = Column(String(255))
    version = Column(String(64))
    source_url = Column(String(255))


class Log(Base):
    __tablename__ = "logs"

    id = Column(Integer, primary_key=True)
    model = Column(String(255))
    operation = Column(String(255))
    log_data = Column(Text)
    status = Column(String(64))
    timestamp = Column(DateTime, default=datetime.utcnow)


class UrlPlaceholder(Base):
    __tablename__ = "url_placeholders"

    id = Column(Integer, primary_key=True)
    model = Column(String(255), ForeignKey("device_profiles.model"), nullable=False)
    component = Column(String(255), nullable=False)
    url = Column(Text)
    type = Column(String(64), nullable=False)
    checksum = Column(String(255))
    verified = Column(Boolean, default=False)


class AiTailoredOption(Base):
    __tablename__ = "ai_tailored_options"

    id = Column(Integer, primary_key=True)
    model = Column(String(255), ForeignKey("device_profiles.model"), nullable=False)
    option = Column(String(255))
    tailored_data = Column(Text)


class DbMetadata(Base):
    __tablename__ = "db_metadata"

    id = Column(Integer, primary_key=True)
    key = Column(String(255), unique=True, nullable=False)
    value = Column(String(255))
