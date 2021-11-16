def limit_characters(string, chars):
    return "".join(list(filter(lambda ch: ch in str(chars), string)))

def remove_characters(string, chars):
    return "".join(list(filter(lambda ch: ch not in str(chars), string)))