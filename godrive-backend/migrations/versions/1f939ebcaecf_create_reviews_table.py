"""create_reviews_table

Revision ID: 1f939ebcaecf
Revises: cf54b346da40
Create Date: 2025-12-31 19:59:42.519096

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1f939ebcaecf'
down_revision: Union[str, None] = 'cf54b346da40'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Criação da tabela reviews
    op.create_table(
        'reviews',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('ride_id', sa.Integer(), nullable=False),
        sa.Column('reviewer_id', sa.Integer(), nullable=False),
        sa.Column('reviewee_id', sa.Integer(), nullable=False),
        sa.Column('rating', sa.Integer(), nullable=False),
        sa.Column('comment', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        
        # Chaves Primária e Estrangeiras
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['ride_id'], ['rides.id'], ),
        sa.ForeignKeyConstraint(['reviewer_id'], ['users.id'], ),
        sa.ForeignKeyConstraint(['reviewee_id'], ['users.id'], ),
        
        # Constraint Única: Impede que o mesmo usuário avalie a mesma aula 2x
        sa.UniqueConstraint('ride_id', 'reviewer_id', name='uq_review_ride_reviewer')
    )
    
    # Índice para a chave primária (padrão do projeto)
    op.create_index(op.f('ix_reviews_id'), 'reviews', ['id'], unique=False)


def downgrade() -> None:
    # Remove na ordem inversa
    op.drop_index(op.f('ix_reviews_id'), table_name='reviews')
    op.drop_table('reviews')