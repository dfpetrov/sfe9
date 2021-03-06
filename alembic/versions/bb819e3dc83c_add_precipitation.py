"""add precipitation

Revision ID: bb819e3dc83c
Revises: 9e04dd1bc318
Create Date: 2020-04-03 12:36:26.295116

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bb819e3dc83c'
down_revision = '9e04dd1bc318'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('forecast', sa.Column('precipitation', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('forecast', 'precipitation')
    # ### end Alembic commands ###
