"""Change EAA fields from int to float - SQLite compatible

Revision ID: 299606e5426d_manual
Revises: 
Create Date: 2026-01-08 17:11:20.434427

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '299606e5426d_manual'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema - SQLite compatible table recreation."""
    # Create new table with float columns
    op.create_table('whey_proteins_new',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=True),
        sa.Column('price', sa.Float(), nullable=True),
        sa.Column('brand', sa.String(), nullable=True),
        sa.Column('serving_size', sa.Integer(), nullable=True),
        sa.Column('total_weight', sa.Integer(), nullable=True),
        sa.Column('protein_per_serving', sa.Integer(), nullable=True),
        sa.Column('fenilanina', sa.Float(), nullable=True, default=0.0),
        sa.Column('histidina', sa.Float(), nullable=True, default=0.0),
        sa.Column('isoleucina', sa.Float(), nullable=True, default=0.0),
        sa.Column('leucina', sa.Float(), nullable=True, default=0.0),
        sa.Column('lisina', sa.Float(), nullable=True, default=0.0),
        sa.Column('metionina', sa.Float(), nullable=True, default=0.0),
        sa.Column('treonina', sa.Float(), nullable=True, default=0.0),
        sa.Column('triptofano', sa.Float(), nullable=True, default=0.0),
        sa.Column('valina', sa.Float(), nullable=True, default=0.0),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create indexes
    op.create_index(op.f('ix_whey_proteins_new_id'), 'whey_proteins_new', ['id'], unique=False)
    op.create_index(op.f('ix_whey_proteins_new_name'), 'whey_proteins_new', ['name'], unique=False)
    
    # Copy data if old table exists
    connection = op.get_bind()
    result = connection.execute(sa.text("SELECT name FROM sqlite_master WHERE type='table' AND name='whey_proteins'"))
    if result.fetchone():
        op.execute("""
            INSERT INTO whey_proteins_new (id, name, price, brand, serving_size, total_weight, protein_per_serving,
                                         fenilanina, histidina, isoleucina, leucina, lisina, metionina, 
                                         treonina, triptofano, valina)
            SELECT id, name, price, brand, serving_size, total_weight, protein_per_serving,
                   CAST(fenilanina AS REAL), CAST(histidina AS REAL), CAST(isoleucina AS REAL), 
                   CAST(leucina AS REAL), CAST(lisina AS REAL), CAST(metionina AS REAL),
                   CAST(treonina AS REAL), CAST(triptofano AS REAL), CAST(valina AS REAL)
            FROM whey_proteins
        """)
        
        # Drop old table
        op.drop_table('whey_proteins')
    
    # Rename new table
    op.rename_table('whey_proteins_new', 'whey_proteins')


def downgrade() -> None:
    """Downgrade schema."""
    # Create old table with integer columns
    op.create_table('whey_proteins_old',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=True),
        sa.Column('price', sa.Float(), nullable=True),
        sa.Column('brand', sa.String(), nullable=True),
        sa.Column('serving_size', sa.Integer(), nullable=True),
        sa.Column('total_weight', sa.Integer(), nullable=True),
        sa.Column('protein_per_serving', sa.Integer(), nullable=True),
        sa.Column('fenilanina', sa.Integer(), nullable=True, default=0),
        sa.Column('histidina', sa.Integer(), nullable=True, default=0),
        sa.Column('isoleucina', sa.Integer(), nullable=True, default=0),
        sa.Column('leucina', sa.Integer(), nullable=True, default=0),
        sa.Column('lisina', sa.Integer(), nullable=True, default=0),
        sa.Column('metionina', sa.Integer(), nullable=True, default=0),
        sa.Column('treonina', sa.Integer(), nullable=True, default=0),
        sa.Column('triptofano', sa.Integer(), nullable=True, default=0),
        sa.Column('valina', sa.Integer(), nullable=True, default=0),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Copy data back
    op.execute("""
        INSERT INTO whey_proteins_old (id, name, price, brand, serving_size, total_weight, protein_per_serving,
                                     fenilanina, histidina, isoleucina, leucina, lisina, metionina, 
                                     treonina, triptofano, valina)
        SELECT id, name, price, brand, serving_size, total_weight, protein_per_serving,
               CAST(fenilanina AS INTEGER), CAST(histidina AS INTEGER), CAST(isoleucina AS INTEGER), 
               CAST(leucina AS INTEGER), CAST(lisina AS INTEGER), CAST(metionina AS INTEGER),
               CAST(treonina AS INTEGER), CAST(triptofano AS INTEGER), CAST(valina AS INTEGER)
        FROM whey_proteins
    """)
    
    # Drop current table and rename
    op.drop_table('whey_proteins')
    op.rename_table('whey_proteins_old', 'whey_proteins')