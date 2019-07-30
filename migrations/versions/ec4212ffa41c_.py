"""empty message

Revision ID: ec4212ffa41c
Revises: 7b8a559714ad
Create Date: 2019-07-23 10:40:15.287227

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ec4212ffa41c'
down_revision = '7b8a559714ad'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('recipes', 'description',
               existing_type=sa.VARCHAR(),
               type_=sa.String(length=500),
               existing_nullable=True)
    op.alter_column('recipes', 'title',
               existing_type=sa.VARCHAR(length=500),
               type_=sa.String(length=255),
               existing_nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('recipes', 'title',
               existing_type=sa.String(length=255),
               type_=sa.VARCHAR(length=500),
               existing_nullable=True)
    op.alter_column('recipes', 'description',
               existing_type=sa.String(length=500),
               type_=sa.VARCHAR(),
               existing_nullable=True)
    # ### end Alembic commands ###
