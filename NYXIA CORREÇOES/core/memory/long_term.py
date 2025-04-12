import sqlite3
from datetime import datetime

class LongTermMemory:
    def __init__(self, db_file='nyxia_long_term_memory.db'):
        self.conn = sqlite3.connect(db_file)
        self._init_db()

    def _init_db(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS memories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                data TEXT NOT NULL,
                category TEXT,
                importance INTEGER DEFAULT 1,
                created_at TEXT NOT NULL,
                last_accessed TEXT NOT NULL,
                access_count INTEGER DEFAULT 0
            )
        ''')
        self.conn.commit()

    def add(self, data, category, importance=1):
        """Armazena informações por anos"""
        now = datetime.now().isoformat()
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO memories (data, category, importance, created_at, last_accessed)
            VALUES (?, ?, ?, ?, ?)
        ''', (str(data), category, importance, now, now))
        self.conn.commit()

    def retrieve(self, category=None, min_importance=0, max_results=100):
        """Recupera memórias de longo prazo com filtros"""
        query = '''
            SELECT data, category, importance 
            FROM memories 
            WHERE importance >= ?
            {category_filter}
            ORDER BY importance DESC, access_count DESC
            LIMIT ?
        '''.format(
            category_filter=f"AND category = '{category}'" if category else ""
        )
        
        cursor = self.conn.cursor()
        cursor.execute(query, (min_importance, max_results))
        
        # Atualiza contagem de acesso
        for row in cursor:
            cursor.execute('''
                UPDATE memories 
                SET access_count = access_count + 1, 
                    last_accessed = ?
                WHERE data = ? AND category = ?
            ''', (datetime.now().isoformat(), row[0], row[1]))
        
        self.conn.commit()
        return cursor.fetchall()

    def consolidate(self):
        """Remove memórias pouco acessadas e consolida espaço"""
        cursor = self.conn.cursor()
        cursor.execute('''
            DELETE FROM memories 
            WHERE access_count < 1 
            AND julianday('now') - julianday(last_accessed) > 365
        ''')
        cursor.execute('VACUUM')
        self.conn.commit()