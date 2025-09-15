"""adding user

Revision ID: 01751995f451
Revises: 8eeb64ab3a60
Create Date: 2025-09-15 16:32:25.613852

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '01751995f451'
down_revision: Union[str, None] = '8eeb64ab3a60'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
