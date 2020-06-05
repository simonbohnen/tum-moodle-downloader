import json
import os
import sys
from getpass import getpass
import authentication
import course_retrieval
import argparse
import update_folder


def parse_args() -> dict:
    args = sys.argv[1:]
    if not args:
        print('Usage: python3 main.py [-l [course] | -d course file [path]]')
        exit(1)
    if args[0] == '-l':
        if len(args) > 1:
            return {'mode': 'list', 'course': args[1]}
        else:
            return {'mode': 'list', 'course': None}
    elif args[0] == '-d':
        if len(args) > 2:
            return {'mode': 'download', 'course': args[1], 'file': args[2], 'path': None}
        if len(args) > 3:
            return {'mode': 'download', 'course': args[1], 'file': args[2], 'path': args[3]}
    else:
        print('Usage: python3 main.py [-l | -d] [course] [file] [path]')
        exit(1)


def setup_credentials():
    credentials_path = os.path.join(sys.path[0], 'credentials.json')
    if os.path.isfile(credentials_path):
        with open(credentials_path, 'r') as f:
            config_data = json.load(f)
            try:
                os.environ['USERNAME'] = config_data['username']
                os.environ['PASSWORD'] = config_data['password']
            except KeyError:
                print('Check credentials.json file')
                exit(1)
    else:
        print('credentials.json file not found. Setting up new credentials.json file...')
        config_data = {
            "username": input('Enter username or email (e.g. go42tum/example@tum.de)\n'),
            "password": getpass('Enter password: '),
        }
        os.environ['USERNAME'] = config_data['username']
        os.environ['PASSWORD'] = config_data['password']
        config_json = json.dumps(config_data)
        with open(credentials_path, 'w') as f:
            f.write(config_json)


if __name__ == "__main__":
    # arguments = parse_args()
    # parser = argparse.ArgumentParser(description="Download files from the TUM Moodle.")
    # parser.add_argument('-r', '--recursive', help='Recursively update all subdirectories.')

    setup_credentials()
    session = authentication.start_session(
        os.environ['USERNAME'],
        os.environ['PASSWORD']
    )
    if session is None:
        print('Could not start session.')
        exit(1)

    update_folder.update_folder(session, os.getcwd())

    # course_name = arguments['course']
    # course = None
    # if course_name is not None:
    #     course = course_retrieval.get_course(session, course_name)
    #     if course is None:
    #         print('Could not find course: ' + course_name)
    #         exit(1)
    #
    # if arguments['mode'] == 'list':
    #     if course_name is None:
    #         print('Listing available courses: ')
    #         course_retrieval.list_courses(session)
    #         exit(0)
    #     else:
    #         course.list_all_resources()
    #         exit(0)
    # elif arguments['mode'] == 'download':
    #     file = arguments['file']
    #     path = './' if arguments['path'] is None else arguments['path']
    #     course.download_resource(file, path)
