import subprocess

def setup_migrations():
    try:
        subprocess.run(['alembic', 'upgrade', 'head'], check=True)
    except subprocess.CalledProcessError:
        print("Migration failed; check alembic config.")

# In main setup:
# ...
init_db()  # First create if not exists
setup_migrations()  # Then apply any pending
