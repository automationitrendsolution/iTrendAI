import pandas as pd
import re


def _title_score(title: str) -> float:
    if not isinstance(title, str) or not title.strip():
        return 0
    length = len(title)
    words = len(title.split())
    score = 0
    if 80 <= length <= 200:
        score += 40
    elif 50 <= length < 80 or 200 < length <= 250:
        score += 20
    if words >= 10:
        score += 30
    elif words >= 6:
        score += 15
    # Penalize ALL CAPS
    if title.isupper():
        score -= 10
    # Reward presence of numbers (sizes, quantities — good for SEO)
    if re.search(r'\d', title):
        score += 10
    return min(100, max(0, score))


def _image_score(count) -> float:
    if pd.isna(count):
        return 40  # unknown — moderate penalty
    c = int(count)
    if c >= 7:
        return 100
    if c >= 5:
        return 75
    if c >= 3:
        return 50
    return 20


def _review_score(count) -> float:
    """Proxy for listing maturity / trust."""
    if pd.isna(count):
        return 0
    c = int(count)
    if c >= 1000:
        return 100
    if c >= 500:
        return 80
    if c >= 100:
        return 60
    if c >= 25:
        return 40
    return 15


def run(df: pd.DataFrame) -> dict:
    rows = []
    for _, row in df.iterrows():
        title_sc = _title_score(row.get('title', ''))
        image_sc = _image_score(row.get('image_count'))
        review_sc = _review_score(row.get('review_count'))
        # Keyword score: titles containing brand + numeric info score higher
        kw_sc = min(100, title_sc * 0.8 + (20 if re.search(r'\d', str(row.get('title', ''))) else 0))
        overall = round(title_sc * 0.35 + image_sc * 0.25 + review_sc * 0.2 + kw_sc * 0.2, 1)
        rows.append({
            'asin': row.get('asin', ''),
            'title_score': round(title_sc, 1),
            'image_score': round(image_sc, 1),
            'review_score': round(review_sc, 1),
            'keyword_score': round(kw_sc, 1),
            'overall_score': overall,
        })

    if not rows:
        return {'avg_scores': {}, 'listings': []}

    scores_df = pd.DataFrame(rows)
    avg = {
        'title': round(float(scores_df['title_score'].mean()), 1),
        'image': round(float(scores_df['image_score'].mean()), 1),
        'review': round(float(scores_df['review_score'].mean()), 1),
        'keyword': round(float(scores_df['keyword_score'].mean()), 1),
        'overall': round(float(scores_df['overall_score'].mean()), 1),
    }

    return {
        'avg_scores': avg,
        'listings': scores_df.sort_values('overall_score', ascending=False).head(20).to_dict('records'),
    }
