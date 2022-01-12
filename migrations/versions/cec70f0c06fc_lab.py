"""lab

Revision ID: cec70f0c06fc
Revises: 35b65f6be9c5
Create Date: 2022-01-11 18:39:48.816060

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cec70f0c06fc'
down_revision = '35b65f6be9c5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('labworkdeadline',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('subject', sa.String(), nullable=False),
    sa.Column('edgroupId', sa.Integer(), nullable=False),
    sa.Column('deadline', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['edgroupId'], ['edgroup.id'], ),
    sa.ForeignKeyConstraint(['id'], ['labwork.id'], ),
    sa.ForeignKeyConstraint(['subject'], ['labwork.subject'], ),
    sa.PrimaryKeyConstraint('id', 'subject', 'edgroupId')
    )
    op.create_table('labworkpass',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('subject', sa.String(length=50), nullable=False),
    sa.Column('studentid', sa.Integer(), nullable=False),
    sa.Column('mark', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['id'], ['labwork.id'], ),
    sa.ForeignKeyConstraint(['studentid'], ['student.id'], ),
    sa.ForeignKeyConstraint(['subject'], ['labwork.subject'], ),
    sa.PrimaryKeyConstraint('id', 'subject', 'studentid')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('labworkpass')
    op.drop_table('labworkdeadline')
    # ### end Alembic commands ###
