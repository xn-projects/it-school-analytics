import re
import logging
import pandas as pd
import numpy as np


def clean_duplicates(df, name, subset=None, ignore_first_col=True, preview=True):
    """
    Remove duplicate rows from a DataFrame and optionally preview them.
    """
    if subset is None:
        subset = df.columns[1:] if ignore_first_col else df.columns

    before = len(df)
    duplicates = df[df.duplicated(subset=subset, keep=False)]

    if not duplicates.empty:
        logging.info(f'{name}: {duplicates.shape[0]} duplicates found.')
        if preview:
            logging.info(f'Preview of duplicate rows in {name} (up to 5):')
            logging.info('\n' + str(duplicates.head(5)))
    else:
        logging.info(f'{name}: No duplicate rows found.')

    df = df.drop_duplicates(subset=subset, keep='first')
    after = len(df)

    logging.info(
        f'{name}: {before - after} duplicates removed '
        f'({after} rows remaining). Checked columns: {list(subset)}'
    )
    return df
    

def first_non_null(x):
    """
    Returns the first non-null (non-empty) value within each group
    """
    nonnull = x.dropna()
    return nonnull.iloc[0] if not nonnull.empty else np.nan


def clean_amount(value):
    """
    Convert amount strings to numeric values.
    Removes currency symbols, spaces and fixes decimal separators.
    """

    if pd.isna(value):
        return np.nan

    value = re.sub(r'[€$\s]+', '', str(value))
    value = value.replace('.', '').replace(',', '.')

    return pd.to_numeric(value, errors='coerce')


def normalize_german_level(value):
    """
    Determines the German language level (A0–C2)
    """

    if value is None or (isinstance(value, float) and np.isnan(value)):
        return 'Unknown'

    if (
        (isinstance(value, (int, np.integer)) and value == 0)
        or (isinstance(value, (float, np.floating)) and value == 0.0)
    ):
        return 'A0'

    if not isinstance(value, str):
        return 'Unknown'

    text = value.strip().lower()

    if re.fullmatch(r'\s*0\s*', text) or re.search(r'ня-?0', text):
        return 'A0'

    if text in ['', '-', '—', '–', 'unknown', ' ']:
        return 'Unknown'

    mapping = {'а': 'A', 'б': 'B', 'в': 'B', 'с': 'C', 'c': 'C'}
    order = {'A0': 0, 'A1': 1, 'A2': 2, 'B1': 3, 'B2': 4, 'C1': 5, 'C2': 6}

    def _norm(lvl):
        return mapping.get(lvl[0], lvl[0].upper()) + lvl[1]

    outer_m = re.match(r'^\s*([абвabc][12])\b', text)
    paren_m = re.search(r'\(([^)]{0,120})\)', text)

    if outer_m:
        outer = _norm(outer_m.group(1))

        if paren_m:
            par = paren_m.group(1).lower()

            if ('англ' in par) or ('ая' in par and 'нем' not in par and 'ня' not in par):
                return outer

            par_lvls = re.findall(r'[абвabc][12]', par)
            if par_lvls:
                par_lvl = _norm(par_lvls[-1])
                higher = order.get(par_lvl, -1) > order.get(outer, -1)

                if re.search(r'экзам', par):
                    return outer

                if higher and re.search(r'(уже|сдал|сдала|получ|ждет|ждёт|результ|итог|сертиф|сер[тц])', par):
                    return par_lvl

            return outer

    if re.search(r'([абвabc][12])\s*\([^)]*(не\s+сдал|не\s+сдала)', text):
        outer_lvl = re.match(r'\s*([абвabc][12])', text)
        if outer_lvl:
            return _norm(outer_lvl.group(1))

    if re.search(r'\bb1\b.*\bэкзам', text) and not ('нем' not in text and 'ня' not in text):
        return 'B1'
    if re.search(r'\bb1\b.*\bэкзам', text) and ('англ' in text or 'english' in text or 'eng' in text):
        return 'B1'

    if re.search(r'\bb1\b.*не\s+сдал', text) or re.search(r'\(.*не\s+сдал.*в2', text):
        return 'B1'

    if re.search(r'\bв1\b.*уч', text) and re.search(r'в2', text):
        return 'B1'

    if re.search(r'не\s+зна[юе]\s+уров', text) and re.search(r'(говор|учил)', text):
        return 'A2'

    if 'разговор' in text:
        return 'B1'

    if re.search(r'а1\s*[-–—]\s*а2(?:.*\bая\b)?', text):
        return 'A1'

    if re.search(r'а2\s*[,;.\-–—]?\s*англ', text):
        return 'A2'

    m_future = re.search(r'([абвabc][12])\s+будет\b', text)
    if m_future:
        lvl = m_future.group(1)
        return _norm(lvl)

    has_level = bool(re.search(r'[абвabc][12]', text))
    mentions_german = 'нем' in text or 'ня' in text or 'немец' in text

    if not (has_level or mentions_german):
        if any(x in text for x in ['нет', 'никакой', 'не учил', 'нулевой']):
            return 'A0'
        if re.search(r'\b0\b', text):
            return 'A0'

    if 'англ' in text or 'english' in text or 'eng' in text:
        if not ('нем' in text or 'ня' in text):
            return None
    if 'ая' in text and 'ня' not in text and 'нем' not in text:
        if re.search(r'ая\s*[абвabc][0-2]', text):
            return 'Unknown'
        return None

    if 'граждан' in text:
        return 'B1'

    if 'по факту' in text:
        levels = re.findall(r'[abcабвс][0-2]', text, flags=re.IGNORECASE)
        if len(levels) >= 2:
            lvl = levels[-1]
            return _norm(lvl)

    match_nem = re.search(
        r'(?:нем[а-я\s:;,()-]*([абвabc][0-2])|([абвabc][0-2])[а-я\s:;,()-]*нем)', text
    )
    match_nya = re.search(
        r'(?:ня[а-я\s:;,()-]*([абвabc][0-2])|([абвabc][0-2])[а-я\s:;,()-]*ня)', text
    )

    for match in [match_nem, match_nya]:
        if match:
            lvl = match.group(1) or match.group(2)
            if '0' in lvl:
                return 'A0'
            return _norm(lvl)

    match_range = re.search(r'([абвabc][0-2])\s*[-–—]\s*([абвabc][0-2])', text)
    if match_range:
        lvl = match_range.group(1)
        return _norm(lvl)

    levels = re.findall(r'[abcабвс][0-2]', text, flags=re.IGNORECASE)
    if levels:
        cleaned = [_norm(l) for l in levels]
        return sorted(cleaned, key=lambda x: order.get(x, -1))[0]

    if ('нем' in text or 'ня' in text or 'немецк' in text or 'бй' in text
        or re.search(r'\b[вb]\b', text)):
        return 'B1'

    if 'f2' in text:
        return 'A2'

    if re.search(r'\b[aа]\b', text):
        return 'A1'

    if re.search(r'\b[cс]\b', text):
        return 'C1'

    return 'Unknown'
