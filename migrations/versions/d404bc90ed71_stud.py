"""stud

Revision ID: d404bc90ed71
Revises: a3b09cd90814
Create Date: 2022-01-11 17:57:46.727074

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd404bc90ed71'
down_revision = 'a3b09cd90814'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('student',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=True),
    sa.Column('grants', sa.Integer(), nullable=True),
    sa.Column('education', sa.String(length=50), nullable=True),
    sa.Column('edgroup', sa.String(length=10), nullable=True),
    sa.ForeignKeyConstraint(['edgroup'], ['edgroup.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('student')
    # ### end Alembic commands ###
