import pandas as pd


def run(df: pd.DataFrame) -> dict:
    if 'brand' not in df or df['brand'].isna().all():
        return {'top_brands': [], 'dominance_score': 0, 'hhi': 0}

    grp = df.groupby('brand', dropna=True).agg(
        revenue=('monthly_revenue', 'sum'),
        units=('monthly_sales', 'sum'),
        listings=('asin', 'count'),
        avg_price=('price', 'mean'),
        avg_reviews=('review_count', 'mean'),
    ).reset_index()

    total_rev = grp['revenue'].sum()
    total_units = grp['units'].sum()

    grp['revenue_share'] = (grp['revenue'] / total_rev * 100).round(1) if total_rev > 0 else 0
    grp['units_share'] = (grp['units'] / total_units * 100).round(1) if total_units > 0 else 0
    grp = grp.sort_values('revenue', ascending=False).reset_index(drop=True)

    # Herfindahl-Hirschman Index (market concentration)
    shares = grp['revenue_share'].values
    hhi = round(float((shares ** 2).sum()), 1)

    top = grp.head(10)
    top_brands = []
    for _, row in top.iterrows():
        top_brands.append({
            'brand': str(row['brand']),
            'revenue': round(float(row['revenue']), 2),
            'revenue_share': float(row['revenue_share']),
            'units_share': float(row['units_share']),
            'listings': int(row['listings']),
            'avg_price': round(float(row['avg_price']), 2) if not pd.isna(row['avg_price']) else 0,
            'avg_reviews': round(float(row['avg_reviews']), 0) if not pd.isna(row['avg_reviews']) else 0,
        })

    top3_share = float(grp.head(3)['revenue_share'].sum())

    return {
        'top_brands': top_brands,
        'top3_revenue_share': round(top3_share, 1),
        'hhi': hhi,
        'dominance_score': round(top3_share, 1),
        'total_brands': len(grp),
    }
