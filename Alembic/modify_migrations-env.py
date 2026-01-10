from sqlalchemy import MetaData, create_engine
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

# ... (rest of env.py remains)
