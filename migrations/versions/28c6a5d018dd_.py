"""empty message

Revision ID: 28c6a5d018dd
Revises: 
Create Date: 2024-02-03 17:58:50.695764

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '28c6a5d018dd'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('alert', schema=None) as batch_op:
        batch_op.add_column(sa.Column('status', sa.String(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('alert', schema=None) as batch_op:
        batch_op.drop_column('status')

    # ### end Alembic commands ###
