"""test

Revision ID: 6b53a099248e
Revises: 
Create Date: 2025-04-02 19:40:19.927384

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '6b53a099248e'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('sbom')
    op.drop_table('project')
    with op.batch_alter_table('trivy_reports', schema=None) as batch_op:
        batch_op.add_column(sa.Column('sbom_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key(None, 'sboms', ['sbom_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('trivy_reports', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('sbom_id')

    op.create_table('project',
    sa.Column('id', sa.INTEGER(), server_default=sa.text("nextval('project_id_seq'::regclass)"), autoincrement=True, nullable=False),
    sa.Column('name', sa.VARCHAR(length=255), autoincrement=False, nullable=False),
    sa.Column('version', sa.VARCHAR(length=50), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='project_pkey'),
    postgresql_ignore_search_path=False
    )
    op.create_table('sbom',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('project_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('sbom_data', postgresql.JSON(astext_type=sa.Text()), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['project_id'], ['project.id'], name='sbom_project_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='sbom_pkey')
    )
    # ### end Alembic commands ###
