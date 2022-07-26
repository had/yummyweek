"""rework ingredients

Revision ID: 80a074f2c92a
Revises: 332152892216
Create Date: 2022-11-06 18:01:21.590616

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '80a074f2c92a'
down_revision = '332152892216'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('recipes')
    op.drop_table('ingredients')
    op.create_table('ingredients',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('name', sa.String(), unique=True, nullable=True),
                    sa.Column('category', sa.String(), nullable=True),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('dish_ingredients',
                    sa.Column('dish_id', sa.String(), nullable=False),
                    sa.Column('ingredient_id', sa.Integer(), nullable=False),
                    sa.Column('quantity', sa.String(), nullable=True),
                    sa.Column('unit', sa.String(), nullable=True),
                    sa.ForeignKeyConstraint(['dish_id'], ['dishes.id'], ),
                    sa.ForeignKeyConstraint(['ingredient_id'], ['ingredients.id'], ),
                    sa.PrimaryKeyConstraint('dish_id', 'ingredient_id')
                    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###

    op.drop_table('ingredients')
    op.create_table('ingredients',
                    sa.Column('id', sa.String(), nullable=False),
                    sa.Column('category', sa.String(), nullable=True),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('recipes',
                    sa.Column('id', sa.VARCHAR(), nullable=False),
                    sa.Column('ingredients', sa.VARCHAR(), nullable=True),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.drop_table('dish_ingredients')
    # ### end Alembic commands ###
