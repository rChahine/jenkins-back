"""first revision

Revision ID: ff1368ada6fe
Revises: 
Create Date: 2021-02-09 08:05:50.475162

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ff1368ada6fe'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('choices',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('wording', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('role', sa.String(), nullable=False),
    sa.Column('username', sa.String(), nullable=False),
    sa.Column('password', sa.String(), nullable=False),

    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users_x_choices',
    sa.Column('idUser', sa.Integer(), nullable=False),
    sa.Column('idChoice', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['idChoice'], ['choices.id'], ),
    sa.ForeignKeyConstraint(['idUser'], ['users.id'], ),
    sa.PrimaryKeyConstraint('idUser', 'idChoice')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users_x_choices')
    op.drop_table('users')
    op.drop_table('choices')
    # ### end Alembic commands ###
