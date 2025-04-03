# pylint: disable=R0903
"""
Modèles SQLAlchemy pour l'application, compatibles avec Flask-SQLAlchemy.
Ces modèles sont conçus pour être utilisés dans une application Flask externe.
"""

import uuid  # ✅ 1️⃣ Import standard Python

# ✅ 2️⃣ Imports externes (librairies installées)
from sqlalchemy import (
    Column, Integer, String, ForeignKey, JSON, DateTime, Boolean
)
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import func as sa_func

# ✅ 3️⃣ Imports internes (modules du projet)
from depsec_db.extensions import db


class Project(db.Model):
    """Modèle d'un projet."""
    __tablename__ = 'projects'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    auteur_id = Column(Integer, ForeignKey('users.id'), nullable=False)  # Clé étrangère vers User
    titre = Column(String, nullable=False)
    status = Column(String, nullable=False)
    path = Column(String, nullable=False)

    """Relation avec SBOM : suppression en cascade"""
    sboms = relationship(
        "SBOM", backref="project", cascade="all, delete", passive_deletes=True
    )

    def to_dict(self):
        """Retourne un dictionnaire représentant le projet."""
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

    id = Column(Integer, primary_key=True, autoincrement=True)
    public_id = Column(
        String(36), unique=True, nullable=False, default=lambda: str(uuid.uuid4())
    )
    username = Column(String(255), unique=True, nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=True)
    is_admin = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime(timezone=True), server_default=sa_func.now(), nullable=False)
    updated_at = Column(
        DateTime(timezone=True),
        server_default=sa_func.now(),
        onupdate=sa_func.now(),
        nullable=False
    )

    """Relation One-To-Many avec Project (un user peut avoir plusieurs projets)"""
    projects = relationship('Project', backref='user', lazy=True)

    def set_password(self, password: str) -> None:
        """Hash et définit le mot de passe de l'utilisateur."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        """Vérifie la correspondance du mot de passe fourni avec le haché."""
        return check_password_hash(self.password_hash, password)


class TokenBlacklist(db.Model):
    """Modèle pour stocker les JWT révoqués."""
    __tablename__ = 'token_blacklist'

    id = Column(Integer, primary_key=True)
    jti = Column(String(36), unique=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=sa_func.now(), nullable=False)

    @classmethod
    def is_token_blacklisted(cls, jti: str, session=None) -> bool:
        """Vérifie si un token (via JTI) est blacklisté."""
        session = session or db.session
        return session.query(cls).filter_by(jti=jti).first() is not None


class TrivyReport(db.Model):
    """Modèle représentant un rapport d'analyse Trivy."""
    __tablename__ = 'trivy_reports'

    id = Column(Integer, primary_key=True, autoincrement=True)
    schema_version = Column(Integer, nullable=False)
    
    """Clé étrangère vers SBOM"""
    sbom_id = Column(Integer, ForeignKey('sboms.id'), nullable=False)
    
    created_at = Column(
        DateTime(timezone=True),
        server_default=sa_func.now(),
        default=sa_func.now(),
        nullable=False
    )

    artifact_name = Column(String, nullable=False)
    artifact_type = Column(String, nullable=False)
    report_metadata = Column(JSON, nullable=True)
    results = Column(JSON, nullable=True)


class SBOM(db.Model):
    """Modèle d'un SBOM."""
    __tablename__ = 'sboms'

    id = Column(Integer, primary_key=True, autoincrement=True)
    
    """Clé étrangère vers Project avec suppression en cascade"""
    project_id = Column(Integer, ForeignKey('projects.id', ondelete="CASCADE"), nullable=False)
    
    sbom_data = Column(JSON, nullable=False)

    """Relation One-To-Many avec TrivyReport"""
    trivy_reports = relationship('TrivyReport', backref='sbom', lazy=True)
