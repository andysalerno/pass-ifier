#!/usr/local/bin/python3

from getpass import getpass
from hashlib import sha256
from random import SystemRandom

RAND_RANGE = 100
DELIM = ':'
DICT_FILE = 'dictionary'


def gen_password(numbers_available, factors=None):
    pass


def gen_hash(master_password, site_name, number):
    combined = master_password + DELIM + site_name + DELIM + str(number)
    return sha256(combined.encode('utf-8')).hexdigest()


def hash_to_pass(the_hash):
    dictionary = open(DICT_FILE, 'r')
    word_list = dictionary.readlines()
    dict_len = len(word_list)

    first_chunk = the_hash[0:6]
    second_chunk = the_hash[6:12]
    third_chunk = the_hash[12:18]

    first_index = int(first_chunk, 16) % dict_len
    second_index = int(second_chunk, 16) % dict_len
    third_index = int(third_chunk, 16) % dict_len

    result = word_list[first_index].rstrip().capitalize() + word_list[second_index].rstrip().capitalize() + word_list[
        third_index].rstrip().capitalize()
    dictionary.close()
    return result


def roll_new_number(numbers_available):
    crypto_generator = SystemRandom()
    number = crypto_generator.choice(list(numbers_available))
    numbers_available.remove(number)
    return number


def main():
    master = None
    while True:
        master = getpass('Master password: ')
        confirm = getpass('Confirm: ')

        if master == confirm:
            break
        else:
            print('Try again.')

    website = getpass('Website: ')  # todo: have arg to make sitename getpass or not getpass

    number = getpass('Number (leave empty to generate): ')
    assert len(number) == 0 or number.isdigit(), 'Number must be empty or a digit.'

    hash = gen_hash(master, website, 9)



if __name__ == '__main__':
    main()
