"""post

Revision ID: 4516e0c744ff
Revises: 2f000e112c0c
Create Date: 2023-03-28 12:03:50.665489

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision = '4516e0c744ff'
down_revision = '2f000e112c0c'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('posts', sa.Column('content', sqlmodel.sql.sqltypes.AutoString(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('posts', 'content')
    # ### end Alembic commands ###