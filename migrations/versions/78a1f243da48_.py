"""empty message

Revision ID: 78a1f243da48
Revises: 
Create Date: 2021-12-19 18:40:13.124920

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '78a1f243da48'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('test')
    op.drop_table('testpass')
    op.drop_table('labworkdeadline')
    op.drop_table('subject')
    op.drop_table('testdeadline')
    op.drop_table('labworkpass')
    op.drop_table('student')
    op.drop_table('edgroup')
    op.drop_table('assignedclass')
    op.drop_table('labwork')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('labwork',
    sa.Column('id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('subject', sa.VARCHAR(length=50), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['subject'], ['subject.name'], name='labwork_subject_fkey'),
    sa.PrimaryKeyConstraint('id', 'subject', name='labwork_pkey'),
    postgresql_ignore_search_path=False
    )
    op.create_table('assignedclass',
    sa.Column('edgroup', sa.VARCHAR(length=10), autoincrement=False, nullable=False),
    sa.Column('subject', sa.VARCHAR(length=50), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['edgroup'], ['edgroup.id'], name='assignedclass_edgroup_fkey'),
    sa.ForeignKeyConstraint(['subject'], ['subject.name'], name='assignedclass_subject_fkey'),
    sa.PrimaryKeyConstraint('edgroup', 'subject', name='assignedclass_pkey')
    )
    op.create_table('edgroup',
    sa.Column('id', sa.VARCHAR(length=10), autoincrement=False, nullable=False),
    sa.Column('course', sa.SMALLINT(), autoincrement=False, nullable=True),
    sa.Column('faculty', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['faculty'], ['faculty.id'], name='edgroup_faculty_fkey'),
    sa.PrimaryKeyConstraint('id', name='edgroup_pkey'),
    postgresql_ignore_search_path=False
    )
    op.create_table('student',
    sa.Column('id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('name', sa.VARCHAR(length=50), autoincrement=False, nullable=True),
    sa.Column('grants', postgresql.MONEY(), autoincrement=False, nullable=True),
    sa.Column('education', sa.VARCHAR(length=50), autoincrement=False, nullable=True),
    sa.Column('edgroup', sa.VARCHAR(length=10), autoincrement=False, nullable=True),
    sa.CheckConstraint("((education)::text ~~ '%%-Бюджет'::text) OR (((education)::text ~~ '%%-Контракт'::text) AND (grants = NULL::money))", name='student_check'),
    sa.ForeignKeyConstraint(['edgroup'], ['edgroup.id'], name='student_edgroup_fkey'),
    sa.PrimaryKeyConstraint('id', name='student_pkey'),
    postgresql_ignore_search_path=False
    )
    op.create_table('labworkpass',
    sa.Column('id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('subject', sa.VARCHAR(length=50), autoincrement=False, nullable=False),
    sa.Column('studentid', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('mark', sa.SMALLINT(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['id', 'subject'], ['labwork.id', 'labwork.subject'], name='labworkpass_id_subject_fkey'),
    sa.ForeignKeyConstraint(['studentid'], ['student.id'], name='labworkpass_studentid_fkey'),
    sa.PrimaryKeyConstraint('id', 'subject', 'studentid', name='labworkpass_pkey')
    )
    op.create_table('testdeadline',
    sa.Column('id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('subject', sa.VARCHAR(length=50), autoincrement=False, nullable=False),
    sa.Column('edgroup', sa.VARCHAR(length=10), autoincrement=False, nullable=False),
    sa.Column('deadline', sa.DATE(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['id', 'subject'], ['test.id', 'test.subject'], name='testdeadline_id_subject_fkey'),
    sa.PrimaryKeyConstraint('id', 'subject', 'edgroup', name='testdeadline_pkey')
    )
    op.create_table('subject',
    sa.Column('name', sa.VARCHAR(length=50), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('name', name='subject_pkey'),
    postgresql_ignore_search_path=False
    )
    op.create_table('labworkdeadline',
    sa.Column('id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('subject', sa.VARCHAR(length=50), autoincrement=False, nullable=False),
    sa.Column('edgroupid', sa.VARCHAR(length=10), autoincrement=False, nullable=False),
    sa.Column('deadline', sa.DATE(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['edgroupid'], ['edgroup.id'], name='labworkdeadline_edgroupid_fkey'),
    sa.ForeignKeyConstraint(['id', 'subject'], ['labwork.id', 'labwork.subject'], name='labworkdeadline_id_subject_fkey'),
    sa.PrimaryKeyConstraint('id', 'edgroupid', 'subject', name='labworkdeadline_pkey')
    )
    op.create_table('testpass',
    sa.Column('id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('studentid', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('subject', sa.VARCHAR(length=50), autoincrement=False, nullable=False),
    sa.Column('mark', sa.SMALLINT(), autoincrement=False, nullable=True),
    sa.CheckConstraint('(mark >= 2) AND (mark <= 5)', name='testpass_mark_check'),
    sa.ForeignKeyConstraint(['id', 'subject'], ['test.id', 'test.subject'], name='testpass_id_subject_fkey'),
    sa.ForeignKeyConstraint(['studentid'], ['student.id'], name='testpass_studentid_fkey'),
    sa.PrimaryKeyConstraint('id', 'subject', 'studentid', name='testpass_pkey')
    )
    op.create_table('test',
    sa.Column('id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('subject', sa.VARCHAR(length=50), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['subject'], ['subject.name'], name='test_subject_fkey'),
    sa.PrimaryKeyConstraint('id', 'subject', name='test_pkey')
    )
    # ### end Alembic commands ###
