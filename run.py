"""
程序启动入口
"""
import os, sys

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from backend.app import run_server

if __name__ == '__main__':
    print("=" * 50)
    print("Doris数据库查询工具")
    print("=" * 50)
    run_server()