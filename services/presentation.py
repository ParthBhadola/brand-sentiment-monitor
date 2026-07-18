import html


SENTIMENT_CLASSES = {
    "NEGATIVE": "negative",
    "NEUTRAL": "neutral",
    "POSITIVE": "positive",
}


def escape_html(value):
    return html.escape(str(value), quote=True)


def sentiment_class(value):
    return SENTIMENT_CLASSES.get(str(value).upper(), "neutral")
