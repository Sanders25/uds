"""empty message

Revision ID: 7bfc519c28de
Revises: de2614eb7fa1
Create Date: 2022-01-26 16:40:13.347738

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7bfc519c28de'
down_revision = 'de2614eb7fa1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('faculty',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_faculty_name'), 'faculty', ['name'], unique=True)
    op.create_table('user',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('login', sa.String(length=50), nullable=True),
    sa.Column('hash', sa.String(length=256), nullable=True),
    sa.Column('role', sa.String(length=50), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('hash'),
    sa.UniqueConstraint('login')
    )
    op.create_table('edgroup',
    sa.Column('id', sa.String(length=10), nullable=False),
    sa.Column('course', sa.Integer(), nullable=True),
    sa.Column('faculty', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['faculty'], ['faculty.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('staff',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=True),
    sa.Column('faculty', sa.Integer(), nullable=True),
    sa.Column('userId', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['faculty'], ['faculty.id'], ),
    sa.ForeignKeyConstraint(['userId'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('student',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=True),
    sa.Column('grants', sa.Integer(), nullable=True),
    sa.Column('education', sa.String(length=50), nullable=True),
    sa.Column('edgroup', sa.String(length=10), nullable=True),
    sa.Column('userId', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['edgroup'], ['edgroup.id'], ),
    sa.ForeignKeyConstraint(['userId'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('subject',
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('staffId', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['staffId'], ['staff.id'], ),
    sa.PrimaryKeyConstraint('name')
    )
    op.create_table('assignedclass',
    sa.Column('edgroup', sa.String(length=10), nullable=False),
    sa.Column('subject', sa.String(length=100), nullable=False),
    sa.ForeignKeyConstraint(['edgroup'], ['edgroup.id'], ),
    sa.ForeignKeyConstraint(['subject'], ['subject.name'], ),
    sa.PrimaryKeyConstraint('edgroup', 'subject')
    )
    op.create_table('labwork',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('subject', sa.String(length=100), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=True),
    sa.ForeignKeyConstraint(['subject'], ['subject.name'], ),
    sa.PrimaryKeyConstraint('id', 'subject')
    )
    op.create_table('test',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('subject', sa.String(length=100), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=True),
    sa.ForeignKeyConstraint(['subject'], ['subject.name'], ),
    sa.PrimaryKeyConstraint('id', 'subject')
    )
    op.create_table('labworkdeadline',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('subject', sa.String(length=100), nullable=False),
    sa.Column('edgroup', sa.String(length=10), nullable=False),
    sa.Column('deadline', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['edgroup'], ['edgroup.id'], ),
    sa.ForeignKeyConstraint(['id', 'subject'], ['labwork.id', 'labwork.subject'], ),
    sa.PrimaryKeyConstraint('id', 'subject', 'edgroup')
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
    op.create_table('testdeadline',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('subject', sa.String(length=50), nullable=False),
    sa.Column('edgroup', sa.String(length=10), nullable=False),
    sa.Column('deadline', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['edgroup'], ['edgroup.id'], ),
    sa.ForeignKeyConstraint(['id', 'subject'], ['test.id', 'test.subject'], ),
    sa.PrimaryKeyConstraint('id', 'subject', 'edgroup')
    )
    op.create_table('testpass',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('studentid', sa.Integer(), nullable=False),
    sa.Column('subject', sa.String(length=50), nullable=False),
    sa.Column('mark', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['id', 'subject'], ['test.id', 'test.subject'], ),
    sa.ForeignKeyConstraint(['studentid'], ['student.id'], ),
    sa.PrimaryKeyConstraint('id', 'studentid', 'subject')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('testpass')
    op.drop_table('testdeadline')
    op.drop_table('labworkpass')
    op.drop_table('labworkdeadline')
    op.drop_table('test')
    op.drop_table('labwork')
    op.drop_table('assignedclass')
    op.drop_table('subject')
    op.drop_table('student')
    op.drop_table('staff')
    op.drop_table('edgroup')
    op.drop_table('user')
    op.drop_index(op.f('ix_faculty_name'), table_name='faculty')
    op.drop_table('faculty')
    # ### end Alembic commands ###
