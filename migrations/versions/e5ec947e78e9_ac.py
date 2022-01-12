"""ac

Revision ID: e5ec947e78e9
Revises: b0575945b674
Create Date: 2022-01-11 17:52:43.595736

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e5ec947e78e9'
down_revision = 'b0575945b674'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('assignedclass',
    sa.Column('edgroup', sa.Integer(), nullable=False),
    sa.Column('subject', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['edgroup'], ['edgroup.id'], ),
    sa.ForeignKeyConstraint(['subject'], ['subject.name'], ),
    sa.PrimaryKeyConstraint('edgroup', 'subject')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('assignedclass')
    # ### end Alembic commands ###
