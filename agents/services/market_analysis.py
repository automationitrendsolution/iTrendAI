import pandas as pd


def run(df: pd.DataFrame) -> dict:
    rev = df['monthly_revenue'].dropna() if 'monthly_revenue' in df else pd.Series(dtype=float)
    units = df['monthly_sales'].dropna() if 'monthly_sales' in df else pd.Series(dtype=float)
    prices = df['price'].dropna() if 'price' in df else pd.Series(dtype=float)
    reviews = df['review_count'].dropna() if 'review_count' in df else pd.Series(dtype=float)

    total_revenue = float(rev.sum())
    total_units = int(units.sum())
    avg_price = float(prices.mean()) if len(prices) else 0
    median_price = float(prices.median()) if len(prices) else 0
    avg_reviews = float(reviews.mean()) if len(reviews) else 0
    _rating = df['rating'].dropna() if 'rating' in df else pd.Series(dtype=float)
    avg_rating = float(_rating.mean()) if len(_rating) else 0

    # Revenue concentration: top 20% of listings capture X% of revenue
    revenue_concentration = 0
    if len(rev) > 0 and rev.sum() > 0:
        sorted_rev = rev.sort_values(ascending=False).reset_index(drop=True)
        top_n = max(1, int(len(sorted_rev) * 0.2))
        revenue_concentration = round(float(sorted_rev.iloc[:top_n].sum() / rev.sum() * 100), 1)

    return {
        'total_revenue': round(total_revenue, 2),
        'total_units': total_units,
        'avg_price': round(avg_price, 2),
        'median_price': round(median_price, 2),
        'avg_reviews': round(avg_reviews, 0),
        'avg_rating': round(avg_rating, 2),
        'revenue_concentration': revenue_concentration,
        'total_listings': len(df),
    }
