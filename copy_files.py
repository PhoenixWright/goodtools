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
        shutil.copy(file, target_directory)

if __name__ == '__main__':
    copy_files('file_list.json')
