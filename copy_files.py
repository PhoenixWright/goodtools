import logging
import sys
import os
import shutil
import json

log = logging.getLogger('goodtools')
log.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
log.addHandler(ch)

working_directory = sys.argv[1]
log.info('Extracting items from directory: {}'.format(working_directory))

target_directory = working_directory + '/a'

try:
    os.stat(target_directory)
    log.info('Clearing out old target directory: {}'.format(target_directory))
    shutil.rmtree(target_directory)
except:
    log.debug('No existing target directory.')

log.info('Creating target directory: {}'.format(target_directory))
os.mkdir(target_directory)


def read_json(file_name):
    with open(file_name) as json_file:
        json_data = json.load(json_file)
        return json_data


def copy_files(file_name):
    json_data = read_json(file_name)

    file_list = json_data['files']
    #log.debug(file_list)

    log.info('Copying {} files.'.format(len(file_list)))

    for file in file_list:
        log.debug('Copying {}...'.format(os.path.basename(file)))
        extension = os.path.splitext(file)[1]

        updated_name = os.path.basename(file)\
            .replace(extension, '')\
            .replace('(U)', '')\
            .replace('(E)', '')\
            .replace('[!]', '')\
            .replace('[U]', '')\
            .replace('[E]', '')\
            .replace('(PRG1)', '')\
            .replace('(PRG2)', '') \
            .replace('(REV01)', '') \
            .replace('(REV02)', '') \
            .replace('(REVA)', '')\
            .replace('(REVB)', '')\
            .replace('[b1]', '')\
            .replace('[b1+C]', '')\
            .replace('[b2]', '')\
            .replace('(V1.0)', '')\
            .replace('(V1.1)', '') \
            .replace('(V1.2)', '') \
            .replace('(M1)', '') \
            .replace('(M2)', '') \
            .replace('(M3)', '') \
            .replace('(M4)', '') \
            .replace('(M5)', '') \
            .replace('(M6)', '') \
            .replace('(M7)', '') \
            .replace('(M8)', '') \
            .strip() + extension

        if ', The' in updated_name:
            updated_name = updated_name.replace(', The', '')
            updated_name = 'The ' + updated_name

        target_path = target_directory + '/' + updated_name
        shutil.copyfile(file, target_path)

if __name__ == '__main__':
    copy_files('file_list.json')
