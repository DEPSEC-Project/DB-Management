# pylint: disable=R0903
"""
Modèles SQLAlchemy pour l'application, compatibles avec Flask-SQLAlchemy.
Ces modèles sont conçus pour être utilisés dans une application Flask externe.
"""

import uuid

from sqlalchemy import (
    ForeignKey,
    func as sa_func
)
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash

from depsec_db.extensions import db

class Project(db.Model):
    """Modèle d'un projet."""
    __tablename__ = 'projects'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    """Clé étrangère vers l'id de la table User"""
    auteur_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    titre = db.Column(db.String, nullable=False)
    status = db.Column(db.String, nullable=False)
    path = db.Column(db.String, nullable=False)
    """Relation avec SBOM : suppression en cascade"""
    sboms = relationship("SBOM", backref="project", cascade="all, delete", passive_deletes=True)
    def to_dict(self):
        """Function to return projects as JSON"""
        return {
            "id": self.id,
            "auteur_id": self.auteur_id,
            "titre": self.titre,
            "status": self.status,
            "path": self.path
    }

class User(db.Model):
    """Modèle utilisateur principal pour l'authentification."""
    __tablename__ = 'users'

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    public_id = db.Column(
		db.String(36),
		unique=True,
		nullable=False,
		default=lambda: str(uuid.uuid4())
	)
    username = db.Column(db.String(255), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(255), nullable=True)
    name = db.Column(db.String(255), nullable=True)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)
    created_at = db.Column(
		db.DateTime(timezone=True),
		server_default=sa_func.now(), # pylint: disable=not-callable
		nullable=False
	)
    updated_at = db.Column(
		db.DateTime(timezone=True),
		server_default=sa_func.now(), # pylint: disable=not-callable
		onupdate=sa_func.now(), # pylint: disable=not-callable
		nullable=False
	)
    """Relation One-To-Many avec la table Project qui utilise l'id de User"""
    projects = db.relationship('Project', backref='user', lazy=True)
    def set_password(self, password: str) -> None:
        """Hash et définit le mot de passe de l'utilisateur."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        """Vérifie la correspondance du mot de passe fourni avec le haché."""
        return check_password_hash(self.password_hash, password)


class TokenBlacklist(db.Model):
    """Modèle pour stocker les JWT révoqués (blacklistés)."""
    __tablename__ = 'token_blacklist'

    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(36), unique=True, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=sa_func.now(), nullable=False) # pylint: disable=not-callable

    @classmethod
    def is_token_blacklisted(cls, jti: str, session=None) -> bool:
        """Vérifie si un token (via JTI) est blacklisté."""
        session = session or db.session
        return session.query(cls).filter_by(jti=jti).first() is not None


class TrivyReport(db.Model):
    """Modèle représentant un rapport d'analyse Trivy."""
    __tablename__ = 'trivy_reports'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    schema_version = db.Column(db.Integer, nullable=False)
    """Clé étrangère vers l'id de la table SBOM"""
    sbom_id = db.Column(db.Integer, db.ForeignKey('sboms.id'), nullable=False)
    created_at = db.Column(
        db.DateTime(timezone=True),
        server_default=sa_func.now(),  # pylint: disable=not-callable
        default=sa_func.now(),  # pylint: disable=not-callable
        nullable=False
    )

    artifact_name = db.Column(db.String, nullable=False)
    artifact_type = db.Column(db.String, nullable=False)
    report_metadata = db.Column(db.JSON, nullable=True)
    results = db.Column(db.JSON, nullable=True)


class SBOM(db.Model):
    """
    Modèle d'un SBOM.
    """
    __tablename__ = 'sboms'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    """Clé étrangère vers l'id du projet"""
    project_id = db.Column(db.Integer, ForeignKey('projects.id',ondelete="CASCADE"),nullable=False)
    sbom_data = db.Column(db.JSON, nullable=False)
    """Relation One-To-Many avec la table TrivyReport qui utilise l'id du SBOM"""
    projects = db.relationship('TrivyReport', backref='sboms', lazy=True)
