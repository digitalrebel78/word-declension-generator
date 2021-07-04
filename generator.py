import io
import json

with io.open('model.json', 'r', encoding = 'utf8') as f:
    plain_model = f.read()
    model = json.loads(plain_model)

with io.open('input.txt', 'r', encoding = 'utf8') as f:
    words = f.read()

with io.open('output.txt', 'w', encoding = 'utf8') as f:
    f.write('')

def generate(i, word, word_type, gender, aspect, comparable):
    with io.open('output.txt', 'a', encoding = 'utf8') as f:
        f.write(str(i) + ': ' + word + ' (')
        
        if word_type == 'noun':
            f.write(model['noun']['name'] + ', ' + model['noun'][gender]['name'] + '):\n')
            ending = '-' + word[-3:]
            if ending in model['noun'][gender]:
                for number in model['noun'][gender][ending]:
                    f.write('\t' + number + ':\n')
                    for declension in model['noun'][gender][ending][number]:
                        f.write('\t\t' + declension + ':\n\t\t\t' + word[:-3] + model['noun'][gender][ending][number][declension][1:] + '\n')
                
        elif word_type == 'verb':
            f.write(model['verb']["name"] + ', ')
            ending = '-' + word[-2:]
            if ending in model['verb']:
                f.write(model['verb'][ending][aspect]['name'] + ', ' + model['verb'][ending]["name"] + '):\n')
                for form in model['verb'][ending][aspect]:
                    if form == 'name':
                        continue
                    elif isinstance(model['verb'][ending][aspect][form], str):
                        f.write('\t' + form + ':\n' + '\t\t' + word[:-2] + model['verb'][ending][aspect][form][1:] + '\n')
                    else:
                        f.write('\t' + form + ':\n')
                        for declension in model['verb'][ending][aspect][form]:
                            f.write('\t\t' + declension + ':\n\t\t\t' + word[:-2] + model['verb'][ending][aspect][form][declension][1:] + '\n')
        elif word_type == 'adjective':
            f.write(model['adjective']["name"] + '):\n')
            ending = '-' + word[-2:]
            if ending in model['adjective']:
                for declension in model['adjective'][ending]["non comparable"]:
                    f.write('\t\t' + declension + ':\n\t\t\t' + word[:-2] + model['adjective'][ending]["non comparable"][declension][1:] + '\n')
                if comparable:
                    for degree in model['adjective'][ending]["comparable"]:
                        f.write('\t' + degree + ':\n')
                        for declension in model['adjective'][ending]["comparable"][degree]:
                            f.write('\t\t' + declension + ':\n\t\t\t' + model['adjective'][ending]["comparable"][degree][declension].replace('-', word[:-2]) + '\n')

        f.write('\n\n')


parameter = False
word_sequence = False

word_type = None
gender = None
aspect = None
comparable = None

i = 0
word = ''
word_type = ''

for e in words:

    if parameter:
        if word_type == 'noun':
            if e == 'm':
                gender = 'masculine'
            elif e == 'f':
                gender = 'feminine'
            elif e == 'n':
                gender = 'neuter'
        if word_type == 'verb':
            if e == 'i':
                aspect = 'imperfective'
            elif e == 'p':
                aspect = 'perfective'
        if word_type == 'adjective':
            if e == 'c':
                comparable = True
            elif e == 'n':
                comparable = False
        parameter = False

    elif e == '-':
        parameter = True

    elif e == '"':
        if not word_sequence:
            word = ''
        else:
            print('Generowanie form dla wyrazu "' + word + '"')
            if not word_type:
                print('Nie zdefioniowano typu wyrazu')
            if word == '':
                print('Brak wyrazu')
            i += 1
            generate(i, word, word_type, gender, aspect, comparable)
            word_type = None
            gender = None
            aspect = None
            comparable = None
        word_sequence = not word_sequence

    elif word_sequence:
        word += e

    elif e == 'n':
        word_type = 'noun'
    elif e == 'v':
        word_type = 'verb'
    elif e == 'a':
        word_type = 'adjective'

input("\n\nPress the enter key to exit.")
