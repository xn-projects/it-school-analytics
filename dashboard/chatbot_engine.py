import os
import json

BASE_DIR = os.path.dirname(__file__)
JSON_PATH = os.path.join(BASE_DIR, 'chatbot.json')

with open(JSON_PATH, 'r', encoding='utf-8') as f:
    DASHBOARD = json.load(f)

STATE = {
    'lang': None,
    'running': True,
    'page': None
}


def get_sales_kpi_text(lang: str) -> str:
    page = next(p for p in DASHBOARD['pages'] if p['id'] == 'sales_analytics')
    chart = next(c for c in page['charts'] if c['type'] == 'kpi_cards')

    output = []
    output.append(chart['title'][lang])
    output.append(chart['description'][lang])
    output.append('')

    for metric in chart.get('metrics', []):
        output.append(f"- {metric['label'][lang]}")

    return '\n'.join(output)


def get_sales_filters_text(lang: str) -> str:
    page = next(p for p in DASHBOARD['pages'] if p['id'] == 'sales_analytics')

    output = []
    for flt in page.get('filters', []):
        output.append(flt['label'][lang])

        if flt['type'] == 'dropdown':
            for opt in flt['options'][lang]:
                output.append(f'- {opt}')

        if flt['type'] == 'date_range':
            for line in flt['range']['label'][lang]:
                output.append(f'- {line}')

        output.append('')

    return '\n'.join(output)


def get_marketing_insights_text(lang: str) -> str:
    page = next(p for p in DASHBOARD['pages'] if p['id'] == 'marketing_analytics')

    output = []
    for chart in page['charts']:
        insights = chart.get('insights', {}).get(lang)
        if insights:
            output.append(chart['title'][lang])
            for i in insights:
                output.append(f'- {i}')
            output.append('')

    return '\n'.join(output)


def get_sales_insights_text(lang: str) -> str:
    page = next(p for p in DASHBOARD['pages'] if p['id'] == 'sales_analytics')

    output = []
    for chart in page['charts']:
        insights = chart.get('insights', {}).get(lang)
        if insights:
            output.append(chart['title'][lang])
            for i in insights:
                output.append(f'- {i}')
            output.append('')

    return '\n'.join(output)
