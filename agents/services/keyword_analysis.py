import re
import pandas as pd
from collections import Counter

STOP_WORDS = {
    'a', 'an', 'the', 'and', 'or', 'for', 'in', 'on', 'at', 'to', 'of',
    'with', 'by', 'from', 'is', 'it', 'its', 'be', 'as', 'up', 'are',
    'was', 'has', 'have', 'do', 'your', 'this', 'that', 'set', 'pack',
    'new', 'all', 'use', 'pro', 'plus', 'super', 'ultra', 'max', 'mini',
}

EMOTIONAL_WORDS = {
    'premium', 'luxury', 'professional', 'heavy', 'duty', 'durable',
    'easy', 'compact', 'portable', 'stylish', 'modern', 'elegant',
    'perfect', 'best', 'top', 'rated', 'waterproof', 'adjustable',
    'ergonomic', 'comfortable', 'lightweight', 'multi', 'smart',
    'high', 'quality', 'fast', 'quick', 'safe', 'certified', 'organic',
    'natural', 'eco', 'friendly', 'reusable', 'washable', 'foldable',
}


def _tokenize(text: str) -> list:
    text = text.lower()
    words = re.findall(r'\b[a-z]{3,}\b', text)
    return [w for w in words if w not in STOP_WORDS]


def run(df: pd.DataFrame) -> dict:
    if 'title' not in df or df['title'].isna().all():
        return {'top_keywords': [], 'long_tail': [], 'emotional_words': []}

    titles = df['title'].dropna().tolist()
    all_words = []
    bigrams = []

    for title in titles:
        tokens = _tokenize(str(title))
        all_words.extend(tokens)
        for i in range(len(tokens) - 1):
            bigrams.append(f"{tokens[i]} {tokens[i+1]}")

    word_freq = Counter(all_words)
    bigram_freq = Counter(bigrams)

    top_single = [{'keyword': w, 'count': c} for w, c in word_freq.most_common(15)]
    top_bigrams = [{'keyword': b, 'count': c} for b, c in bigram_freq.most_common(15)
                   if c >= 2]

    emotional = [{'keyword': w, 'count': word_freq[w]} for w in EMOTIONAL_WORDS
                 if word_freq.get(w, 0) > 0]
    emotional.sort(key=lambda x: x['count'], reverse=True)

    # Long-tail = bigrams appearing in < 30% of listings but > 1 time
    total = len(titles)
    long_tail = [b for b in top_bigrams if 1 < b['count'] < total * 0.3]

    return {
        'top_keywords': top_single[:10],
        'top_bigrams': top_bigrams[:10],
        'long_tail': long_tail[:8],
        'emotional_words': emotional[:10],
    }
