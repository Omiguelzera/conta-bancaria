import sys
import os
from logging.config import fileConfig

from sqlalchemy import create_engine
from sqlalchemy import pool
from alembic import context

# Adicione o caminho para o seu projeto
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'app')))

# Importar os modelos e a base do seu projeto
from app.models.base import Base  # Altere o caminho conforme a estrutura do seu projeto

# Configurações do arquivo ini
config = context.config

# Configuração do logging (geralmente é configurada no alembic.ini)
fileConfig(config.config_file_name)

# Adicionando o metadata dos modelos
target_metadata = Base.metadata

def run_migrations_offline():
    """Executa migrações em modo offline"""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(url=url, target_metadata=target_metadata, literal_binds=True)

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    """Executa migrações em modo online"""
    # Cria uma engine para o banco de dados
    connectable = create_engine(config.get_main_option("sqlalchemy.url"), poolclass=pool.NullPool)

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
