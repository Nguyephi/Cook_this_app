"""empty message

Revision ID: a11b2b9f869b
Revises: 7f5e7cf73353
Create Date: 2019-07-18 16:46:31.878996

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a11b2b9f869b'
down_revision = '7f5e7cf73353'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('recipes', sa.Column('instructions', sa.String(), nullable=True))
    op.drop_column('recipes', 'intructions')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('recipes', sa.Column('intructions', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.drop_column('recipes', 'instructions')
    # ### end Alembic commands ###
