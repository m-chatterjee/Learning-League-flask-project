"""added usr id

Revision ID: 20ddc63d2a2e
Revises: 
Create Date: 2020-12-18 19:21:02.914886

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '20ddc63d2a2e'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('student')
    op.add_column('contact_student', sa.Column('user_id', sa.Integer(), nullable=False))
    op.alter_column('contact_student', 'email',
               existing_type=sa.TEXT(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('contact_student', 'email',
               existing_type=sa.TEXT(),
               nullable=False)
    op.drop_column('contact_student', 'user_id')
    op.create_table('student',
    sa.Column('roll', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('name', sa.TEXT(), autoincrement=False, nullable=True),
    sa.Column('dept', sa.TEXT(), autoincrement=False, nullable=True),
    sa.Column('phone', sa.TEXT(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('roll', name='student_pkey')
    )
    # ### end Alembic commands ###