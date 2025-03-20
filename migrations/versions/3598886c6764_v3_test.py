"""v3 test

Revision ID: 3598886c6764
Revises: 
Create Date: 2025-03-13 12:00:06.993434

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3598886c6764'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('name', sa.String(length=255), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_column('name')

    # ### end Alembic commands ###
