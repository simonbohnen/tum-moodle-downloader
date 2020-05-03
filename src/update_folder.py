import os
import json
import course_retrieval


def update_folder(session, path):
    # get config json
    config_file = None
    for file in os.listdir(path):
        if file.endswith('.json'):
            config_file = file
            break
    if config_file is None:
        # TODO perhaps search for shell script
        return
    config_path = os.path.join(path, config_file)

    # parse json
    with open(config_path, 'r') as f:
        config_data = json.load(f)
        try:
            course_name = config_data['name']
            rules = config_data['rules']
            course = course_retrieval.get_course(session, course_name)
            download_files(course, rules)
        except KeyError:
            print('Check json file')
            return


# download resources and save them where rule specifies
def download_files(course, rules):
    for rule in rules:
        try:
            pattern = rule['pattern']
            path = rule['path']
        except KeyError:
            print('Check rule format')
            continue
        course.download_resources(pattern, path)
