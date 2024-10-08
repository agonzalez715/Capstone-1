"""Added is_active field to Car model

Revision ID: 670aaf948c92
Revises: a19c761f7f69
Create Date: 2024-08-15 16:08:00.038435

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '670aaf948c92'
down_revision = 'a19c761f7f69'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('car', schema=None) as batch_op:
        batch_op.add_column(sa.Column('is_active', sa.Boolean(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('car', schema=None) as batch_op:
        batch_op.drop_column('is_active')

    # ### end Alembic commands ###
