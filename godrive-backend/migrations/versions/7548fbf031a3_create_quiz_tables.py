"""create_quiz_tables

Revision ID: 7548fbf031a3
Revises: 78e25c396c23
Create Date: 2025-12-31 20:31:40.180817

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7548fbf031a3'
down_revision: Union[str, None] = '78e25c396c23'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. Tabela Quizzes
    op.create_table(
        'quizzes',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('module_id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('passing_score', sa.Float(), nullable=True, server_default='70.0'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['module_id'], ['course_modules.id'], ondelete='CASCADE'),
    )
    op.create_index(op.f('ix_quizzes_id'), 'quizzes', ['id'], unique=False)

    # 2. Tabela Quiz Questions (Perguntas)
    op.create_table(
        'quiz_questions',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('quiz_id', sa.Integer(), nullable=False),
        sa.Column('text', sa.Text(), nullable=False),
        sa.Column('order', sa.Integer(), nullable=True, server_default='0'),
        sa.Column('points', sa.Integer(), nullable=True, server_default='1'),
        
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['quiz_id'], ['quizzes.id'], ondelete='CASCADE'),
    )
    op.create_index(op.f('ix_quiz_questions_id'), 'quiz_questions', ['id'], unique=False)

    # 3. Tabela Quiz Options (Alternativas)
    op.create_table(
        'quiz_options',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('question_id', sa.Integer(), nullable=False),
        sa.Column('text', sa.String(), nullable=False),
        sa.Column('is_correct', sa.Boolean(), nullable=True, server_default='false'),
        
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['question_id'], ['quiz_questions.id'], ondelete='CASCADE'),
    )
    op.create_index(op.f('ix_quiz_options_id'), 'quiz_options', ['id'], unique=False)

    # 4. Tabela User Quiz Attempts (Tentativas/Notas dos Alunos)
    op.create_table(
        'user_quiz_attempts',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('quiz_id', sa.Integer(), nullable=False),
        sa.Column('score_achieved', sa.Float(), nullable=False),
        sa.Column('passed', sa.Boolean(), nullable=True, server_default='false'),
        sa.Column('attempted_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.ForeignKeyConstraint(['quiz_id'], ['quizzes.id'], ),
    )
    op.create_index(op.f('ix_user_quiz_attempts_id'), 'user_quiz_attempts', ['id'], unique=False)


def downgrade() -> None:
    # Remove as tabelas na ordem inversa (Filho -> Pai)
    op.drop_index(op.f('ix_user_quiz_attempts_id'), table_name='user_quiz_attempts')
    op.drop_table('user_quiz_attempts')

    op.drop_index(op.f('ix_quiz_options_id'), table_name='quiz_options')
    op.drop_table('quiz_options')

    op.drop_index(op.f('ix_quiz_questions_id'), table_name='quiz_questions')
    op.drop_table('quiz_questions')

    op.drop_index(op.f('ix_quizzes_id'), table_name='quizzes')
    op.drop_table('quizzes')
