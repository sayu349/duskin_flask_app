"""empty message

Revision ID: a38fd7b5f0d3
Revises: 
Create Date: 2023-12-21 20:54:26.919535

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a38fd7b5f0d3'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('customers',
    sa.Column('customer_id', sa.Integer(), nullable=False),
    sa.Column('customer_name', sa.String(), nullable=False),
    sa.Column('telephon_number', sa.String(), nullable=False),
    sa.Column('customer_situation', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('customer_id')
    )
    op.create_table('period',
    sa.Column('period_id', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('period_id')
    )
    op.create_table('products',
    sa.Column('product_id', sa.String(), nullable=False),
    sa.Column('product_name', sa.String(), nullable=False),
    sa.Column('product_price', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('product_id')
    )
    op.create_table('contracts',
    sa.Column('contract_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('period_id', sa.String(), nullable=False),
    sa.Column('customer_id', sa.Integer(), nullable=False),
    sa.Column('product_id', sa.String(), nullable=False),
    sa.Column('contract_number', sa.Integer(), nullable=False),
    sa.Column('contract_situation', sa.String(), nullable=False),
    sa.Column('pay_method_id', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['customer_id'], ['customers.customer_id'], ),
    sa.ForeignKeyConstraint(['period_id'], ['period.period_id'], ),
    sa.ForeignKeyConstraint(['product_id'], ['products.product_id'], ),
    sa.PrimaryKeyConstraint('contract_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('contracts')
    op.drop_table('products')
    op.drop_table('period')
    op.drop_table('customers')
    # ### end Alembic commands ###