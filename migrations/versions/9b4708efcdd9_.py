"""empty message

Revision ID: 9b4708efcdd9
Revises: 0229d5a985ff
Create Date: 2022-01-11 19:05:21.065319

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9b4708efcdd9'
down_revision = '0229d5a985ff'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('test', sa.Column('subject1', sa.String(length=100), nullable=False))
    op.drop_constraint('test_subject_fkey', 'test', type_='foreignkey')
    op.create_foreign_key(None, 'test', 'subject', ['subject1'], ['name'])
    op.drop_column('test', 'subject')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('test', sa.Column('subject', sa.VARCHAR(length=100), autoincrement=False, nullable=False))
    op.drop_constraint(None, 'test', type_='foreignkey')
    op.create_foreign_key('test_subject_fkey', 'test', 'subject', ['subject'], ['name'])
    op.drop_column('test', 'subject1')
    # ### end Alembic commands ###
