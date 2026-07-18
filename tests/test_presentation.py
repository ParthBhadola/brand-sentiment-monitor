import unittest

from services.presentation import escape_html, sentiment_class


class PresentationTests(unittest.TestCase):
    def test_escape_html_protects_untrusted_content(self):
        value = '<img src=x onerror="alert(1)">'

        self.assertEqual(
            escape_html(value),
            "&lt;img src=x onerror=&quot;alert(1)&quot;&gt;",
        )

    def test_sentiment_class_allows_known_values_only(self):
        self.assertEqual(sentiment_class("positive"), "positive")
        self.assertEqual(sentiment_class("NEGATIVE"), "negative")
        self.assertEqual(sentiment_class("unknown injected-class"), "neutral")


if __name__ == "__main__":
    unittest.main()
