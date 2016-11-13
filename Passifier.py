#!/usr/bin/env python3
from getpass import getpass
from hashlib import pbkdf2_hmac, sha256
from random import SystemRandom

DICT_FILE = 'dictionary'  # relative path to the dictionary file
MAX_NUM = 99  # maximum value for number element
ITERATIONS = 100000  # amount of pbkdf2_hmac iterations to perform
WORDS = 4  # amount of words to pick from dictionary


def key_to_password(key, dictionary, number):
    password = ''
    for _ in range(WORDS):
        sha = sha256()
        sha.update(key)
        key = sha.digest()
        index = int.from_bytes(key, 'big') % len(dictionary)
        password += str(dictionary[index], 'utf-8').strip().capitalize()

    password += '!{}'.format(number)

    return password


def gen_dictionary_identifier(dictionary):
    sha = sha256()
    for word_bytes in dictionary:
        sha.update(word_bytes)
    index = int.from_bytes(sha.digest(), 'big') % len(dictionary)
    return str(dictionary[index].strip(), 'utf-8')


def open_dictionary():
    try:
        dictionary = open(DICT_FILE, 'rb')
        return dictionary.readlines()
    except:
        print('Error opening dictionary file {}'.format(DICT_FILE))
        quit()


def prompt_user():
    while True:
        master_pw = getpass('Master password: ')
        confirm_pw = getpass('Confirm password: ')

        if master_pw != confirm_pw:
            print('Confirmation didn\'t match.  Try again.')
        else:
            break

    service = input('Service name (e.g. facebook): ').lower()
    number = input('number (leave blank to generate): ')

    if number == '':
        number = SystemRandom().choice(range(MAX_NUM + 1))
    else:
        assert number.isdigit(), "Must enter a valid digit.  You entered: {}".format(number)
        number = int(number)
        assert 0 <= number <= MAX_NUM, "Number must be >= 0 and <= {}.  You entered: {}".format(
            str(MAX_NUM), str(number))

    return master_pw, service, number


def main():
    dictionary = open_dictionary()

    print('Dictionary size: {} words'.format(len(dictionary)))
    print('Dictionary Identifier: {}'.format(
        gen_dictionary_identifier(dictionary)))

    master_pw, service, number = prompt_user()
    combined = master_pw + str(number)
    key = pbkdf2_hmac('sha256', combined.encode(),
                      service.encode(), ITERATIONS)
    print(key_to_password(key, dictionary, number))

if __name__ == '__main__':
    main()
