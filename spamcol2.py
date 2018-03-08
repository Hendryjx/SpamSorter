
def main():
    """ Konverterar input-filen till lista där varje element är ett brev """
    """ Anropar sedan granskningsfunktionen med brevlistan som parameter """
    print('\nWelcome! You will now be asked to enter 3 files.\n\n' + 'Please enter email file for spam check:')
    email_list_input = main_file_check()
    mail_list = email_list_input.read().split('---')
    print('\nPlease enter file for clean email:')
    clean_mail = input_check()
    print(clean_mail)
    print('\nPlease enter file for spam email:')
    junk_mail = input_check()

    with open('ordlista.txt') as junk_words:
        junk_wordlist = [line.strip() for line in junk_words]

    junk_check(mail_list, clean_mail, junk_mail, junk_wordlist)

def main_file_check():
    while True:
        try:
            prompt = open(input('>>> '))
        except IOError:
            print('File does not exist on drive. Try again:')
            continue
        else:
            return prompt

def input_check():
    while True:
        try:
            file_name = input('>>> ')
            file_exist = open(file_name)
            file_exist = file_exist.close()
            return file_name
        except IOError:
            print('File does not exist on drive.')
            continue
        else:
            break

def spam_limit_check():
    print('\nSet spam sensitivity. Press enter for default value (12) or enter a value of your choice.')
    while True:
        spam_value = int(input('\nSpam limit: ') or '12')
        if spam_value < 4:
            print('Number is too small, enter value higher than 4.')
        else:
            return spam_value

def junk_check(mail_list, clean_mail, junk_mail, junk_wordlist):
    mail_counter = -1
    spam_counter = 0
    spam_limit = int(spam_limit_check())
    for mail in mail_list:
        spam_info = []
        junk_points = 0
        mail_counter += 1
        for junkword in junk_wordlist:
            if mail.count(junkword) > 0:
                junk_points += 4*mail.count(junkword)
                spam_info.append(junkword + ' ' + str(4*mail.count(junkword)) + 'p')
        if not collector(junk_points, spam_limit, mail, junk_mail, clean_mail, spam_info):
            spam_counter += 1

    print('Out of total ' + str(mail_counter) + ' emails:')
    print('Found ' + str(spam_counter) + ' spam emails', '(see ' + junk_mail + ')')
    print('Found ' + str(mail_counter - spam_counter) + ' clean emails', '(see ' + clean_mail + ')\n')

def collector(junk_points, spam_limit, mail, junk_mail, clean_mail, spam_info):
    if junk_points >= spam_limit:
        with open(junk_mail, 'a') as out:
            out.write(mail + '---\n')
        spam_print(spam_info, junk_points)
        return False
    else:
        with open(clean_mail, 'a') as out:
            out.write(mail + '---\n')

def spam_print(spam_info, junk_points):
    print('\n' + 'SPAM ' + str(junk_points) + 'p:')
    print('\n'.join(spam_info) + '\n')

main()
