from pathlib import Path
import sys
from logging.config import fileConfig

from alembic import context
from sqlalchemy import create_engine, pool


# ---------------------------------------------------------------------
# Make the project root importable
# ---------------------------------------------------------------------
sys.path.append(str(Path(__file__).resolve().parents[1]))

# ---------------------------------------------------------------------
# Import application components
# ---------------------------------------------------------------------
from app.core.settings import get_settings
from app.database.session import Base
import app.models  # Registers all ORM models with Base.metadata

# ---------------------------------------------------------------------
# Alembic Configuration
# ---------------------------------------------------------------------
config = context.config
settings = get_settings()

# ---------------------------------------------------------------------
# Configure Python logging
# ---------------------------------------------------------------------
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# ---------------------------------------------------------------------
# Metadata for Alembic autogeneration
# ---------------------------------------------------------------------
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """
    Run migrations in 'offline' mode.

    This configures the context with just a database URL
    instead of an Engine. Calls to context.execute() emit
    the generated SQL directly.
    """
    context.configure(
        url=settings.DATABASE_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """
    Run migrations in 'online' mode.

    In this mode Alembic creates a SQLAlchemy Engine and
    associates a live database connection with the migration
    context.
    """
    connectable = create_engine(
        settings.DATABASE_URL,
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()