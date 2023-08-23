def checkYorN(author):
    def inner(message):
        return message.content in ['y', 'n'] and message.author == author

    return inner


def check_a(author, author2):
    def inner(message):
        return "selected an option" in message.content and (author in message.mentions or author2 in message.mentions)

    return inner


def check_a2(author, author2, mes):
    def inner(message):
        return "selected an option" in message.content and ((author in message.mentions and author not in mes.mentions) or (author2 in message.mentions and author2 not in mes.mentions))

    return inner
