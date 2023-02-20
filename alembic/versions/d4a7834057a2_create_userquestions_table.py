"""create UserQuestions table

Revision ID: d4a7834057a2
Revises: 
Create Date: 2023-02-19 15:31:32.152833

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import text

# revision identifiers, used by Alembic.
revision = 'd4a7834057a2'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'user_questions',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('user', sa.String(50), nullable=False),
        sa.Column('question', sa.String(), nullable=False),
        sa.Column('query', sa.String()),
        sa.Column('query_plan', sa.String()),
        sa.Column('query_errors', sa.String()),
        sa.Column('query_explanation', sa.String()),
        sa.Column('was_valid', sa.Boolean(), default=False),
        sa.Column('marked_good', sa.Boolean(), default=False),
        sa.Column('marked_bad', sa.Boolean(), default=False),
        sa.Column('viewed_query', sa.Boolean(), default=False),
        sa.Column('created_at', sa.DateTime(timezone=False)),
        sa.Column('updated_at', sa.DateTime(timezone=False)),
    )

def downgrade():
    op.drop_table('user_questions')
