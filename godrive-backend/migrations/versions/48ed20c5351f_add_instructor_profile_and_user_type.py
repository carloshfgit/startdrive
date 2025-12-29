"""add instructor profile and user type

Revision ID: 48ed20c5351f
Revises: 37278a644c8e
Create Date: 2025-12-28 20:44:46.228298

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import geoalchemy2  # Importante para o tipo Geometry


# revision identifiers, used by Alembic.
revision: str = '48ed20c5351f'
down_revision: Union[str, None] = '37278a644c8e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. Habilitar a extensão PostGIS (se ainda não existir)
    # Isso é necessário para usar tipos GEOMETRY
    op.execute("CREATE EXTENSION IF NOT EXISTS postgis")

    # 2. Criar a tabela de Perfil de Instrutor
    op.create_table(
        'instructor_profiles',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('bio', sa.Text(), nullable=True),
        sa.Column('hourly_rate', sa.Float(), nullable=True),
        sa.Column('cnh_category', sa.String(), nullable=True),
        sa.Column('vehicle_model', sa.String(), nullable=True),
        # Coluna Especial do PostGIS:
        sa.Column('location', geoalchemy2.types.Geometry(geometry_type='POINT', srid=4326, from_text='ST_GeomFromEWKT', name='geometry'), nullable=True),
        sa.ForeignKeyConstraint(['id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Criar índice espacial para buscas rápidas (raio km)
    # Equivalente ao 'using gist' no PostgreSQL
    conn = op.get_bind()
    insp = sa.inspect(conn)
    # Verifica se a tabela existe e se o índice ainda não existe antes de criar
    if 'instructor_profiles' in insp.get_table_names():
        if not any(idx.get('name') == 'idx_instructor_profiles_location' for idx in insp.get_indexes('instructor_profiles')):
            op.create_index('idx_instructor_profiles_location', 'instructor_profiles', ['location'], unique=False, postgresql_using='gist')

    # 3. Adicionar campo user_type na tabela users já existente
    op.add_column('users', sa.Column('user_type', sa.String(), nullable=False, server_default='student'))
    # Removemos o default do servidor depois de criar para não ficar "preso" no banco, é uma boa prática
    op.alter_column('users', 'user_type', server_default=None)


def downgrade() -> None:
    # Desfazer na ordem inversa
    op.drop_column('users', 'user_type')
    # Drop index safely if it exists
    op.execute("DROP INDEX IF EXISTS idx_instructor_profiles_location")
    op.drop_table('instructor_profiles')
    # Não removemos a extensão PostGIS no downgrade por segurança, pois outros apps podem usar