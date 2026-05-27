import json

try:
    from openai import OpenAI
    _OPENAI_AVAILABLE = True
except ImportError:
    _OPENAI_AVAILABLE = False


def _build_prompt(asin: str, niche: str, market: dict, brand: dict,
                  seller: dict, price: dict, keyword: dict, prediction: dict) -> str:
    return f"""
You are an expert Amazon product research analyst.

Analyze the following market data for niche: "{niche}" (reference ASIN: {asin}).

MARKET OVERVIEW:
- Total Monthly Revenue: ${market['total_revenue']:,.0f}
- Total Units Sold/mo: {market['total_units']:,}
- Avg Price: ${market['avg_price']:.2f} | Median: ${market['median_price']:.2f}
- Avg Reviews: {market['avg_reviews']:.0f}
- Revenue Concentration (top 20%): {market['revenue_concentration']}%

BRAND ANALYSIS:
- Total Brands: {brand['total_brands']}
- Top 3 Revenue Share: {brand['top3_revenue_share']}%
- HHI: {brand['hhi']} (>2500 = highly concentrated)
- Top brands: {', '.join([b['brand'] + ' (' + str(b['revenue_share']) + '%)' for b in brand['top_brands'][:5]])}

SELLER INTELLIGENCE:
- Old Sellers (>2yr): {seller['old_count']} | Revenue Share: {seller['old_revenue_share']}%
- New Sellers (<2yr): {seller['new_count']} | Revenue Share: {seller['new_revenue_share']}%
- New Seller Success Rate: {seller['new_seller_success_rate']}%

PRICE ANALYSIS:
- Best Performing Segment: {price.get('best_label', 'N/A')}
- Price Range: ${price.get('price_stats', {}).get('min', 0):.2f} – ${price.get('price_stats', {}).get('max', 0):.2f}

TOP KEYWORDS: {', '.join([k['keyword'] for k in keyword.get('top_keywords', [])[:8]]) or 'N/A'}

PREDICTION SCORE: {prediction['score']}/100 — {prediction['verdict']}

Provide a concise analysis with these 4 sections:
1. OPPORTUNITIES (3 bullet points — specific actionable opportunities)
2. RISKS (3 bullet points — key risks a new seller faces)
3. LAUNCH STRATEGY (2 bullet points — pricing and differentiation advice)
4. SUMMARY (1 sentence verdict on whether to enter this market)

Respond in JSON format:
{{
  "opportunities": ["...", "...", "..."],
  "risks": ["...", "...", "..."],
  "launch_strategy": ["...", "..."],
  "summary": "..."
}}
"""


def run(asin: str, niche: str, market: dict, brand: dict, seller: dict,
        price: dict, keyword: dict, prediction: dict, api_key: str = None) -> dict:

    if not _OPENAI_AVAILABLE or not api_key:
        return _fallback_insights(market, brand, seller, prediction)

    try:
        client = OpenAI(api_key=api_key)
        prompt = _build_prompt(asin, niche, market, brand, seller, price, keyword, prediction)

        from openai.types.shared_params import ResponseFormatJSONObject
        response = client.chat.completions.create(
            model='gpt-4o',
            messages=[{'role': 'user', 'content': prompt}],
            temperature=0.4,
            max_tokens=800,
            response_format=ResponseFormatJSONObject(type='json_object'),
        )

        content = response.choices[0].message.content
        return json.loads(content)

    except Exception as e:
        return _fallback_insights(market, brand, seller, prediction)


def _fallback_insights(market: dict, brand: dict, seller: dict, prediction: dict) -> dict:
    score = prediction.get('score', 50)
    top3 = brand.get('top3_revenue_share', 50)
    new_success = seller.get('new_seller_success_rate', 0)
    rev = market.get('total_revenue', 0)

    opps = []
    if rev > 200_000:
        opps.append(f"Large market with ${rev:,.0f}/mo total revenue presents meaningful volume opportunity.")
    if top3 < 60:
        opps.append("No single brand dominates — market is fragmented and accessible to new entrants.")
    if new_success > 20:
        opps.append(f"{new_success:.0f}% of new sellers are achieving meaningful revenue — market is enterable.")
    if not opps:
        opps.append("Niche market with potential for targeted positioning and differentiation.")

    risks = []
    avg_rev = market.get('avg_reviews', 0)
    if avg_rev > 1000:
        risks.append(f"High review barrier — competitors average {avg_rev:.0f} reviews, requiring aggressive early review strategy.")
    if top3 > 50:
        risks.append(f"Top 3 brands control {top3}% of revenue — strong incumbent presence to compete against.")
    risks.append("Amazon PPC costs in established niches can erode margins — budget carefully for launch phase.")

    strategy = [
        "Launch at 10–15% below market median price to gain initial traction, then raise price after accumulating 50+ reviews.",
        "Differentiate through superior listing quality — professional images, keyword-rich title, and detailed bullet points targeting gaps in competitor listings.",
    ]

    if score >= 65:
        summary = "This market shows strong fundamentals — proceed with launch planning and a focused differentiation strategy."
    elif score >= 40:
        summary = "Market is viable but competitive — success depends on tight execution, strong listing quality, and disciplined PPC management."
    else:
        summary = "High barriers and competition make this market challenging — consider pivoting to an adjacent niche with lower entry friction."

    return {
        'opportunities': opps[:3],
        'risks': risks[:3],
        'launch_strategy': strategy,
        'summary': summary,
    }
