def choice_tag(title, desc):
    arg = title + ' ' + desc
    import json
    import os
    from django.conf import settings

    # path = os.path.dirname(os.path.join(settings.BASE_DIR, '/mefi/bot/management/commands/keywords.json'))

    with open('C:/Users/Светлана/Desktop/MeFiGit/Meetup_Finder/mefi/bot/management/commands/keywords.json', "r", encoding='utf-8') as read_file:
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

def check_conformity(first_event, second_event):
    first_description_list = first_event.el_description.split(' ')  #Разделяем описание по предложениям
    first_title_list = first_event.el_title
    second_description_list = second_event.el_description
    second_title_list = second_event.el_title

    description_len = len(first_description_list)
    conformity_counter = 0
    persent = 0
    for sentence in first_description_list:
        if sentence in second_description_list:
            conformity_counter += 1
            persent = conformity_counter / description_len * 100
    

    return persent