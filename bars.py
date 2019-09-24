import json
import argparse

def load_data(filepath):
    with open(filepath, 'r', encoding='utf8') as file_handler:
        return json.loads(file_handler.read())


def get_biggest_bar(bars):
    sizes_list = list(map(get_bar_size, bars))
    biggest_size = max(sizes_list)
    biggest_bar_id = sizes_list.index(biggest_size)
    return biggest_bar_id


def get_smallest_bar(bars):
    sizes_list = list(map(get_bar_size, bars))
    smallest_size = min(sizes_list)
    smallest_bar_id = sizes_list.index(smallest_size)
    return smallest_bar_id


def get_closest_bar(bars, longitude, latitude):
    coordinates_list = list(map(get_bar_coordinates, bars))
    distances_list = list(map(get_distance, coordinates_list))
    smallest_distance = min(distances_list)
    closest_bar_id = distances_list.index(smallest_distance)
    return closest_bar_id


def get_bar_name(bar):
    return bar.get('properties').get('Attributes').get('Name')


def get_bar_size(bar):
    return bar.get('properties').get('Attributes').get('SeatsCount')


def get_bar_coordinates(bar):
    return bar.get('geometry').get('coordinates')


def get_distance(coordinates):
    return ((coordinates[0]-longitude)**2 + (coordinates[1]-latitude)**2)**0.5



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Find the closest bar')
    parser.add_argument('filepath', nargs='?', default='bars.json',
                    help='An optional filepath')
    args = parser.parse_args()
    filepath = args.filepath

    bars = load_data(filepath).get('features')

    names_list = list(map(get_bar_name, bars))

    print('Самый большой бар: ', names_list[get_biggest_bar(bars)])
    print('Самый маленький бар: ', names_list[get_smallest_bar(bars)])

    longitude = float(input('Введите долготу: '))  # Например, 37.62
    latitude = float(input('Введите широту: '))  # Например, 55.76

    print(
        'Ближайший бар: ',
        names_list[get_closest_bar(bars, longitude, latitude)])
