#!/usr/local/bin/python3

from getpass import getpass
from hashlib import sha256
from random import SystemRandom

RAND_RANGE = 100  # Range of numbers to randomly select an ID
DELIM = ':'  # The deliminator used in hashing and output.  Change if password requirements demand some exotic char.
DICT_FILE = 'dictionary'  # Location of the file containing newline-delimited words making up the dictionary.


def gen_password(hash, number):
    return hash_to_pass(hash) + DELIM + str(number)


def gen_hash(master_password, site_name, number):
    combined = master_password + DELIM + site_name + DELIM + str(number)
    return sha256(combined.encode('utf-8')).hexdigest()


def hash_to_pass(hash):
    dictionary = open(DICT_FILE, 'r')
    word_list = dictionary.readlines()
    dict_len = len(word_list)

    first_chunk = hash[0:6]
    second_chunk = hash[6:12]
    third_chunk = hash[12:18]

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


def print_password(password):
    print("Your password is:")
    print("=================")
    print(password)
    print("=================")


def main():
    master = None
    numbers_available = set(range(RAND_RANGE))

    while True:
        master = getpass('Master password: ')
        confirm = getpass('Confirm: ')

        if master == confirm:
            break
        else:
            print("Confirmation didn't match.  Try again.")

    website = input('Website: ')

    number = input('Number (leave empty to generate): ')
    assert number == '' or number.isdigit(), 'Number must be empty or a digit.'

    if number == '':
        number = roll_new_number(numbers_available)

    while True:
        hash = gen_hash(master, website, number)
        password = gen_password(hash, number)
        print_password(password)
        redo = input('Reroll? y/n: ')

        if redo.lower() == 'n':
            break

        if len(numbers_available) == 0:
            print('Exhausted number range.')
            break

        number = roll_new_number(numbers_available)


if __name__ == '__main__':
    main()
