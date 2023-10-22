"""init

Revision ID: e8c84da838c2
Revises: 
Create Date: 2023-10-16 15:07:13.781840

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = 'e8c84da838c2'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('cities',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=50), nullable=True),
    sa.Column('country', sa.String(length=2), nullable=True),
    sa.Column('state', sa.String(length=50), nullable=True),
    sa.Column('latitude', sa.Float(), nullable=True),
    sa.Column('longitude', sa.Float(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name', 'country'),
    sa.CheckConstraint('-90 <= latitude AND latitude <= 90', name='lat_check'),
    sa.CheckConstraint('-180 <= longitude AND longitude <= 180', name='lon_check')
    )
    op.create_table('conditions',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('main', sa.String(length=20), nullable=True),
    sa.Column('description', sa.String(length=50), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('weather_fact',
    sa.Column('timestamp', sa.DateTime(), primary_key=True),
    sa.Column('temp', sa.Float(), nullable=True),
    sa.Column('temp_min', sa.Float(), nullable=True),
    sa.Column('temp_max', sa.Float(), nullable=True),
    sa.Column('pressure', sa.Integer(), nullable=True),
    sa.Column('humidity', sa.Integer(), nullable=True),
    sa.Column('wind_speed', sa.Float(), nullable=True),
    sa.Column('wind_direction', sa.Integer(), nullable=True),
    sa.Column('wind_gust', sa.Float(), nullable=True),
    sa.Column('clouds', sa.Integer(), nullable=True),
    sa.Column('city', sa.Integer(), nullable=True),
    sa.Column('condition', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['city'], ['cities.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['condition'], ['conditions.id'], ondelete='RESTRICT'),
    sa.PrimaryKeyConstraint('timestamp', 'city'),
    sa.CheckConstraint('100 < temp AND temp < 400', name='temp_check'),
    sa.CheckConstraint('100 < temp_min AND temp_min < 400', name='min_temp_check'),
    sa.CheckConstraint('100 < temp_max AND temp_max < 400', name='max_temp_check'),
    sa.CheckConstraint('0 < pressure AND pressure < 2000', name='pressure_check'),
    sa.CheckConstraint('0 <= humidity AND humidity <= 100', name='humidity_check'),
    sa.CheckConstraint('0 <= clouds AND clouds <= 100', name='clouds_check'),
    sa.CheckConstraint('0 <= wind_speed AND wind_speed < 1000', name='wind_speed_check'),
    sa.CheckConstraint('0 <= wind_direction AND wind_direction <= 360', name='wind_dir_check'),
    sa.CheckConstraint('0 <= wind_gust AND wind_gust < 1000', name='wind_gust_check')

    )
    op.create_table('weather_forecast',
    sa.Column('timestamp', sa.DateTime(), primary_key=True),
    sa.Column('temp', sa.Float(), nullable=True),
    sa.Column('temp_min', sa.Float(), nullable=True),
    sa.Column('temp_max', sa.Float(), nullable=True),
    sa.Column('pressure', sa.Integer(), nullable=True),
    sa.Column('humidity', sa.Integer(), nullable=True),
    sa.Column('wind_speed', sa.Float(), nullable=True),
    sa.Column('wind_direction', sa.Integer(), nullable=True),
    sa.Column('wind_gust', sa.Float(), nullable=True),
    sa.Column('clouds', sa.Integer(), nullable=True),
    sa.Column('city', sa.Integer(), nullable=True),
    sa.Column('condition', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['city'], ['cities.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['condition'], ['conditions.id'], ondelete='RESTRICT'),
    sa.PrimaryKeyConstraint('timestamp', 'city'),
    sa.CheckConstraint('100 < temp AND temp < 400', name='temp_check'),
    sa.CheckConstraint('100 < temp_min AND temp_min < 400', name='min_temp_check'),
    sa.CheckConstraint('100 < temp_max AND temp_max < 400', name='max_temp_check'),
    sa.CheckConstraint('0 < pressure AND pressure < 2000', name='pressure_check'),
    sa.CheckConstraint('0 <= humidity AND humidity <= 100', name='humidity_check'),
    sa.CheckConstraint('0 <= clouds AND clouds <= 100', name='clouds_check'),
    sa.CheckConstraint('0 <= wind_speed AND wind_speed < 1000', name='wind_speed_check'),
    sa.CheckConstraint('0 <= wind_direction AND wind_direction <= 360', name='wind_dir_check'),
    sa.CheckConstraint('0 <= wind_gust AND wind_gust < 1000', name='wind_gust_check')
    )


def downgrade() -> None:
    op.drop_table('weather_forecast')
    op.drop_table('weather_fact')
    op.drop_table('conditions')
    op.drop_table('cities')
