def choice_tag(title, desc):
    arg = title + ' ' + desc
    import json
    import os
    from django.conf import settings

    # path = os.path.dirname(os.path.join(settings.BASE_DIR, '/mefi/bot/management/commands/keywords.json'))

    with open('keywords.json', "r", encoding='utf-8') as read_file:
        data = dict(json.load(read_file))

    useless_characters = ['.', ',', '!', '?', '!?', '"', "'", "[", "]", "{", "}", ":", " - "]

    tags = []
    for i in useless_characters:
        arg = arg.replace(i, ' ')
    arg = arg.replace('    ', ' ')
    arg = arg.replace('   ', ' ')
    arg = arg.replace('  ', ' ')
    arg = arg.strip()
    # arg = arg.split(' ')
    # for i in range(len(arg)):
    #     arg[i] = arg[i].lower()
    arg = arg.lower()
    # print(arg)
    for i in data.keys():
        quent_keys = 0
        for keyword in data[i]:
            # for word in arg:
            # if keyword in word:
            quent_keys += 1
            if keyword.lower() in arg and i not in tags and quent_keys >= 2:
                tags.append(i)

    return tags

