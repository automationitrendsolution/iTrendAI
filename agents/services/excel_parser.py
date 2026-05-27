import pandas as pd

# Maps our standard field names to possible Helium 10 column name variations
COLUMN_MAP = {
    'asin':                 ['asin', 'asin #', 'product asin', 'asin number'],
    'title':                ['title', 'product name', 'product title', 'name', 'listing title'],
    'brand':                ['brand', 'brand name', 'manufacturer'],
    'price':                ['price', 'buy box price', 'buybox price', 'selling price', 'current price', 'sale price'],
    'monthly_revenue':      ['monthly revenue', 'est. monthly revenue', 'estimated monthly revenue',
                             'est monthly revenue', 'revenue', 'monthly est. revenue'],
    'monthly_sales':        ['monthly sales', 'est. monthly sales', 'estimated monthly sales',
                             'est monthly sales', 'units sold', 'monthly unit sales', 'sales'],
    'review_count':         ['# of reviews', 'review count', 'reviews', 'number of reviews',
                             '# reviews', 'review #', 'ratings count', 'total reviews'],
    'rating':               ['rating', 'review rating', 'avg rating', 'average rating', 'star rating', 'stars'],
    'seller_name':          ['seller', 'seller name', 'fulfilled by', 'sold by', 'merchant'],
    'seller_creation_date': ['date first available', 'seller since', 'listing date',
                             'date listed', 'first available', 'date first listed'],
    'image_count':          ['# of images', 'image count', 'images', '# images', 'number of images', 'image #'],
    'bsr':                  ['bsr', 'best seller rank', 'sales rank', 'bsr #', 'rank'],
}


def _normalize(name: str) -> str:
    return name.strip().lower()


def _find_col(df_cols: list, candidates: list):
    lookup = {_normalize(c): c for c in df_cols}
    for candidate in candidates:
        if _normalize(candidate) in lookup:
            return lookup[_normalize(candidate)]
    return None


def _clean_numeric(series: pd.Series) -> pd.Series:
    return pd.to_numeric(
        series.astype(str).str.replace(r'[\$,£€%\s]', '', regex=True),
        errors='coerce'
    )


def parse_helium_file(file) -> pd.DataFrame:
    """
    Parse a Helium 10 Excel or CSV export into a standardized DataFrame.
    Returns a DataFrame with columns matching COLUMN_MAP keys (where found).
    """
    filename = getattr(file, 'name', '')
    try:
        if str(filename).lower().endswith('.csv'):
            raw = pd.read_csv(file)
        else:
            raw = pd.read_excel(file, engine='openpyxl')
    except Exception:
        raw = pd.read_csv(file)

    raw = raw.dropna(how='all').reset_index(drop=True)

    std = pd.DataFrame(index=raw.index)
    for field, candidates in COLUMN_MAP.items():
        col = _find_col(list(raw.columns), candidates)
        std[field] = raw[col] if col else None

    for num_col in ['price', 'monthly_revenue', 'monthly_sales', 'review_count',
                    'rating', 'image_count', 'bsr']:
        if std[num_col].notna().any():
            std[num_col] = _clean_numeric(std[num_col])

    return std
