"""empty message

Revision ID: de71d9bdc2b3
Revises: 30b79b2b4439
Create Date: 2022-01-19 20:05:57.413218

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'de71d9bdc2b3'
down_revision = '30b79b2b4439'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('labworkdeadline',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('subject', sa.String(length=100), nullable=False),
    sa.Column('edgroupId', sa.String(length=10), nullable=False),
    sa.Column('deadline', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['edgroupId'], ['edgroup.id'], ),
    sa.ForeignKeyConstraint(['id', 'subject'], ['labwork.id', 'labwork.subject'], ),
    sa.PrimaryKeyConstraint('id', 'subject', 'edgroupId')
    )
    op.create_table('labworkpass',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('subject', sa.String(length=50), nullable=False),
    sa.Column('studentid', sa.Integer(), nullable=False),
    sa.Column('mark', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['id', 'subject'], ['labwork.id', 'labwork.subject'], ),
    sa.ForeignKeyConstraint(['studentid'], ['student.id'], ),
    sa.PrimaryKeyConstraint('id', 'subject', 'studentid')
    )
    op.create_table('testpass',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('studentid', sa.Integer(), nullable=False),
    sa.Column('subject', sa.String(length=50), nullable=False),
    sa.ForeignKeyConstraint(['id', 'subject'], ['test.id', 'test.subject'], ),
    sa.ForeignKeyConstraint(['studentid'], ['student.id'], ),
    sa.PrimaryKeyConstraint('id', 'studentid', 'subject')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('testpass')
    op.drop_table('labworkpass')
    op.drop_table('labworkdeadline')
    # ### end Alembic commands ###