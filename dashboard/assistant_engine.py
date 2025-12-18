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
    output.append(f"**{chart['title'][lang]}**")
    output.append(chart['description'][lang])
    output.append('')

    for metric in chart.get('metrics', []):
        output.append(f"**- {metric['label'][lang]}**")
        output.append(f"  {metric['description'][lang]}")

    return '\n'.join(output)


def get_sales_filters_text(lang: str) -> str:
    page = next(p for p in DASHBOARD['pages'] if p['id'] == 'sales_analytics')

    output = []
    for flt in page.get('filters', []):
        output.append(f"**{flt['label'][lang]}**")

        if 'description' in flt:
            output.append(f"  {flt['description'][lang]}")

        if flt['type'] == 'dropdown':
            options = flt.get('options')

            if isinstance(options, list):
                for opt in options:
                    output.append(f"**- {opt['label'][lang]}**")
                    if 'description' in opt:
                        output.append(f"  {opt['description'][lang]}")

            elif isinstance(options, dict):
                for opt in options.get(lang, []):
                    output.append(f"- {opt}")

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
            output.append(f"**{chart['title'][lang]}**")
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
            output.append(f"**{chart['title'][lang]}**")
            for i in insights:
                output.append(f'- {i}')
            output.append('')

    return '\n'.join(output)
