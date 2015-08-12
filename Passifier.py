from getpass import getpass
from hashlib import sha256
from random import SystemRandom

RAND_RANGE = 100
DELIM = ':'
DICT_FILE = 'dictionary'


def gen_password(numbers_taken, factors=None):
    if factors:
        master_password = factors['master']
        site_name = factors['site']
        number = None
    else:
        master_password = getpass('Master password: ')
        master_password_confirm = getpass('Conform master password: ')

        while master_password != master_password_confirm:
            print('Confirmation did not match. Try again.')
            master_password = getpass('Master password: ')
            master_password_confirm = getpass('Confirm master password: ')

        site_name = input('Site name (case insensitive): ').lower()

        number = input('number to recalc a password, or enter to calc new one: ')

    number = int(number) if number else roll_new_number(numbers_taken)
    numbers_taken.add(number)

    the_hash = gen_hash(master_password, site_name, number)
    password = hash_to_pass(the_hash) + ':' + str(number)

    return password, {'master': master_password, 'site': site_name, 'number': number}


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


def roll_new_number(numbers_taken):
    crypto_generator = SystemRandom()
    roll = crypto_generator.randrange(RAND_RANGE)
    while roll in numbers_taken:
        roll = crypto_generator.randrange(RAND_RANGE)
    return roll


if __name__ == '__main__':
    numbers_taken = set()
    password, factors = gen_password(numbers_taken)

    print('Your password: ' + password)
    all_done = input('happy? (if no, will reroll) y/n: ')
    while all_done != 'y':
        password, factors = gen_password(numbers_taken, factors=factors)
        print('Your password: ' + password)
        if len(numbers_taken) == RAND_RANGE:
            print('used up all ' + str(RAND_RANGE) + ' passwords.')
            quit()
        all_done = input('happy? (if no, will reroll) y/n: ')
