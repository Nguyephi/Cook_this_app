"""empty message

Revision ID: 87d8e929dc30
Revises: ff0ac38acf56
Create Date: 2019-07-15 10:52:05.010774

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '87d8e929dc30'
down_revision = 'ff0ac38acf56'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users', 'username',
               existing_type=sa.VARCHAR(length=80),
               nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users', 'username',
               existing_type=sa.VARCHAR(length=80),
               nullable=False)
    # ### end Alembic commands ###