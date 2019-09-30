import json
import argparse
import os


class DataValidationException(Exception):
    pass


def load_data(filepath):
    if not os.path.exists(filepath):
        return None
    try:
        with open(filepath, 'r', encoding='utf8') as file:
            return json.loads(file.read()).get('features')
    except json.decoder.JSONDecodeError:
        return None


def get_biggest_bar(bars):
    try:
        biggest_bar = max(bars, key=get_bar_size)
    except DataValidationException:
        return None
    return biggest_bar


def get_smallest_bar(bars):
    try:
        smallest_bar = min(bars, key=get_bar_size)
    except DataValidationException:
        return None
    return smallest_bar


def get_closest_bar(bars, longitude, latitude):
    def get_bar_distance(bar):
        bar_geometry = bar.get('geometry')
        if bar_geometry is None:
            raise DataValidationException('Bar has no geometry')
        coord = bar_geometry.get('coordinates')
        if coord is None:
            raise DataValidationException('Bar has no coordinates')
        return ((coord[0]-longitude)**2 + (coord[1]-latitude)**2)**0.5

    try:
        closest_bar = min(bars, key=get_bar_distance)
    except DataValidationException:
        return None
    return closest_bar


def get_bar_name(bar):
    bar_properties = bar.get('properties')
    if bar_properties is None:
        raise DataValidationException('Bar has no properties')
    bar_attributes = bar_properties.get('Attributes')
    if bar_attributes is None:
        raise DataValidationException('Bar has no attributes')
    bar_name = bar_attributes.get('Name')
    if bar_name is None:
        raise DataValidationException('Bar has no name')
    return bar_name


def get_bar_size(bar):
    bar_properties = bar.get('properties')
    if bar_properties is None:
        raise DataValidationException('Bar has no properties')
    bar_attributes = bar_properties.get('Attributes')
    if bar_attributes is None:
        raise DataValidationException('Bar has no attributes')
    bar_seatscount = bar_attributes.get('SeatsCount')
    if (bar_seatscount is None):
        raise DataValidationException('Bar has no seatscount')
    return bar_seatscount


def get_user_coordinates():
    user_input = input('Введите координаты: ')
    try:
        longitude, latitude = map(float, user_input.split())
    except ValueError:
        return None
    return longitude, latitude


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Find the closest bar')
    parser.add_argument('filepath', nargs='?', default='bars.json',
                        help='An optional filepath')
    args = parser.parse_args()
    filepath = args.filepath

    bars = load_data(filepath)
    if bars is None:
        exit('Не удалось загрузить данные')

    biggest_bar = get_biggest_bar(bars)
    if biggest_bar is None:
        exit('Некорректные данные')
    print('Самый большой бар: ', get_bar_name(biggest_bar))

    smallest_bar = get_smallest_bar(bars)
    if smallest_bar is None:
        exit('Некорректные данные')
    print('Самый маленький бар: ', get_bar_name(smallest_bar))

    user_coordinates = get_user_coordinates()
    if user_coordinates is None:
        exit('Некорректный ввод')

    longitude, latitude = user_coordinates
    closest_bar = get_closest_bar(bars, longitude, latitude)
    if closest_bar is None:
        exit('Некорректные данные')
    print('Ближайший бар: ', get_bar_name(closest_bar))
