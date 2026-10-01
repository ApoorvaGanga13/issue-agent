from collections import Counter


def top_words(text, n):
    counts = Counter(text.split())
    return [w for w, _ in counts.most_common(n)]
