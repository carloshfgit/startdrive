"""add_status_and_docs_to_instructor

Revision ID: cf54b346da40
Revises: 61cdd3387525
Create Date: 2025-12-31 19:25:36.120308

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'cf54b346da40'
down_revision: Union[str, None] = '61cdd3387525'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Cria o tipo Enum no banco (Postgres)
    # Se der erro de "type already exists", pode usar sa.String() simples, mas Enum é mais seguro
    instructor_status = sa.Enum('pending', 'verified', 'rejected', 'blocked', name='instructorstatus')
    instructor_status.create(op.get_bind(), checkfirst=True)

    op.add_column('instructor_profiles', sa.Column('status', instructor_status, nullable=False, server_default='pending'))
    op.add_column('instructor_profiles', sa.Column('cnh_url', sa.String(), nullable=True))
    op.add_column('instructor_profiles', sa.Column('vehicle_doc_url', sa.String(), nullable=True))

def downgrade() -> None:
    op.drop_column('instructor_profiles', 'vehicle_doc_url')
    op.drop_column('instructor_profiles', 'cnh_url')
    op.drop_column('instructor_profiles', 'status')
    # Opcional: Dropar o type enum
    sa.Enum(name='instructorstatus').drop(op.get_bind(), checkfirst=False)