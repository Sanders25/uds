"""warn

Revision ID: 35b65f6be9c5
Revises: 8b9dded365fb
Create Date: 2022-01-11 18:35:28.411094

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '35b65f6be9c5'
down_revision = '8b9dded365fb'
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
