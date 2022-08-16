"""Add table for suggestions

Revision ID: 6796a4188bc9
Revises: bf86d558e629
Create Date: 2022-08-16 14:29:57.512925

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6796a4188bc9'
down_revision = 'bf86d558e629'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('meal_elements',
    sa.Column('id', sa.String(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('category', sa.String(), nullable=True),
    sa.Column('prep_notes', sa.String(), nullable=True),
    sa.Column('prep_time_m', sa.Integer(), nullable=True),
    sa.Column('cooking_notes', sa.String(), nullable=True),
    sa.Column('cooking_time_m', sa.Integer(), nullable=True),
    sa.Column('cooking_time_comments', sa.String(), nullable=True),
    sa.Column('periodicity_d', sa.Integer(), nullable=True),
    sa.Column('tags', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('suggestions',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('date', sa.Date(), nullable=True),
    sa.Column('duration', sa.Integer(), nullable=True),
    sa.Column('lunches', sa.String(), nullable=True),
    sa.Column('dinners', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('meals', schema=None) as batch_op:
        batch_op.add_column(sa.Column('elements', sa.String(), nullable=True))
        batch_op.add_column(sa.Column('cooking_time_comments', sa.String(), nullable=True))
        batch_op.add_column(sa.Column('tags', sa.String(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('meals', schema=None) as batch_op:
        batch_op.drop_column('tags')
        batch_op.drop_column('cooking_time_comments')
        batch_op.drop_column('elements')

    op.drop_table('suggestions')
    op.drop_table('meal_elements')
    # ### end Alembic commands ###
