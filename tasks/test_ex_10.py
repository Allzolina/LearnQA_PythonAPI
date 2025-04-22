class TestShortPhrase:
    def test_is_short_phrase(self):
        phrase = input("Set a phrase: ")
        max_len_short_phrase = 15
        len_phrase = len(phrase)

        assert len_phrase <= max_len_short_phrase, f"Phrase is longer than {max_len_short_phrase} characters"
