"""Added price column

Revision ID: 51f0ce13122b
Revises: fdb1f2b7f91b
Create Date: 2021-02-20 16:33:13.411590

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '51f0ce13122b'
down_revision = 'fdb1f2b7f91b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('product', sa.Column('price', sa.Integer(), nullable=False))
    op.drop_constraint(None, 'product', type_='foreignkey')
    op.drop_column('product', 'cus_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('product', sa.Column('cus_id', sa.INTEGER(), nullable=True))
    op.create_foreign_key(None, 'product', 'user', ['cus_id'], ['id'])
    op.drop_column('product', 'price')
    # ### end Alembic commands ###
