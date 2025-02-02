"""Add Users

Revision ID: c803dbcc982d
Revises: 
Create Date: 2025-01-15 08:31:51.381236

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c803dbcc982d'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Customers',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('username', sa.String(length=50), nullable=False),
    sa.Column('registrated_at', sa.DateTime(), nullable=False),
    sa.Column('address', sa.String(length=50), nullable=False),
    sa.Column('email', sa.String(length=50), nullable=False),
    sa.Column('city', sa.String(length=70), nullable=False),
    sa.Column('birth_date', sa.DateTime(), nullable=False),
    sa.Column('user_type', sa.Enum('NEWBIE', 'REGULAR', 'MASTER', 'SUPER', name='usertype', create_constraint=True), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('Customers')
    # ### end Alembic commands ###
