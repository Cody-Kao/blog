"""empty message

Revision ID: 486f10025f54
Revises: 88515592df00
Create Date: 2023-07-28 16:09:20.809271

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '486f10025f54'
down_revision = '88515592df00'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('comment', schema=None) as batch_op:
        batch_op.add_column(sa.Column('date_deleted', sa.DateTime(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('comment', schema=None) as batch_op:
        batch_op.drop_column('date_deleted')

    # ### end Alembic commands ###
