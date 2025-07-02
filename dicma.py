    semi_words = [text for _, text in pre_words]
    almost_words = [text for text in semi_words if '.' not in text]
    def valid(text):
        return all(not c.isupper() for c in text[1:])
    words += [text for text in almost_words if valid(text)]
    return words
