import pandas as pd
from datetime import date


TWO_YEARS_DAYS = 730


def _seller_age_days(creation_date) -> int | None:
    if pd.isna(creation_date):
        return None
    try:
        d = pd.to_datetime(creation_date).date()
        return (date.today() - d).days
    except Exception:
        return None


def run(df: pd.DataFrame) -> dict:
    if 'seller_creation_date' not in df or df['seller_creation_date'].isna().all():
        return {
            'old_count': 0, 'new_count': 0, 'unknown_count': len(df),
            'old_revenue_share': 0, 'new_revenue_share': 0,
            'old_avg_reviews': 0, 'new_avg_reviews': 0,
            'new_seller_success_rate': 0,
        }

    df = df.copy()
    df['seller_age_days'] = df['seller_creation_date'].apply(_seller_age_days)
    df['seller_type'] = df['seller_age_days'].apply(
        lambda d: 'old' if d is not None and d > TWO_YEARS_DAYS
        else ('new' if d is not None else 'unknown')
    )

    old = df[df['seller_type'] == 'old']
    new = df[df['seller_type'] == 'new']

    total_rev = df['monthly_revenue'].sum()

    def safe_share(subset):
        if total_rev and total_rev > 0:
            return round(float(subset['monthly_revenue'].sum() / total_rev * 100), 1)
        return 0

    def safe_avg_reviews(subset):
        vals = subset['review_count'].dropna()
        return round(float(vals.mean()), 0) if len(vals) else 0

    # New seller success: new sellers capturing meaningful revenue (>1% share each)
    if len(new) > 0 and total_rev > 0:
        new_with_rev = new[new['monthly_revenue'] > (total_rev * 0.01)]
        success_rate = round(len(new_with_rev) / len(new) * 100, 1)
    else:
        success_rate = 0

    return {
        'old_count': len(old),
        'new_count': len(new),
        'unknown_count': len(df[df['seller_type'] == 'unknown']),
        'old_revenue_share': safe_share(old),
        'new_revenue_share': safe_share(new),
        'old_avg_reviews': safe_avg_reviews(old),
        'new_avg_reviews': safe_avg_reviews(new),
        'old_avg_revenue': round(float(old['monthly_revenue'].mean()), 2) if len(old) else 0,
        'new_avg_revenue': round(float(new['monthly_revenue'].mean()), 2) if len(new) else 0,
        'new_seller_success_rate': success_rate,
    }
