import json

from flask_caching import Cache
import redis

cache = redis.Redis(host='redis', port=6379)


def get_soil_key(id):
    return str(id) + '.json'

def get_user_records(user_id):

    data = get_cache(user_id)

    return data


def get_soil_records(user_id):
    return get_cache(user_id)

def store_soil(soil):

    set_cache(
        soil.user_id,
        soil.to_dict()
    )


def get_cache(key):
    try:
        with open('store/data.json', 'r+') as file:
            # First we load existing data into a dict.
            file_data = json.load(file)

            data = []

            for dat in file_data[key]:

                dat = json.loads(dat)

                dat['predictions'] = json.loads(dat['predictions'])

                data.append(
                    dat
                )

            return data

    except:
        return []
    # return cache.get(key)


# function to add to JSON
def write_data(key, data):
    with open('store/data.json', 'r+') as file:
        # First we load existing data into a dict.
        file_data = json.load(file)
        # Join new_data with file_data inside emp_details
        if key in file_data:
            file_data[key].append(data)
        else:
            file_data[key] = [
                data
            ]
        # Sets file's current position at offset.
        file.seek(0)
        # convert back to json.
        json.dump(file_data, file, indent=4)


def set_cache(key, data):
    write_data(key, data)