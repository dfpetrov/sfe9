"""users

Revision ID: 26c0dc2d655a
Revises: ebb7cbc02195
Create Date: 2020-04-06 21:38:28.880396

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '26c0dc2d655a'
down_revision = 'ebb7cbc02195'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('email', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('password', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('authenticated', sa.BOOLEAN(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('email', name='user_pkey')
    )
    # ### end Alembic commands ###