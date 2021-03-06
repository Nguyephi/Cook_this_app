"""empty message

Revision ID: dc11c8bc88c4
Revises: 12e51e0ebfbd
Create Date: 2019-07-19 23:21:55.959295

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dc11c8bc88c4'
down_revision = '12e51e0ebfbd'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('instructions', sa.Column('instruction', sa.String(), nullable=True))
    op.add_column('instructions', sa.Column('instruction_id', sa.Integer(), nullable=True))
    op.drop_column('instructions', 'instructions')
    op.drop_column('instructions', 'instructions_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('instructions', sa.Column('instructions_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.add_column('instructions', sa.Column('instructions', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.drop_column('instructions', 'instruction_id')
    op.drop_column('instructions', 'instruction')
    # ### end Alembic commands ###
