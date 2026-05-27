import pandas as pd


def run(df: pd.DataFrame) -> dict:
    if 'price' not in df or df['price'].isna().all():
        return {'segments': [], 'best_segment': None, 'price_stats': {}}

    prices = df['price'].dropna()

    # Dynamic segmentation: low = bottom 33%, mid = 34–66%, premium = top 33%
    p33 = float(prices.quantile(0.33))
    p66 = float(prices.quantile(0.66))

    def segment(price):
        if price <= p33:
            return 'low'
        elif price <= p66:
            return 'mid'
        return 'premium'

    df = df.copy()
    df['segment'] = df['price'].apply(lambda p: segment(p) if not pd.isna(p) else None)

    results = []
    for seg, label, color in [('low', f'Low (≤${p33:.0f})', '#059669'),
                               ('mid', f'Mid (${p33:.0f}–${p66:.0f})', '#6366f1'),
                               ('premium', f'Premium (>${p66:.0f})', '#db2777')]:
        subset = df[df['segment'] == seg]
        rev = float(subset['monthly_revenue'].sum()) if 'monthly_revenue' in subset else 0
        units = int(subset['monthly_sales'].sum()) if 'monthly_sales' in subset else 0
        total_rev = float(df['monthly_revenue'].sum()) if 'monthly_revenue' in df else 1
        results.append({
            'segment': seg,
            'label': label,
            'color': color,
            'count': len(subset),
            'revenue': round(rev, 2),
            'revenue_share': round(rev / total_rev * 100, 1) if total_rev > 0 else 0,
            'units': units,
            'avg_price': round(float(subset['price'].mean()), 2) if len(subset) else 0,
        })

    best = max(results, key=lambda x: x['revenue_share'])

    return {
        'segments': results,
        'best_segment': best['segment'],
        'best_label': best['label'],
        'price_stats': {
            'min': round(float(prices.min()), 2),
            'max': round(float(prices.max()), 2),
            'avg': round(float(prices.mean()), 2),
            'median': round(float(prices.median()), 2),
            'p33': round(p33, 2),
            'p66': round(p66, 2),
        },
    }
