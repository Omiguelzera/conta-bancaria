"""Create Account and Transaction tables

Revision ID: 7775512e730d
Revises: 
Create Date: 2024-12-03 13:47:57.608303

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7775512e730d'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # Criando a tabela 'account'
    op.create_table(
        'account',
        sa.Column('id', sa.Integer(), primary_key=True, index=True),
        sa.Column('username', sa.String(), unique=True, nullable=False),
        sa.Column('password', sa.String(), nullable=False),
        sa.Column('balance', sa.Float(), default=0),
    )

    # Criando a tabela 'transaction'
    op.create_table(
        'transaction',
        sa.Column('id', sa.Integer(), primary_key=True, index=True),
        sa.Column('amount', sa.Float(), nullable=False),
        sa.Column('transaction_type', sa.String(), nullable=False),
        sa.Column('account_id', sa.Integer(), sa.ForeignKey('account.id')),
    )

def downgrade():
    # Removendo as tabelas em caso de downgrade
    op.drop_table('transaction')
    op.drop_table('account')
