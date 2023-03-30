"""post update

Revision ID: 60bb436ba05b
Revises: 0dea510492e9
Create Date: 2023-03-30 05:32:21.826148

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision = '60bb436ba05b'
down_revision = '0dea510492e9'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('posts', sa.Column('created_at', sa.DateTime(), nullable=True))
    op.add_column('posts', sa.Column('updated_at', sa.DateTime(), nullable=True))
    op.add_column('posts', sa.Column('publish', sa.Boolean(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('posts', 'publish')
    op.drop_column('posts', 'updated_at')
    op.drop_column('posts', 'created_at')
    # ### end Alembic commands ###