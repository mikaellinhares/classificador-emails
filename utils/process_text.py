import spacy


# Rodar "python -m spacy download pt_core_news_sm"
nlp = spacy.load("pt_core_news_sm")


def process_text(text: str) -> str:
    doc = nlp(text)

    tokens_lemma = [token.lemma_ for token in doc if not token.is_stop]

    result = " ".join(tokens_lemma)

    return result
