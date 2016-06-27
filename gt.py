import logging
import sys
import os
import shutil
import json

from collections import OrderedDict

logger = logging.getLogger('goodtools')
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
logger.addHandler(ch)

working_directory = sys.argv[1]
logger.info('Extracting items from directory: {}'.format(working_directory))

directory_names = [d[0] for d in os.walk(working_directory)]

unambiguous_names = []
ambiguous_names = []
unlicensed_names = []

locale_priority = [
    ['(U)', '[!]'],
    ['(E)', '[!]']
    #'(U) [!]',
    #'(U) (PRG2) [!]',
    #'[U][!]',
    #'(E) [!]',
    #'(JU) [!]',
    #'(J) [!]',
    #'(Ch) [!]',
    #'(U).',
    #'(E).',
    #'(JU).',
    #'(J).',
    #'(R).',
    #'(Ch).',
    #'[p2][!]',
    #'(Prototype2) [!]',
    #'(Prototype2).',
    #'(Prototype1) [!]',
    #'(Prototype1).',
    #'[!]'
]


for directory_name in directory_names[1:]:
    file_names = os.listdir(directory_name)

    # if the whole directory is unlicensed, just take all the files
    #if all('(Unl)' in x for x in file_names):
    #    for file_name in file_names:
    #        unlicensed_names.append(directory_name + '/' + file_name)
    #    continue

    final_name = None

    locales_not_matched_count = 0

    for locale in locale_priority:
        locale_and_exclamation_files = []
        for file_name in file_names:
            ###
            # if 'Prototype' in file_name:
            # logger.debug('prototype: {}'.format(file_name))
            ###
            all_in = True
            for piece in locale:
                all_in = all_in and piece in file_name
            if all_in:
                locale_and_exclamation_files.append(file_name)

        if len(locale_and_exclamation_files) == 0:
            #logger.debug('locale {} not found at all for directory'.format(locale, directory_name))
            locales_not_matched_count += 1
            continue
        elif len(locale_and_exclamation_files) == 1:
            final_name = locale_and_exclamation_files[0]
            #logger.debug('Locale for {}: {}'.format(directory_name, locale))
            break
        else:
            break

    if locales_not_matched_count == len(locale_priority):
        continue

    if final_name:
        unambiguous_names.append(directory_name + '/' + final_name)
    else:
        ambiguous_names.append(directory_name)

        choices = OrderedDict({
            'n': 'none',
            'a': 'all'
        })

        for idx, file_name in enumerate(file_names):
            choices[str(idx)] = file_name

        message = ''
        for key, value in choices.items():
            message += key + ' - ' + value + '\n'

        choice = None
        while True:
            user_input = input(message)
            #logger.debug('got user input: {}'.format(user_input))
            if user_input in choices:
                choice = choices[user_input]
                break

        if choice == 'none':
            logger.debug('Continuing without adding any roms from {}.'.format(directory_name))
            continue
        elif choice == 'all':
            logger.debug('Adding all roms from {}.'.format(directory_name))
            for name in file_names:
                unambiguous_names.append(directory_name + '/' + name)
        else:
            logger.debug('Adding {}.'.format(choice))
            unambiguous_names.append(directory_name + '/' + choice)

logger.debug('Automatically detected {} of {} files.'.format(len(unambiguous_names), len(directory_names)))
logger.debug('{} of {} files need manual selection.'.format(len(ambiguous_names), len(directory_names)))

# include the unlicensed names
unambiguous_names.extend(unlicensed_names)

for name in unambiguous_names:
    logger.debug(name)

# create json to document all the file names we want
file_json = {
    'files': unambiguous_names
}

# back up the file names in case shit goes wrong
with open('file_list.json', 'w') as output_file:
    json.dump(file_json, output_file)

#from IPython import embed; embed()
