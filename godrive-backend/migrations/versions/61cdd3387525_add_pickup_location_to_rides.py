"""add_pickup_location_to_rides

Revision ID: 61cdd3387525
Revises: 5f50b1886d8e
Create Date: 2025-12-31 19:14:57.980980

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '61cdd3387525'
down_revision: Union[str, None] = '5f50b1886d8e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('rides', sa.Column('pickup_latitude', sa.Float(), nullable=True))
    op.add_column('rides', sa.Column('pickup_longitude', sa.Float(), nullable=True))

def downgrade() -> None:
    op.drop_column('rides', 'pickup_longitude')
    op.drop_column('rides', 'pickup_latitude')