"""Add concept of 'committed' to suggestions

Revision ID: 45074da6d478
Revises: 7ba513f484ec
Create Date: 2022-08-30 10:39:33.336332

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '45074da6d478'
down_revision = '7ba513f484ec'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('ingredients',
    sa.Column('id', sa.String(), nullable=False),
    sa.Column('category', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('recipes',
    sa.Column('id', sa.String(), nullable=False),
    sa.Column('ingredients', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('suggestions', schema=None) as batch_op:
        batch_op.add_column(sa.Column('committed', sa.Boolean(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('suggestions', schema=None) as batch_op:
        batch_op.drop_column('committed')

    op.drop_table('recipes')
    op.drop_table('ingredients')
    # ### end Alembic commands ###
