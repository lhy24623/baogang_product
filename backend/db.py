"""
Doris数据库连接模块
Doris兼容MySQL协议，使用pymysql连接
"""
import pymysql
from pymysql.cursors import DictCursor
from backend.config import DORIS_CONFIG


class DorisConnector:
    """Doris数据库连接器"""
    
    def __init__(self):
        self.connection = None
    
    def connect(self):
        """连接数据库，成功返回True，失败返回False。若已连接则直接返回True"""
        # 已有有效连接则复用
        if self.connection and self.connection.open:
            return True
        try:
            params = {
                'host': DORIS_CONFIG['host'],
                'port': DORIS_CONFIG['port'],
                'user': DORIS_CONFIG['user'],
                'password': DORIS_CONFIG['password'],
                'charset': 'utf8mb4',
                'cursorclass': DictCursor,
            }
            # database非空时才指定，留空则连接后可跨库操作
            if DORIS_CONFIG['database']:
                params['database'] = DORIS_CONFIG['database']
            self.connection = pymysql.connect(**params)
            return True
        except Exception as e:
            print(f"连接失败: {e}")
            return False
    
    def execute(self, sql):
        """执行SQL，返回 (成功标志, 结果或错误信息)。失败自动重试一次"""
        for attempt in range(2):
            if self.connection is None or not self.connection.open:
                if not self.connect():
                    return False, "数据库连接失败"
            try:
                self.connection.ping(reconnect=True)
                with self.connection.cursor() as cursor:
                    cursor.execute(sql)
                    if cursor.description:
                        result = cursor.fetchall()
                    else:
                        self.connection.commit()
                        result = cursor.rowcount
                    return True, result
            except Exception as e:
                self.connection.rollback()
                if attempt == 0:
                    # 首次失败，重置连接后重试
                    print(f"[db] 执行失败(第{attempt+1}次): {e}, 正在重试...")
                    self.connection = None
                else:
                    return False, str(e)
        return False, "数据库连接失败"
    
    def close(self):
        """关闭连接"""
        if self.connection:
            self.connection.close()
            self.connection = None


db = DorisConnector()