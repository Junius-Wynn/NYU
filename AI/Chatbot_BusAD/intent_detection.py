import re #for regular expressions


def preprocess(text):
    # we apply the preprocessing steps covered in class: lowercase -> remove punctuation -> normalize whitespace
    text = text.lower()
    text = re.sub(r"[^\w\s]", " ", text)
    return " ".join(text.split())


def score_intents(user_input, patterns):
    # we score each intent using the same matching rules from the lecture
    question = preprocess(user_input)
    question_words = set(question.split())
    scores = {}

    for intent, examples in patterns.items():
        total = 0.0
        for example in examples:
            pattern = preprocess(example)
            if not pattern:
                continue
            pattern_words = set(pattern.split())
            total += 0.5 * len(question_words & pattern_words)
        scores[intent] = total

    return scores


def detect_intent(user_input, patterns, min_score=1.0):
    # we return None is the matching is weak
    scores = score_intents(user_input, patterns)
    if not scores:
        return None

    highest = max(scores.values())
    if highest < min_score:
        return None

    winners = [intent for intent, score in scores.items() if score == highest]
    return winners[0] if len(winners) == 1 else None