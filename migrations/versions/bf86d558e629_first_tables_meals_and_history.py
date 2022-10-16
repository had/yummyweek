"""First tables (meals and history)

Revision ID: bf86d558e629
Revises: 
Create Date: 2022-07-27 11:27:33.970618

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'bf86d558e629'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('meals',
                    sa.Column('id', sa.String(), nullable=False),
                    sa.Column('name', sa.String(), nullable=True),
                    sa.Column('prep_notes', sa.String(), nullable=True),
                    sa.Column('prep_time_m', sa.Integer(), nullable=True),
                    sa.Column('cooking_notes', sa.String(), nullable=True),
                    sa.Column('cooking_time_m', sa.Integer(), nullable=True),
                    sa.Column('meal_type', sa.Enum('lunch', 'dinner', 'both', 'batch_cooking', name='mealtype'),
                              nullable=True),
                    sa.Column('periodicity_d', sa.Integer(), nullable=True),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('meal_history',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('date', sa.Date(), nullable=True),
                    sa.Column('meal', sa.String(), nullable=True),
                    sa.ForeignKeyConstraint(['meal'], ['meals.id'], name="meal2mealhistory"),
                    sa.PrimaryKeyConstraint('id')
                    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('meal_history')
    op.drop_table('meals')
    # ### end Alembic commands ###
