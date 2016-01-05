#!/usr/local/bin/python3

import argparse
from getpass import getpass
from hashlib import sha256
from random import SystemRandom

RAND_RANGE = 100  # Range of numbers to randomly select an ID
DELIM = ':'  # The deliminator used in hashing and output.  Change if password requirements demand some exotic char.
DICT_FILE = 'dictionary'  # Location of the file containing newline-delimited words making up the dictionary.

numbers_available = set(range(RAND_RANGE))


def gen_password(hash, number):
    return hash_to_pass(hash) + DELIM + str(number)


def gen_hash(master_password, site_name, number):
    combined = master_password + DELIM + site_name + DELIM + str(number)
    return sha256(combined.encode('utf-8')).hexdigest()


def hash_to_pass(hash):
    dictionary = open(DICT_FILE, 'r')
    word_list = dictionary.readlines()
    dict_len = len(word_list)

    chunk_size = int(len(hash) / 3)
    assert chunk_size >= 3, "hash not large enough."

    first_chunk = hash[0:chunk_size]
    second_chunk = hash[chunk_size:chunk_size * 2]
    third_chunk = hash[chunk_size * 2:chunk_size * 3]

    first_index = int(first_chunk, 16) % dict_len
    second_index = int(second_chunk, 16) % dict_len
    third_index = int(third_chunk, 16) % dict_len

    result = word_list[first_index].rstrip().capitalize() + word_list[second_index].rstrip().capitalize() + word_list[
        third_index].rstrip().capitalize()
    dictionary.close()
    return result


def roll_new_number():
    global numbers_available
    crypto_generator = SystemRandom()
    number = crypto_generator.choice(list(numbers_available))
    numbers_available.remove(number)
    return number


def print_password(password):
    print("\nYour password is:")
    print("=================")
    print(password)
    print("=================")


def parse_args():
    parser = argparse.ArgumentParser(description='Deterministically generate passwords.')
    parser.add_argument('website', nargs='?')
    parser.add_argument('number', nargs='?', type=int)
    args = parser.parse_args()

    if bool(args.number) != bool(args.website):  # if one var is set but not the other
        parser.print_usage()
        print("I need both the website and the number to recompute a password.")
        quit()

    return args.website, args.number


def ask_for_details():
    master = ask_for_master()

    website = input('Website: ')

    number = input('Number (leave empty to generate): ')
    assert number == '' or number.isdigit(), 'Number must be empty or a digit.'

    if number == '':
        number = roll_new_number()

    return master, website, number


def ask_for_master():
    master = None

    while True:
        master = getpass('Master password: ')
        confirm = getpass('Confirm: ')

        if master == confirm:
            break
        else:
            print("Confirmation didn't match.  Try again.")

    return master


def main():
    args = parse_args()

    master, website, number = None, None, None

    if all(args):  # if the user included details in args
        website, number = args[0], args[1]
        master = ask_for_master()

        hash = gen_hash(master, website, number)
        password = gen_password(hash, number)
        print_password(password)
        print()
        return  # nothing left to do

    else:  # otherwise we must ask for those details
        master, website, number = ask_for_details()

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

        number = roll_new_number()


if __name__ == '__main__':
    main()
