"""empty message

Revision ID: 7b8a559714ad
Revises: dc11c8bc88c4
Create Date: 2019-07-22 19:45:26.957030

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7b8a559714ad'
down_revision = 'dc11c8bc88c4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('ingredients', sa.Column('quantity', sa.String(), nullable=True))
    op.add_column('recipes', sa.Column('date_created', sa.DateTime(), nullable=True))
    op.add_column('recipes', sa.Column('description', sa.String(), nullable=True))
    op.add_column('users', sa.Column('date_created', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'date_created')
    op.drop_column('recipes', 'description')
    op.drop_column('recipes', 'date_created')
    op.drop_column('ingredients', 'quantity')
    # ### end Alembic commands ###
