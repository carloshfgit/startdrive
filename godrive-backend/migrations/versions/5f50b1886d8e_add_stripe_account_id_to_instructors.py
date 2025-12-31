"""add_stripe_account_id_to_instructors

Revision ID: 5f50b1886d8e
Revises: 56f7653188cb
Create Date: 2025-12-31 18:27:44.159344

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5f50b1886d8e'
down_revision: Union[str, None] = '56f7653188cb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Adiciona a coluna para armazenar o ID da conta conectada do Stripe
    op.add_column(
        'instructor_profiles',
        sa.Column('stripe_account_id', sa.String(), nullable=True)
    )
    
    # Cria uma constraint para garantir que um ID do Stripe não seja usado por 2 instrutores
    op.create_unique_constraint(
        'uq_instructor_stripe_account_id', 
        'instructor_profiles', 
        ['stripe_account_id']
    )


def downgrade() -> None:
    # Remove a constraint primeiro
    op.drop_constraint('uq_instructor_stripe_account_id', 'instructor_profiles', type_='unique')
    
    # Remove a coluna
    op.drop_column('instructor_profiles', 'stripe_account_id')
