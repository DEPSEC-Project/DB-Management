import logging
import os
from logging.config import fileConfig

from alembic import context
from flask import current_app

# Ceci est l'objet de configuration Alembic, qui permet d'accéder aux valeurs dans le fichier .ini.
config = context.config

# Récupération de l'URL de la base de données depuis les variables d'environnement
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://dev_user:motdepassetest@localhost:5433/dev_db")

# Interprète le fichier de configuration pour la gestion des logs.
fileConfig(config.config_file_name)
logger = logging.getLogger('alembic.env')


def get_engine():
    """Retourne l'objet Engine pour la base de données."""
    try:
        # Fonction pour Flask-SQLAlchemy<3 et Alchemical
        return current_app.extensions['migrate'].db.get_engine()
    except (TypeError, AttributeError):
        # Fonction pour Flask-SQLAlchemy>=3
        return current_app.extensions['migrate'].db.engine


def get_engine_url():
    """Retourne l'URL de la base de données, en utilisant la variable d'environnement appropriée."""
    try:
        return DATABASE_URL.replace('%', '%%')
    except AttributeError:
        return str(DATABASE_URL).replace('%', '%%')


# Ajoutez ici l'objet Metadata de votre modèle pour que 'autogenerate' fonctionne
# Exemple: from myapp import mymodel
# target_metadata = mymodel.Base.metadata
config.set_main_option('sqlalchemy.url', get_engine_url())
target_db = current_app.extensions['migrate'].db


def get_metadata():
    """Retourne la metadata du modèle."""
    if hasattr(target_db, 'metadatas'):
        return target_db.metadatas[None]
    return target_db.metadata


def run_migrations_offline():
    """Exécute les migrations en mode 'offline'."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url, target_metadata=get_metadata(), literal_binds=True
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Exécute les migrations en mode 'online'."""
    
    # Callback pour empêcher la génération automatique de migration quand il n'y a pas de changement
    def process_revision_directives(context, revision, directives):
        if getattr(config.cmd_opts, 'autogenerate', False):
            script = directives[0]
            if script.upgrade_ops.is_empty():
                directives[:] = []
                logger.info('Aucun changement de schéma détecté.')

    conf_args = current_app.extensions['migrate'].configure_args
    if conf_args.get("process_revision_directives") is None:
        conf_args["process_revision_directives"] = process_revision_directives

    connectable = get_engine()

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=get_metadata(),
            **conf_args
        )

        with context.begin_transaction():
            context.run_migrations()


# Exécute les migrations en mode 'offline' ou 'online' en fonction du mode
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
