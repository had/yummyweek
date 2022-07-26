"""Adding user table

Revision ID: 36a43524dcdf
Revises: 45074da6d478
Create Date: 2022-09-30 07:48:43.637845

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '36a43524dcdf'
down_revision = '45074da6d478'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('email', sa.String(length=64), nullable=True),
                    sa.Column('username', sa.String(length=64), nullable=True),
                    sa.Column('password_hash', sa.String(length=128), nullable=True),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_index(op.f('ix_users_username'), 'users', ['username'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_users_username'), table_name='users')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')
    # ### end Alembic commands ###
