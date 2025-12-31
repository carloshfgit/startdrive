"""create_course_tables_lms

Revision ID: 78e25c396c23
Revises: 1f939ebcaecf
Create Date: 2025-12-31 20:08:07.002175

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '78e25c396c23'
down_revision: Union[str, None] = '1f939ebcaecf'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. Tabela de Cursos (Courses)
    op.create_table(
        'courses',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('price', sa.Float(), nullable=False, server_default='0.0'),
        sa.Column('cover_image_url', sa.String(), nullable=True),
        sa.Column('is_published', sa.Boolean(), nullable=True, server_default='false'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_courses_id'), 'courses', ['id'], unique=False)
    op.create_index(op.f('ix_courses_title'), 'courses', ['title'], unique=False)

    # 2. Tabela de Módulos (Modules) - Depende de Courses
    op.create_table(
        'course_modules',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('course_id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('order', sa.Integer(), nullable=True, server_default='0'),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['course_id'], ['courses.id'], ondelete='CASCADE') 
        # ondelete='CASCADE' garante que se apagar o curso, apaga os módulos
    )
    op.create_index(op.f('ix_course_modules_id'), 'course_modules', ['id'], unique=False)

    # 3. Tabela de Aulas (Lessons) - Depende de Modules
    op.create_table(
        'course_lessons',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('module_id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('video_url', sa.String(), nullable=True),
        sa.Column('duration_seconds', sa.Integer(), nullable=True, server_default='0'),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('order', sa.Integer(), nullable=True, server_default='0'),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['module_id'], ['course_modules.id'], ondelete='CASCADE')
    )
    op.create_index(op.f('ix_course_lessons_id'), 'course_lessons', ['id'], unique=False)

    # 4. Tabela de Matrículas (Enrollments) - Depende de Users e Courses
    op.create_table(
        'enrollments',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('course_id', sa.Integer(), nullable=False),
        sa.Column('price_paid', sa.Float(), nullable=False),
        sa.Column('purchased_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.ForeignKeyConstraint(['course_id'], ['courses.id'], ),
        
        # Garante que o aluno não compre o mesmo curso 2x
        sa.UniqueConstraint('user_id', 'course_id', name='uq_enrollment_user_course')
    )
    op.create_index(op.f('ix_enrollments_id'), 'enrollments', ['id'], unique=False)


def downgrade() -> None:
    # Remove as tabelas na ordem inversa (Filho -> Pai) para não quebrar FKs
    op.drop_index(op.f('ix_enrollments_id'), table_name='enrollments')
    op.drop_table('enrollments')
    
    op.drop_index(op.f('ix_course_lessons_id'), table_name='course_lessons')
    op.drop_table('course_lessons')
    
    op.drop_index(op.f('ix_course_modules_id'), table_name='course_modules')
    op.drop_table('course_modules')
    
    op.drop_index(op.f('ix_courses_title'), table_name='courses')
    op.drop_index(op.f('ix_courses_id'), table_name='courses')
    op.drop_table('courses')