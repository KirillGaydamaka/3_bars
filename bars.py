import json
import argparse
import os


def load_data(filepath):
    if not os.path.exists(filepath):
        return None
    try:
        with open(filepath, 'r', encoding='utf8') as file:
            return json.loads(file.read()).get('features')
    except json.decoder.JSONDecodeError:
        return None


def get_biggest_bar(bars):
    biggest_bar = max(bars, key=get_bar_size)
    return biggest_bar


def get_smallest_bar(bars):
    smallest_bar = min(bars, key=get_bar_size)
    return smallest_bar


def get_closest_bar(bars, longitude, latitude):
    def get_bar_distance(bar):
        coord = bar.get('geometry').get('coordinates')
        return ((coord[0]-longitude)**2 + (coord[1]-latitude)**2)**0.5

    closest_bar = min(bars, key=get_bar_distance)
    return closest_bar


def get_bar_name(bar):
    return bar.get('properties').get('Attributes').get('Name')


def get_bar_size(bar):
    return bar.get('properties').get('Attributes').get('SeatsCount')


def get_user_coordinates():
    user_input = input('Введите координаты: ')
    try:
        longitude, latitude = map(float, user_input.split())
    except ValueError:
        print('Некорректный ввод')
        quit()
    return longitude, latitude


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Find the closest bar')
    parser.add_argument('filepath', nargs='?', default='bars.json',
                        help='An optional filepath')
    args = parser.parse_args()
    filepath = args.filepath

    bars = load_data(filepath)
    if bars is None:
        print('Не удалось загрузить данные')
        exit()

    biggest_bar = get_biggest_bar(bars)
    print('Самый большой бар: ', get_bar_name(biggest_bar))

    smallest_bar = get_smallest_bar(bars)
    print('Самый маленький бар: ', get_bar_name(smallest_bar))

    longitude, latitude = get_user_coordinates()

    closest_bar = get_closest_bar(bars, longitude, latitude)
    print('Ближайший бар: ', get_bar_name(closest_bar))
