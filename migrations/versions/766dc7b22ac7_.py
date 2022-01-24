"""empty message

Revision ID: 766dc7b22ac7
Revises: 68259b4cacc0
Create Date: 2022-01-20 15:32:29.999285

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '766dc7b22ac7'
down_revision = '68259b4cacc0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('subject', sa.String(length=100), nullable=False))
    op.add_column('user', sa.Column('edgroup', sa.String(length=10), nullable=False))
    op.add_column('user', sa.Column('deadline', sa.DateTime(), nullable=True))
    op.create_foreign_key(None, 'user', 'edgroup', ['edgroup'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'user', type_='foreignkey')
    op.drop_column('user', 'deadline')
    op.drop_column('user', 'edgroup')
    op.drop_column('user', 'subject')
    # ### end Alembic commands ###