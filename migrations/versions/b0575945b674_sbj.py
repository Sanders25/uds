"""sbj

Revision ID: b0575945b674
Revises: 48c00b553329
Create Date: 2022-01-11 17:51:53.853958

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b0575945b674'
down_revision = '48c00b553329'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('subject',
    sa.Column('name', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('name')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('subject')
    # ### end Alembic commands ###
