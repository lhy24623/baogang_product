"""
Doris数据库和Flask服务配置
"""
import os

# Doris连接配置（database可不指定，后续通过USE切换）
DORIS_CONFIG = {
    'host': os.getenv('DORIS_HOST', '10.202.20.115'),
    'port': int(os.getenv('DORIS_PORT', 9030)),
    'user': os.getenv('DORIS_USER', 'analyst4'),
    'password': os.getenv('DORIS_PASSWORD', 'Analyst4@2026'),
    'database': os.getenv('DORIS_DATABASE', ''),  # 留空则不指定数据库
}

# Flask服务配置
FLASK_HOST = os.getenv('FLASK_HOST', '0.0.0.0')
FLASK_PORT = int(os.getenv('FLASK_PORT', 5000))
FLASK_DEBUG = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'