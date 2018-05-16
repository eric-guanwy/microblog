"""add language to posts

Revision ID: e747ad5c1102
Revises: 33cdc48a7e52
Create Date: 2018-05-17 00:03:40.496249

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e747ad5c1102'
down_revision = '33cdc48a7e52'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('project')
    op.drop_table('general_project')
    op.drop_table('sub_item')
    op.add_column('post', sa.Column('language', sa.String(length=5), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('post', 'language')
    op.create_table('sub_item',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('itemname', sa.VARCHAR(length=140), nullable=True),
    sa.Column('weight', sa.FLOAT(), nullable=True),
    sa.Column('project_id', sa.INTEGER(), nullable=True),
    sa.ForeignKeyConstraint(['project_id'], ['project.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('general_project',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('generalprojectname', sa.VARCHAR(length=140), nullable=True),
    sa.Column('weight', sa.FLOAT(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('project',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('projectname', sa.VARCHAR(length=140), nullable=True),
    sa.Column('weight', sa.FLOAT(), nullable=True),
    sa.Column('GeneralProject_id', sa.INTEGER(), nullable=True),
    sa.ForeignKeyConstraint(['GeneralProject_id'], ['general_project.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###
