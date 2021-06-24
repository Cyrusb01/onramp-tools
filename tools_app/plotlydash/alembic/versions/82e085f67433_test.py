"""test

Revision ID: 82e085f67433
Revises: 
Create Date: 2021-06-23 11:10:13.170056

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '82e085f67433'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "cryptocurrency_pairs",
        sa.Column('asset_1', sa.String),
        sa.Column('asset_2', sa.String),
        sa.Column('price_close', sa.Float),
        sa.Column('price_high', sa.Float),
        sa.Column('price_low', sa.Float),
        sa.Column('price_open', sa.Float),
        sa.Column('volume', sa.Float),
        sa.Column('datetime', sa.DateTime)
    )
    op.create_primary_key(
        "pk_cryptocurrency_pairs", "cryptocurrency_pairs",
        ["asset_1", "asset_2", "datetime"]
    )

    op.create_table(
        "close_data",
        sa.Column("symbol", sa.String, primary_key=True),
        sa.Column("close", sa.Float),
        sa.Column("date", sa.Date, primary_key= True)
    )


def downgrade():
    op.drop_table("cryptocurrency_pairs")
