"""id to uuids

Revision ID: b9329afb1296
Revises: d7eb57ff8e2e
Create Date: 2026-11-23 22:33:16.166653

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b9329afb1296'
down_revision: Union[str, Sequence[str], None] = 'd7eb57ff8e2e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """The ids of category and product change from numbers to UUIDs. The data and the links stay."""
    # Step 1: bring the new in. Every row gets a new id, and every product gets the new id of its category.
    op.add_column("category", sa.Column("new_id", sa.CHAR(32)))
    op.execute("UPDATE category SET new_id = REPLACE(UUID(), '-', '')")
    op.add_column("product", sa.Column("new_id", sa.CHAR(32)))
    op.add_column("product", sa.Column("new_category_id", sa.CHAR(32)))
    op.execute("UPDATE product SET new_id = REPLACE(UUID(), '-', '')")
    op.execute("UPDATE product p JOIN category c ON c.id = p.category_id SET p.new_category_id = c.new_id")

    # Step 2: throw the old away. First the link, then the counting, then the old columns.
    op.drop_constraint("product_ibfk_1", "product", type_="foreignkey")
    op.alter_column("product", "id", existing_type=sa.Integer(), autoincrement=False, existing_nullable=False)
    op.drop_constraint("PRIMARY", "product", type_="primary")
    op.drop_column("product", "id")
    op.drop_column("product", "category_id")
    op.alter_column("category", "id", existing_type=sa.Integer(), autoincrement=False, existing_nullable=False)
    op.drop_constraint("PRIMARY", "category", type_="primary")
    op.drop_column("category", "id")

    # Step 3: the new takes the old name, and becomes the key.
    op.alter_column("category", "new_id", new_column_name="id", existing_type=sa.CHAR(32), nullable=False)
    op.create_primary_key("pk_category", "category", ["id"])
    op.alter_column("product", "new_id", new_column_name="id", existing_type=sa.CHAR(32), nullable=False)
    op.alter_column("product", "new_category_id", new_column_name="category_id", existing_type=sa.CHAR(32))
    op.create_primary_key("pk_product", "product", ["id"])
    op.create_foreign_key("fk_product_category", "product", "category", ["category_id"], ["id"])


def downgrade() -> None:
    """Downgrade schema."""
    raise NotImplementedError("The old numbers are gone. To go back, restore the backup.")
