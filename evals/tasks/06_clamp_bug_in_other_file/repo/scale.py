from utils import clamp

def normalize_score(score):
    return clamp(score, 0, 100)
