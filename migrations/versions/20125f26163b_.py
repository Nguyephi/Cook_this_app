"""empty message

Revision ID: 20125f26163b
Revises: 54f04443a754
Create Date: 2019-07-26 15:00:11.741643

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '20125f26163b'
down_revision = '54f04443a754'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('subscribe', sa.Column('subscriber', sa.Integer(), nullable=False))
    op.drop_constraint('subscribe_user_subscribing_fkey', 'subscribe', type_='foreignkey')
    op.create_foreign_key(None, 'subscribe', 'users', ['subscriber'], ['id'])
    op.drop_column('subscribe', 'user_subscribing')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('subscribe', sa.Column('user_subscribing', sa.INTEGER(), autoincrement=False, nullable=False))
    op.drop_constraint(None, 'subscribe', type_='foreignkey')
    op.create_foreign_key('subscribe_user_subscribing_fkey', 'subscribe', 'users', ['user_subscribing'], ['id'])
    op.drop_column('subscribe', 'subscriber')
    # ### end Alembic commands ###