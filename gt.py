import logging
import sys
import os
import shutil

logger = logging.getLogger('goodtools')
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
logger.addHandler(ch)

working_directory = sys.argv[1]
logger.info('Extracting items from directory: {}'.format(working_directory))

target_directory = working_directory + '/a'

try:
    os.stat(target_directory)
    logger.info('Clearing out old target directory: {}'.format(target_directory))
    shutil.rmtree(target_directory)
except:
    logger.debug('No existing target directory.')

logger.info('Creating target directory: {}'.format(target_directory))
os.mkdir(target_directory)

directory_names = [d[0] for d in os.walk(working_directory)]

unambiguous_names = []
ambiguous_names = []
unlicensed_names = []

locale_priority = [
    '(U) [!]',
    '(U) (PRG2) [!]',
    '[U][!]',
    '(E) [!]',
    '(JU) [!]',
    '(J) [!]',
    '(Ch) [!]',
    '(U).',
    '(E).',
    '(JU).',
    '(J).',
    '(R).',
    '(Ch).',
    '[p2][!]',
    '(Prototype2) [!]',
    '(Prototype2).',
    '(Prototype1) [!]',
    '(Prototype1).',
    '[!]'
]


for directory_name in directory_names:
    file_names = os.listdir(directory_name)

    # if the whole directory is unlicensed, just take all the files
    if all('(Unl)' in x for x in file_names):
        file_names.append('')
        unlicensed_names.extend(file_names)
        continue

    final_name = None

    for locale in locale_priority:
        locale_and_exclamation_files = []
        for file_name in file_names:
            ###
            # if 'Prototype' in file_name:
            # logger.debug('prototype: {}'.format(file_name))
            ###
            if locale in file_name:
                locale_and_exclamation_files.append(file_name)

        if len(locale_and_exclamation_files) == 0:
            continue
        elif len(locale_and_exclamation_files) == 1:
            final_name = file_name
            break

    if final_name:
        unambiguous_names.append(directory_name + '/' + file_name)
    else:
        ambiguous_names.append(directory_name)

logger.debug('Automatically detected {} of {} files.'.format(len(unambiguous_names), len(directory_names)))
logger.debug('{} of {} files need manual selection.'.format(len(ambiguous_names), len(directory_names)))

from IPython import embed; embed()
