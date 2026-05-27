"""
Final business prediction engine.

Score breakdown (100 pts total):
  Market Demand       — 25 pts
  Competition Level   — 25 pts  (lower brand dominance = higher score)
  New Seller Access   — 20 pts
  Price Opportunity   — 15 pts
  Listing Quality Gap — 15 pts  (low avg quality = high opportunity)
"""


def run(market: dict, brand: dict, seller: dict, price: dict, listing: dict) -> dict:

    # 1. Market Demand (25 pts)
    total_rev = market.get('total_revenue', 0)
    if total_rev >= 1_000_000:
        demand_score = 25
    elif total_rev >= 500_000:
        demand_score = 20
    elif total_rev >= 200_000:
        demand_score = 14
    elif total_rev >= 50_000:
        demand_score = 8
    else:
        demand_score = 3

    # 2. Competition (25 pts) — lower dominance = more room = higher score
    top3_share = brand.get('top3_revenue_share', 0)
    avg_reviews = market.get('avg_reviews', 0)

    if top3_share < 40:
        competition_score = 25
    elif top3_share < 55:
        competition_score = 18
    elif top3_share < 70:
        competition_score = 10
    else:
        competition_score = 4

    # Penalise for very high review barrier
    if avg_reviews > 3000:
        competition_score = max(0, competition_score - 8)
    elif avg_reviews > 1500:
        competition_score = max(0, competition_score - 4)

    # 3. New Seller Access (20 pts)
    success_rate = seller.get('new_seller_success_rate', 0)
    new_rev_share = seller.get('new_revenue_share', 0)

    if success_rate >= 40 or new_rev_share >= 30:
        seller_score = 20
    elif success_rate >= 25 or new_rev_share >= 20:
        seller_score = 15
    elif success_rate >= 10 or new_rev_share >= 10:
        seller_score = 9
    else:
        seller_score = 4

    # 4. Price Opportunity (15 pts)
    best_seg = price.get('best_segment', '')
    segs = {s['segment']: s for s in price.get('segments', [])}
    mid = segs.get('mid', {})
    mid_share = mid.get('revenue_share', 0)

    if mid_share >= 40:
        price_score = 15      # Mid-market dominant — good entry zone
    elif mid_share >= 25:
        price_score = 11
    elif best_seg == 'low':
        price_score = 6       # Low-price dominance means margin pressure
    else:
        price_score = 8

    # 5. Listing Quality Gap (15 pts) — low market quality = opportunity
    avg_listing = listing.get('avg_scores', {}).get('overall', 70)
    if avg_listing < 50:
        listing_score = 15
    elif avg_listing < 65:
        listing_score = 11
    elif avg_listing < 75:
        listing_score = 7
    else:
        listing_score = 3

    total = demand_score + competition_score + seller_score + price_score + listing_score

    if total >= 65:
        verdict = 'Suitable for Business'
        verdict_key = 'suitable'
        color = '#059669'
        bg = '#f0fdf4'
        border = '#bbf7d0'
        icon = 'bi-patch-check-fill'
    elif total >= 40:
        verdict = 'Proceed with Caution'
        verdict_key = 'caution'
        color = '#d97706'
        bg = '#fffbeb'
        border = '#fde68a'
        icon = 'bi-exclamation-triangle-fill'
    else:
        verdict = 'Not Recommended'
        verdict_key = 'not_recommended'
        color = '#dc2626'
        bg = '#fef2f2'
        border = '#fecaca'
        icon = 'bi-x-circle-fill'

    # AI confidence: scales with data completeness
    confidence = min(95, 55 + demand_score + (competition_score // 2))

    return {
        'score': total,
        'verdict': verdict,
        'verdict_key': verdict_key,
        'color': color,
        'bg': bg,
        'border': border,
        'icon': icon,
        'confidence': confidence,
        'breakdown': {
            'market_demand': demand_score,
            'competition': competition_score,
            'new_seller_access': seller_score,
            'price_opportunity': price_score,
            'listing_quality_gap': listing_score,
        },
    }
