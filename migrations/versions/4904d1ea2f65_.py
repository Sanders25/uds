"""empty message

Revision ID: 4904d1ea2f65
Revises: 44572a8ef0f9
Create Date: 2022-01-11 19:57:35.007523

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4904d1ea2f65'
down_revision = '44572a8ef0f9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_foreign_key(None, 'labworkpass', 'labwork', ['subject'], ['subject'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'labworkpass', type_='foreignkey')
    # ### end Alembic commands ###
