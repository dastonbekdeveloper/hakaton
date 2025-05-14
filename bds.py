import sqlite3
import kategoriya
import sqlite3
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.patches import Patch
# Подключение к базе данных (создаст файл, если его нет)
# conn = sqlite3.connect("my_database.db")
# cursor = conn.cursor()

# # Создание таблиц
# cursor.execute("""
# CREATE TABLE IF NOT EXISTS meter_failure (
#     question TEXT NOT NULL,
#     answer TEXT NOT NULL
# )
# """)

# cursor.execute("""
# CREATE TABLE IF NOT EXISTS overconsumption (
#     question TEXT NOT NULL,
#     answer TEXT NOT NULL
# )
# """)

# cursor.execute("""
# CREATE TABLE IF NOT EXISTS malfunction (
#     question TEXT NOT NULL,
#     answer TEXT NOT NULL
# )
# """)

# cursor.execute("""
# CREATE TABLE IF NOT EXISTS savings_opportunity (
#     question TEXT NOT NULL,
#     answer TEXT NOT NULL
# )
# """)

# cursor.execute("""
# CREATE TABLE IF NOT EXISTS billing_error (
#     question TEXT NOT NULL,
#     answer TEXT NOT NULL
# )
# """)

# cursor.execute("""
# CREATE TABLE IF NOT EXISTS general_inquiry (
#     question TEXT NOT NULL,
#     answer TEXT NOT NULL
# )
# """)
def kategoriyas(question,answer):
    arr = kategoriya.classify_with_threshold(question)
    with sqlite3.connect("my_database.db") as conn:
        cursor = conn.cursor()
        for d in arr:
            cursor.execute(f"""
            INSERT INTO {d} (question, answer)
            VALUES (?, ?)
            """, (question, answer))


def pie_chart():
    # Изначально таблицы с нулями
    tables = {
        "meter_failure": 0,
        "overconsumption": 0,
        "malfunction": 0,
        "savings_opportunity": 0,
        "billing_error": 0,
        "general_inquiry": 0
    }

    # Открытие БД с with и подсчёт записей
    with sqlite3.connect("my_database.db") as conn:
        cursor = conn.cursor()

        for table in tables:
            try:
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                count = cursor.fetchone()[0]
                tables[table] = count  # Присваиваем значение в словарь
            except sqlite3.OperationalError as e:
                print(f"Ошибка в таблице '{table}': {e}")



    # --- Подготовка данных для pie (только ненулевые):
    filtered = {k: v for k, v in tables.items() if v > 0}
    labels = list(filtered.keys())
    sizes  = list(filtered.values())

    # --- Цвета для ненулевых секторов:
    colors = cm.Set3.colors[:len(sizes)]

    # --- Строим pie:
    fig, ax = plt.subplots(figsize=(9, 6))
    wedges, texts, autotexts = ax.pie(
        sizes,
        
        autopct='%1.1f%%',
        startangle=140,
        colors=colors,
        textprops={'color': 'black', 'weight': 'bold'}
    )

    # --- Создаём маппинг от имени категории к её wedge:
    wedge_map = {label: wedge for label, wedge in zip(labels, wedges)}

    # --- Подготавливаем handles и подписи для легенды (в порядке всех категорий):
    handles = []
    legend_labels = []
    rs_tables = [
        "Проблемы со счётчиком",
        "Перерасход",
        "Неисправности в электроснабжении",
        "Возможности Экономии Электроэнергии",
        "Ошибки в Счетах",
        "Общие Вопросы"
    ]
    zero_color = 'lightgrey'
    a = 0
    for name, count in tables.items():
        pretty = name.replace('_', ' ').title()  # Красивое название

        legend_labels.append(f"{rs_tables[a]} — {count} шт.")
        a+=1
        if count > 0:
            handles.append(wedge_map[name])
        else:
            handles.append(Patch(facecolor=zero_color, edgecolor='none'))
    # --- Рисуем легенду с выносом вправо:
    ax.legend(
        handles,
        legend_labels,
        title="Категории",
        loc="center left",
        bbox_to_anchor=(1, 0, 0.5, 1),
        fontsize=10,
        title_fontsize=12
    )

    # --- Финальные штрихи:
    ax.set_title("Распределение вопросов по категориям", fontsize=14, fontweight='bold', pad=20)
    plt.tight_layout()
    plt.savefig("pie_chart.png", dpi=120, bbox_inches='tight')
