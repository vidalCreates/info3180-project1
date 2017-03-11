"""empty message

Revision ID: 69371321f5db
Revises: 9ec328e46405
Create Date: 2017-03-09 19:26:46.416000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '69371321f5db'
down_revision = '9ec328e46405'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user_profile', sa.Column('profile_image', sa.String(length=80), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user_profile', 'profile_image')
    # ### end Alembic commands ###