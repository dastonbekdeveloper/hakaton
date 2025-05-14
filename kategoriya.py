import requests
from typing import Dict

# Конфигурация API Hugging Face
API_URL = "https://api-inference.huggingface.co/models/sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
HEADERS = {"Authorization": "Bearer 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"}  # Замените на ваш ключ

# Описания категорий (можно расширить)
CATEGORIES = {
    "meter_failure": (
        "Проблемы со счётчиком электроэнергии: поломка прибора учёта, "
        "сбои в отображении показаний, невозможность снять или передать показания, "
        "ошибочные данные счётчика."
    ),
    "overconsumption": (
        "Необычно высокое потребление электроэнергии: увеличение расхода без видимой причины, "
        "внезапный рост показаний, подозрения на перерасход или неправильную работу техники."
    ),
    "malfunction": (
        "Неисправности в электроснабжении или оборудовании: перебои в подаче электричества, "
        "включение-выключение света, сбои в работе электроприборов, проблемы с проводкой, замыкания."
    ),
    "savings_opportunity": (
        "Вопросы об экономии электроэнергии: способы снижения потребления, переход на выгодный тариф, "
        "использование энергоэффективных приборов, советы по уменьшению счетов."
    ),
    "billing_error": (
        "Ошибки в выставленных счетах за электроэнергию: неожиданно большие суммы, "
        "несоответствие между потреблением и начислением, неправильный тариф, "
        "вопросы по перерасчёту оплаты."
    ),
    "general_inquiry": (
        "Общие или неочевидные вопросы, не подпадающие под конкретные категории: "
        "запросы информации, уточнения, обращения общего характера."
    )
}

def get_api_similarity(source_sentence: str, sentences: list) -> list:
    """Запрос к API для получения схожести текстов"""
    payload = {
        "inputs": {
            "source_sentence": source_sentence,
            "sentences": sentences
        }
    }
    response = requests.post(API_URL, headers=HEADERS, json=payload)
    return response.json()

def get_similarity_scores(input_text: str) -> Dict[str, float]:
    """Возвращает словарь с процентами схожести для всех категорий"""
    # Получаем все описания категорий
    descriptions = list(CATEGORIES.values())
    
    # Запрашиваем схожесть через API
    try:
        similarities = get_api_similarity(input_text, descriptions)
    except Exception as e:
        print(f"API Error: {e}")
        return {cat: 0.0 for cat in CATEGORIES}
    
    # Сопоставляем результаты с категориями
    scores = {
        category: round(similarity * 100, 2)
        for category, similarity in zip(CATEGORIES.keys(), similarities)
    }
    
    return dict(sorted(scores.items(), key=lambda x: x[1], reverse=True))

def classify_with_threshold(input_text: str, threshold: float = 45) -> str:
    """Классификация с пороговым значением"""
    scores = get_similarity_scores(input_text)
    tops = []
    for category, score in scores.items():
        if score >= threshold:
            tops.append(category)
    if len(tops) == 0:
        tops.append(max(scores, key=scores.get))
    return tops

# Пример использования
# question = "Счёт в этом месяце оказался слишком высоким"
# print(get_similarity_scores(question))
# print(classify_with_threshold(question))