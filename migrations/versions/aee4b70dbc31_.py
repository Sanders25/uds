"""empty message

Revision ID: aee4b70dbc31
Revises: 6b522d2fb577
Create Date: 2022-01-11 19:10:15.712365

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'aee4b70dbc31'
down_revision = '6b522d2fb577'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('testdeadline',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('subject', sa.String(length=50), nullable=False),
    sa.Column('edgroup', sa.String(length=10), nullable=False),
    sa.Column('deadline', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['id'], ['test.id'], name='fk_testdl_test_id'),
    sa.ForeignKeyConstraint(['subject'], ['test.subject'], name='fk_testdl_test_subj'),
    sa.PrimaryKeyConstraint('id', 'subject', 'edgroup')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('testdeadline')
    # ### end Alembic commands ###
