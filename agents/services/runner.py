"""
Orchestrates all analysis services for a ResearchProject.
Saves results to project.result (JSONField) and bulk-creates ProductListing rows.
"""
import traceback
from django.conf import settings

from . import excel_parser, market_analysis, brand_analysis, seller_analysis
from . import listing_quality, keyword_analysis, price_analysis, prediction, ai_insights


def run_product_research(project) -> dict:
    from agents.models import ProductListing

    project.status = 'processing'
    project.save(update_fields=['status'])

    try:
        # ── 1. Parse Excel ──────────────────────────────────────────────
        if project.uploaded_file and project.uploaded_file.name:
            project.uploaded_file.open('rb')
            try:
                df = excel_parser.parse_helium_file(project.uploaded_file)
            finally:
                project.uploaded_file.close()
        else:
            from pandas import DataFrame
            df = DataFrame()

        # ── 2. Persist raw listings ─────────────────────────────────────
        if not df.empty:
            ProductListing.objects.filter(project=project).delete()
            listings = []
            for _, row in df.iterrows():
                listings.append(ProductListing(
                    project=project,
                    asin=str(row.get('asin', '') or '')[:20],
                    title=str(row.get('title', '') or ''),
                    brand=str(row.get('brand', '') or ''),
                    seller_name=str(row.get('seller_name', '') or ''),
                    price=_safe_decimal(row.get('price')),
                    monthly_sales=_safe_int(row.get('monthly_sales')),
                    monthly_revenue=_safe_decimal(row.get('monthly_revenue')),
                    review_count=_safe_int(row.get('review_count')),
                    rating=_safe_float(row.get('rating')),
                    image_count=_safe_int(row.get('image_count')),
                    bsr=_safe_int(row.get('bsr')),
                ))
            ProductListing.objects.bulk_create(listings)

        # ── 3. Run analytics ────────────────────────────────────────────
        market  = market_analysis.run(df)
        brand   = brand_analysis.run(df)
        seller  = seller_analysis.run(df)
        listing = listing_quality.run(df)
        keyword = keyword_analysis.run(df)
        price   = price_analysis.run(df)
        pred    = prediction.run(market, brand, seller, price, listing)

        # ── 4. AI Insights ──────────────────────────────────────────────
        api_key = getattr(settings, 'OPENAI_API_KEY', None)
        insights = ai_insights.run(
            asin=project.asin,
            niche=project.niche,
            market=market,
            brand=brand,
            seller=seller,
            price=price,
            keyword=keyword,
            prediction=pred,
            api_key=api_key,
        )

        # ── 5. Save result ──────────────────────────────────────────────
        result = _to_python({
            'market':     market,
            'brand':      brand,
            'seller':     seller,
            'listing':    listing,
            'keyword':    keyword,
            'price':      price,
            'prediction': pred,
            'insights':   insights,
        })

        project.result = result
        project.status = 'complete'
        project.save(update_fields=['result', 'status', 'updated_at'])

        return result

    except Exception:
        project.status = 'failed'
        project.error_message = traceback.format_exc()
        project.save(update_fields=['status', 'error_message', 'updated_at'])
        raise


# ── Helpers ──────────────────────────────────────────────────────────────────

def _to_python(obj):
    """Recursively convert numpy/pandas types + NaN/Inf to JSON-safe native Python."""
    import math
    import numpy as np
    if isinstance(obj, dict):
        return {k: _to_python(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_to_python(i) for i in obj]
    if isinstance(obj, np.integer):
        return int(obj)
    if isinstance(obj, np.floating):
        f = float(obj)
        return None if (math.isnan(f) or math.isinf(f)) else f
    if isinstance(obj, np.bool_):
        return bool(obj)
    if isinstance(obj, np.ndarray):
        return [_to_python(i) for i in obj.tolist()]
    if hasattr(obj, 'item'):
        return _to_python(obj.item())
    if isinstance(obj, float) and (math.isnan(obj) or math.isinf(obj)):
        return None
    return obj


def _safe_decimal(val):
    try:
        import pandas as pd
        if pd.isna(val):
            return None
        return float(val)
    except Exception:
        return None


def _safe_int(val):
    try:
        import pandas as pd
        if pd.isna(val):
            return None
        return int(val)
    except Exception:
        return None


def _safe_float(val):
    try:
        import pandas as pd
        if pd.isna(val):
            return None
        return float(val)
    except Exception:
        return None
