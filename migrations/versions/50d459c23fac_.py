"""empty message

Revision ID: 50d459c23fac
Revises: e9b2bf9420d2
Create Date: 2019-07-23 14:44:08.498299

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '50d459c23fac'
down_revision = 'e9b2bf9420d2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('is_likes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('post_id', sa.Integer(), nullable=True),
    sa.Column('is_liked', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['post_id'], ['users.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('likes')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('likes',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('post_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('is_liked', sa.BOOLEAN(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['post_id'], ['users.id'], name='likes_post_id_fkey'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name='likes_user_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='likes_pkey')
    )
    op.drop_table('is_likes')
    # ### end Alembic commands ###
