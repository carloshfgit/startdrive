"""create_rides_and_availability_tables

Revision ID: 56f7653188cb
Revises: 48ed20c5351f
Create Date: 2025-12-29 13:37:08.857155

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '56f7653188cb'
down_revision: Union[str, None] = '48ed20c5351f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. Tabela de Disponibilidade (Availability)
    op.create_table(
        'availabilities',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('instructor_id', sa.Integer(), nullable=False),
        sa.Column('day_of_week', sa.SmallInteger(), nullable=False), # 0-6
        sa.Column('start_time', sa.Time(), nullable=False),
        sa.Column('end_time', sa.Time(), nullable=False),
        
        # Constraints
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['instructor_id'], ['instructor_profiles.id'], )
    )
    # Índice para buscar rapidamente a agenda de um instrutor
    op.create_index(op.f('ix_availabilities_instructor_id'), 'availabilities', ['instructor_id'], unique=False)


    # 2. Tabela de Corridas/Aulas (Rides)
    op.create_table(
        'rides',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('student_id', sa.Integer(), nullable=False),
        sa.Column('instructor_id', sa.Integer(), nullable=False),
        
        # Dados da Aula
        sa.Column('scheduled_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('duration_minutes', sa.Integer(), nullable=True, server_default='50'),
        sa.Column('price', sa.Float(), nullable=False),
        sa.Column('status', sa.String(), nullable=True, server_default='pending_payment'),
        
        # Auditoria
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        
        # Constraints
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['student_id'], ['users.id'], ),
        sa.ForeignKeyConstraint(['instructor_id'], ['instructor_profiles.id'], )
    )
    
    # Índices Estratégicos
    op.create_index(op.f('ix_rides_student_id'), 'rides', ['student_id'], unique=False)
    op.create_index(op.f('ix_rides_instructor_id'), 'rides', ['instructor_id'], unique=False)
    op.create_index(op.f('ix_rides_status'), 'rides', ['status'], unique=False)


def downgrade() -> None:
    # Ordem inversa para não quebrar FKs
    op.drop_index(op.f('ix_rides_status'), table_name='rides')
    op.drop_index(op.f('ix_rides_instructor_id'), table_name='rides')
    op.drop_index(op.f('ix_rides_student_id'), table_name='rides')
    op.drop_table('rides')
    
    op.drop_index(op.f('ix_availabilities_instructor_id'), table_name='availabilities')
    op.drop_table('availabilities')
