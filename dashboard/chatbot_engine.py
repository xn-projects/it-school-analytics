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


def choose_language():
    print('\n=== Language Selection ===\n')
    print('1. Русский (ru)')
    print('2. English (en)')
    print('3. Deutsch (de)\n')

    lang_map = {
        '1': 'ru',
        'ru': 'ru',
        'русский': 'ru',

        '2': 'en',
        'en': 'en',
        'english': 'en',

        '3': 'de',
        'de': 'de',
        'deutsch': 'de'
    }

    while True:
        choice = input(
            'Choose language / Выберите язык / Sprache auswählen (1–3 or ru/en/de): '
        ).strip().lower()

        if choice in lang_map:
            STATE['lang'] = lang_map[choice]
            return

        print('Invalid choice. Try again.')


def choose_page():
    lang = STATE['lang']
    pages = DASHBOARD['pages']

    titles = {
        'ru': '=== Выбор страницы дашборда ===',
        'en': '=== Select Dashboard Page ===',
        'de': '=== Dashboard-Seite auswählen ==='
    }

    print(f'\n{titles[lang]}\n')

    print(f"1. {pages[0]['title'][lang]}")
    print(f"2. {pages[1]['title'][lang]}")

    while True:
        choice = input({
            'ru': '\nВаш выбор (1 или 2): ',
            'en': '\nYour choice (1 or 2): ',
            'de': '\nIhre Auswahl (1 oder 2): '
        }[lang]).strip()

        if choice == '1':
            STATE['page'] = pages[0]
            return

        if choice == '2':
            STATE['page'] = pages[1]
            return

        print({
            'ru': 'Введите 1 или 2',
            'en': 'Please enter 1 or 2',
            'de': 'Bitte geben Sie 1 oder 2 ein'
        }[lang])


def sales_page_menu():
    lang = STATE['lang']
    page = STATE['page']

    print(f"\n=== {page['title'][lang]} ===\n")

    options = {
        'ru': [
            '1. Описание фильтров',
            '2. Описание KPI-карточек',
            '3. Описание графиков',
            '4. Назад к выбору страницы'
        ],
        'en': [
            '1. Describe filters',
            '2. Describe KPI cards',
            '3. Describe charts',
            '4. Back to page selection'
        ],
        'de': [
            '1. Filterbeschreibung',
            '2. Beschreibung der KPI-Karten',
            '3. Diagrammbeschreibung',
            '4. Zurück zur Seitenauswahl'
        ]
    }

    for opt in options[lang]:
        print(opt)

    return input({
        'ru': '\nВаш выбор (1–4): ',
        'en': '\nYour choice (1–4): ',
        'de': '\nIhre Auswahl (1–4): '
    }[lang]).strip()


def marketing_page_menu():
    lang = STATE['lang']
    page = STATE['page']

    print(f"\n=== {page['title'][lang]} ===\n")

    options = {
        'ru': [
            '1. Описание маркетинговых графиков',
            '2. Выводы по всем кампаниям',
            '3. Назад к выбору страницы'
        ],
        'en': [
            '1. Describe marketing charts',
            '2. Show campaign insights',
            '3. Back to page selection'
        ],
        'de': [
            '1. Beschreibung der Marketingdiagramme',
            '2. Erkenntnisse zu allen Kampagnen',
            '3. Zurück zur Seitenauswahl'
        ]
    }

    for opt in options[lang]:
        print(opt)

    return input({
        'ru': '\nВаш выбор (1–3): ',
        'en': '\nYour choice (1–3): ',
        'de': '\nIhre Auswahl (1–3): '
    }[lang]).strip()


def print_invalid_choice():
    print({
        'ru': 'Некорректный выбор.',
        'en': 'Invalid choice.',
        'de': 'Ungültige Auswahl.'
    }[STATE['lang']])


def describe_filters():
    lang = STATE['lang']
    page = STATE['page']

    filters = page.get('filters', [])

    if not filters:
        print({
            'ru': 'Для этой страницы фильтры отсутствуют.',
            'en': 'This page has no filters.',
            'de': 'Für diese Seite sind keine Filter vorhanden.'
        }[lang])
        return

    for flt in filters:
        print(f"\n{flt['label'][lang]}")

        if flt['type'] == 'dropdown':
            for opt in flt.get('options', {}).get(lang, []):
                print(f"- {opt}")

        elif flt['type'] == 'date_range':
            label = flt['range']['label'][lang]
            if isinstance(label, list):
                for line in label:
                    print(f'- {line}')
            else:
                print(f'- {label}')


def describe_kpi():
    lang = STATE['lang']
    page = STATE['page']

    for chart in page.get('charts', []):
        if chart['type'] == 'kpi_cards':
            print(f"\n{chart['title'][lang]}")
            print(chart['description'][lang])

            print({
                'ru': '\nМетрики:',
                'en': '\nMetrics:',
                'de': '\nKennzahlen:'
            }[lang])
            for metric in chart.get('metrics', []):
                print(f"- {metric['label'][lang]}")
            return

    print({
        'ru': 'KPI-карточки на этой странице отсутствуют.',
        'en': 'No KPI cards on this page.',
        'de': 'Keine KPI-Karten auf dieser Seite.'
    }[lang])


def describe_charts():
    lang = STATE['lang']
    page = STATE['page']

    for chart in page.get('charts', []):
        if chart['type'] != 'kpi_cards':
            print(f"\n{chart['title'][lang]}")
            print(chart['description'][lang])

            insights = chart.get('insights', {}).get(lang)
            if insights:
                print({
                    'ru': 'Выводы:',
                    'en': 'Insights:',
                    'de': 'Erkenntnisse:'
                }[lang])
                for i in insights:
                    print(f'- {i}')


def sales_page_flow():
    while True:
        choice = sales_page_menu()

        if choice == '1':
            describe_filters()

        elif choice == '2':
            describe_kpi()

        elif choice == '3':
            describe_charts()

        elif choice == '4':
            return

        else:
            print_invalid_choice()


def marketing_page_flow():
    while True:
        choice = marketing_page_menu()

        if choice == '1':
            describe_charts()

        elif choice == '2':
            show_all_insights()

        elif choice == '3':
            return

        else:
            print_invalid_choice()


def page_flow():
    page_id = STATE['page']['id']

    if page_id == 'sales_analytics':
        sales_page_flow()

    elif page_id == 'marketing_analytics':
        marketing_page_flow()


def show_all_insights():
    lang = STATE['lang']
    page = STATE['page']

    for chart in page.get('charts', []):
        insights = chart.get('insights', {}).get(lang)
        if insights:
            print(f"\n{chart['title'][lang]}")
            for i in insights:
                print(f'- {i}')


def confirm_exit():
    lang = STATE['lang']

    messages = {
        'ru': ('Вы действительно хотите выйти?', '1. Да', '2. Нет'),
        'en': ('Do you really want to exit?', '1. Yes', '2. No'),
        'de': ('Möchten Sie wirklich beenden?', '1. Ja', '2. Nein')
    }

    print(f'\n{messages[lang][0]}')
    print(messages[lang][1])
    print(messages[lang][2])

    return input('\nYour choice: ').strip() == '1'


def run():
    choose_language()

    while STATE['running']:
        choose_page()
        page_flow()

        if confirm_exit():
            STATE['running'] = False


def build_chart_text(chart: dict, lang: str) -> str:
    output = []
    output.append(chart['title'][lang])
    output.append(chart['description'][lang])

    insights = chart.get('insights', {}).get(lang)
    if insights:
        output.append('')
        output.extend(insights)

    return '\n'.join(output)


def get_pages(lang: str):
    return [
        {'id': p['id'], 'title': p['title'][lang]}
        for p in DASHBOARD['pages']
    ]


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
