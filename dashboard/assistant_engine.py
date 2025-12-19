import os
import json

BASE_DIR = os.path.dirname(__file__)
JSON_PATH = os.path.join(BASE_DIR, 'analytics_assistant.json')

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
    output.append(chart['title'][lang].upper())
    output.append(chart['description'][lang])
    output.append('')

    for metric in chart.get('metrics', []):
        output.append(metric['label'][lang].upper())
        output.append(metric['description'][lang])
        output.append('')

    return '\n'.join(output)


def get_sales_filters_text(lang: str) -> str:
    page = next(p for p in DASHBOARD['pages'] if p['id'] == 'sales_analytics')

    output = []
    for flt in page.get('filters', []):
        output.append(flt['label'][lang].upper())

        if 'description' in flt:
            output.append(flt['description'][lang])
        output.append('')

        if flt['type'] == 'dropdown':
            options = flt.get('options')

            if isinstance(options, list):
                for opt in options:
                    output.append(opt['label'][lang].upper())
                    if 'description' in opt:
                        output.append(opt['description'][lang])
                    output.append('')

            elif isinstance(options, dict):
                for opt in options.get(lang, []):
                    output.append(f"- {opt}")
                output.append('')

        if flt['type'] == 'date_range':
            for line in flt['range']['label'][lang]:
                output.append(f"- {line}")
            output.append('')

    return '\n'.join(output)


def get_marketing_insights_text(lang: str) -> str:
    page = next(p for p in DASHBOARD['pages'] if p['id'] == 'marketing_analytics')

    output = []
    for chart in page['charts']:
        insights = chart.get('insights', {}).get(lang)
        if insights:
            output.append(chart['title'][lang].upper())
            for i in insights:
                output.append(f"- {i}")
            output.append('')

    return '\n'.join(output)


def get_sales_insights_text(lang: str) -> str:
    page = next(p for p in DASHBOARD['pages'] if p['id'] == 'sales_analytics')

    output = []
    for chart in page['charts']:
        insights = chart.get('insights', {}).get(lang)
        if insights:
            output.append(chart['title'][lang].upper())
            for i in insights:
                output.append(f"- {i}")
            output.append('')

    return '\n'.join(output)
