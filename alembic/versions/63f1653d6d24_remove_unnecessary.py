"""remove unnecessary

Revision ID: 63f1653d6d24
Revises: 8a6b4bd66fa1
Create Date: 2023-12-16 23:45:54.130515

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "63f1653d6d24"
down_revision: Union[str, None] = "8a6b4bd66fa1"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("locations")
    op.add_column("users", sa.Column("uid", sa.TEXT(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("users", "uid")
    op.create_table(
        "locations",
        sa.Column("name", sa.TEXT(), autoincrement=False, nullable=False),
        sa.Column("identifier", sa.TEXT(), autoincrement=False, nullable=False),
        sa.Column("user_id", sa.INTEGER(), autoincrement=False, nullable=True),
        sa.Column("id", sa.INTEGER(), autoincrement=True, nullable=False),
        sa.Column(
            "created_at",
            postgresql.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            autoincrement=False,
            nullable=True,
        ),
        sa.ForeignKeyConstraint(
            ["user_id"], ["users.id"], name="locations_user_id_fkey"
        ),
        sa.PrimaryKeyConstraint("id", name="locations_pkey"),
    )
    # ### end Alembic commands ###
