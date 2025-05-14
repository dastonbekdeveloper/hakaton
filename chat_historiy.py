import sqlite3
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta
import numpy as np
from collections import defaultdict
import time
class ChatAnalytics:
    def __init__(self, db_name='chat_analytics.db'):
        self.db_name = db_name
        self.init_db()
        
    def init_db(self):
        """Инициализация базы данных с улучшенной структурой"""
        with sqlite3.connect(self.db_name) as conn:
            conn.execute('''CREATE TABLE IF NOT EXISTS chat_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id BIGINT NOT NULL,
                question TEXT NOT NULL,
                answer TEXT NOT NULL,
                timestamp TEXT NOT NULL
            )''')
            
            # Создаем индексы для всех временных промежутков
            conn.execute('CREATE INDEX IF NOT EXISTS idx_timestamp ON chat_history(timestamp)')
            conn.execute('CREATE INDEX IF NOT EXISTS idx_user ON chat_history(user_id)')
            conn.execute('''
                CREATE INDEX IF NOT EXISTS idx_date 
                ON chat_history(date(timestamp))
            ''')
            conn.execute('''
                CREATE INDEX IF NOT EXISTS idx_hour 
                ON chat_history(strftime('%H', timestamp))
            ''')

    def save_chat(self, user_id, question, answer):
        """Сохранение чата в базу"""
        time.sleep(3)
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        with sqlite3.connect(self.db_name) as conn:
            conn.execute('''
                INSERT INTO chat_history (user_id, question, answer, timestamp)
                VALUES (?, ?, ?, ?)
            ''', (user_id, question, answer, timestamp))

    def get_time_stats(self, time_range='24h'):
        """
        Получение статистики за указанный период
        Поддерживаемые периоды: 24h, 7d, 30d, 1y, all
        """
        now = datetime.now()
        time_filters = {
            '24h': (now - timedelta(hours=24), '%H:%M', 'Последние 24 часа'),
            '7d': (now - timedelta(days=7), '%Y-%m-%d', 'Последние 7 дней'),
            '30d': (now - timedelta(days=30), '%Y-%m-%d', 'Последние 30 дней'),
            '1y': (now - timedelta(days=365), '%Y-%m', 'Последний год'),
            'all': (datetime(2000, 1, 1), '%Y', 'Вся история')
        }
        
        start_time, time_format, title = time_filters.get(time_range, time_filters['24h'])
        
        with sqlite3.connect(self.db_name) as conn:
            # Запросы и пользователи по времени
            stats = conn.execute(f'''
                SELECT 
                    strftime('{time_format}', timestamp) as time_unit,
                    COUNT(*) as total_requests,
                    COUNT(DISTINCT user_id) as unique_users
                FROM chat_history
                WHERE timestamp >= ?
                GROUP BY time_unit
                ORDER BY timestamp
            ''', (start_time.strftime('%Y-%m-%d %H:%M:%S'),)).fetchall()
            
            # Распределение по часам (для всех периодов кроме 24h)
            if time_range != '24h':
                hour_stats = conn.execute('''
                    SELECT 
                        strftime('%H', timestamp) as hour,
                        COUNT(*) as count
                    FROM chat_history
                    WHERE timestamp >= ?
                    GROUP BY hour
                    ORDER BY hour
                ''', (start_time.strftime('%Y-%m-%d %H:%M:%S'),)).fetchall()
            else:
                hour_stats = []
            
            # Топ активных пользователей
            top_users = conn.execute('''
                SELECT user_id, COUNT(*) as message_count
                FROM chat_history
                WHERE timestamp >= ?
                GROUP BY user_id
                ORDER BY message_count DESC
                LIMIT 5
            ''', (start_time.strftime('%Y-%m-%d %H:%M:%S'),)).fetchall()
        
        return {
            'time_stats': stats,
            'hour_stats': hour_stats,
            'top_users': top_users,
            'time_format': time_format,
            'title': title
        }

    def plot_statistics(self, time_range='24h'):
        """Визуализация статистики с улучшенным дизайном"""
        stats = self.get_time_stats(time_range)
        
        plt.style.use('seaborn-v0_8')
        fig = plt.figure(figsize=(18, 12))
        fig.suptitle(f'Аналитика чата - {stats["title"]}', fontsize=16)
        
        # Основной график активности
        ax1 = plt.subplot2grid((3, 3), (0, 0), colspan=2, rowspan=2)
        if stats['time_stats']:
            times, totals, uniques = zip(*stats['time_stats'])
            x = range(len(times))
            
            ax1.plot(x, totals, 'b-o', label='Все запросы', linewidth=2)
            ax1.plot(x, uniques, 'g--s', label='Уникальные пользователи', linewidth=2)
            
            # Настройка осей
            ax1.set_xticks(x)
            ax1.set_xticklabels(times, rotation=45 if time_range != '24h' else 0)
            ax1.set_xlabel('Временные интервалы')
            ax1.set_ylabel('Количество')
            ax1.legend()
            ax1.grid(True, linestyle='--', alpha=0.7)
            
            # Добавляем значения над точками
            for i, (total, unique) in enumerate(zip(totals, uniques)):
                ax1.text(i, total + max(totals)*0.02, str(total), ha='center')
                ax1.text(i, unique + max(totals)*0.02, str(unique), ha='center')

        # График распределения по часам
        ax2 = plt.subplot2grid((3, 3), (0, 2))
        if stats['hour_stats']:
            hours, counts = zip(*stats['hour_stats'])
            ax2.bar(hours, counts, color='orange')
            ax2.set_title('Распределение по часам')
            ax2.set_xlabel('Час дня')
            ax2.set_ylabel('Запросов')
            ax2.grid(True, linestyle=':', alpha=0.5)

        # Топ пользователей
        ax3 = plt.subplot2grid((3, 3), (1, 2))
        if stats['top_users']:
            users, counts = zip(*stats['top_users'])
            ax3.barh([f'User {u}' for u in users], counts, color='purple')
            ax3.set_title('Топ-5 активных пользователей')
            ax3.set_xlabel('Количество сообщений')
            ax3.grid(True, linestyle=':', alpha=0.5)

        # Дополнительная информация
        ax4 = plt.subplot2grid((3, 3), (2, 0), colspan=3)
        ax4.axis('off')
        
        total_messages = sum(t[1] for t in stats['time_stats']) if stats['time_stats'] else 0
        unique_users = len(set(t[2] for t in stats['time_stats'])) if stats['time_stats'] else 0
        avg_messages_per_user = total_messages / unique_users if unique_users > 0 else 0
        info_text = f"""
        Общая статистика:
        - Всего сообщений: {total_messages}
        - Уникальных пользователей: {unique_users}
        - Среднее сообщений на пользователя: {avg_messages_per_user:.1f}
        - Первое сообщение: {self._get_first_message_date()}
        """
        ax4.text(0.1, 0.5, info_text, fontsize=12)

        plt.tight_layout()
        plt.savefig(f'chat_analytics_{time_range}.png', dpi=120, bbox_inches='tight')
        plt.close()

    def _get_first_message_date(self):
        """Получение даты первого сообщения"""
        with sqlite3.connect(self.db_name) as conn:
            date = conn.execute('SELECT MIN(timestamp) FROM chat_history').fetchone()[0]
        return date if date else "нет данных"


def day():
    analytics = ChatAnalytics()
    analytics.plot_statistics('24h')
def week():
    analytics = ChatAnalytics()
    analytics.plot_statistics('7d')
def month():
    analytics = ChatAnalytics()
    analytics.plot_statistics('30d')
def year():
    analytics = ChatAnalytics()
    analytics.plot_statistics('1y')

def all():
    analytics = ChatAnalytics()
    analytics.plot_statistics('all')


    