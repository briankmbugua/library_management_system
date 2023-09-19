"""added the library table and associated it with the users table, bookMaster table, issueReturn table

Revision ID: d5c5b053dd3b
Revises: c8ce840acebc
Create Date: 2023-09-19 13:35:58.103043

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd5c5b053dd3b'
down_revision = 'c8ce840acebc'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('libraries',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('IssueReturn', schema=None) as batch_op:
        batch_op.add_column(sa.Column('library_id', sa.Integer(), nullable=False))
        batch_op.create_foreign_key(None, 'libraries', ['library_id'], ['id'])

    with op.batch_alter_table('bookMaster', schema=None) as batch_op:
        batch_op.add_column(sa.Column('library_id', sa.Integer(), nullable=False))
        batch_op.create_foreign_key(None, 'libraries', ['library_id'], ['id'])

    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('library_id', sa.Integer(), nullable=False))
        batch_op.create_foreign_key(None, 'libraries', ['library_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('library_id')

    with op.batch_alter_table('bookMaster', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('library_id')

    with op.batch_alter_table('IssueReturn', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('library_id')

    op.drop_table('libraries')
    # ### end Alembic commands ###
