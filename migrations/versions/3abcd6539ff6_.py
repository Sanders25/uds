"""empty message

Revision ID: 3abcd6539ff6
Revises: 4904d1ea2f65
Create Date: 2022-01-11 19:57:44.884469

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3abcd6539ff6'
down_revision = '4904d1ea2f65'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_foreign_key(None, 'labworkpass', 'labwork', ['id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'labworkpass', type_='foreignkey')
    # ### end Alembic commands ###
