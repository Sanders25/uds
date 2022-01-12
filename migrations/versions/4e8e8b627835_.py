"""empty message

Revision ID: 4e8e8b627835
Revises: 9b4708efcdd9
Create Date: 2022-01-11 19:06:36.762017

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4e8e8b627835'
down_revision = '9b4708efcdd9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('labwork', sa.Column('subject1', sa.String(length=100), nullable=False))
    op.drop_constraint('labwork_subject_fkey', 'labwork', type_='foreignkey')
    op.create_foreign_key(None, 'labwork', 'subject', ['subject1'], ['name'])
    op.drop_column('labwork', 'subject')
    op.add_column('test', sa.Column('subject', sa.String(length=100), nullable=False))
    op.drop_constraint('test_subject1_fkey', 'test', type_='foreignkey')
    op.create_foreign_key(None, 'test', 'subject', ['subject'], ['name'])
    op.drop_column('test', 'subject1')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('test', sa.Column('subject1', sa.VARCHAR(length=100), autoincrement=False, nullable=False))
    op.drop_constraint(None, 'test', type_='foreignkey')
    op.create_foreign_key('test_subject1_fkey', 'test', 'subject', ['subject1'], ['name'])
    op.drop_column('test', 'subject')
    op.add_column('labwork', sa.Column('subject', sa.VARCHAR(length=50), autoincrement=False, nullable=False))
    op.drop_constraint(None, 'labwork', type_='foreignkey')
    op.create_foreign_key('labwork_subject_fkey', 'labwork', 'subject', ['subject'], ['name'])
    op.drop_column('labwork', 'subject1')
    # ### end Alembic commands ###
