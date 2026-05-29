from alembic import op
import sqlalchemy as sa

revision = "1"
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        "vehicles",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("vehicle_type", sa.String(20), nullable=False),
        sa.Column("model", sa.String(120), nullable=False),
        sa.Column("year", sa.Integer(), nullable=False),
        sa.Column("manufacturer", sa.String(120), nullable=False),
    )

    op.create_table(
        "cars",
        sa.Column("id", sa.Integer(), sa.ForeignKey("vehicles.id", ondelete="CASCADE"), primary_key=True),
        sa.Column("colour", sa.String(60)),
        sa.Column("engine_size", sa.Float()),
        sa.Column("horsepower", sa.Integer()),
        sa.Column("seats", sa.Integer()),
        sa.Column("top_speed", sa.Float()),
    )

    op.create_table(
        "bikes",
        sa.Column("id", sa.Integer(), sa.ForeignKey("vehicles.id", ondelete="CASCADE"), primary_key=True),
        sa.Column("gears", sa.Integer()),
        sa.Column("type", sa.String(60)),
        sa.Column("wheel_size", sa.Integer()),
    )

    op.create_table(
        "spaceships",
        sa.Column("id", sa.Integer(), sa.ForeignKey("vehicles.id", ondelete="CASCADE"), primary_key=True),
        sa.Column("max_crew", sa.Integer()),
        sa.Column("top_speed", sa.Float()),
    )

def downgrade():
    op.drop_table("spaceships")
    op.drop_table("bikes")
    op.drop_table("cars")
    op.drop_table("vehicles")
