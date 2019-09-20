import json


def load_data(filepath):
    with open(filepath, "r", encoding="utf8") as file:
        return json.loads(file.read())


def get_biggest_bar(data):
    sizes_list = list(map(get_size, data))
    biggest_size = max(sizes_list)
    biggest_bar_id = sizes_list.index(biggest_size)
    return biggest_bar_id


def get_smallest_bar(data):
    sizes_list = list(map(get_size, data))
    smallest_size = min(sizes_list)
    smallest_bar_id = sizes_list.index(smallest_size)
    return smallest_bar_id


def get_closest_bar(data, longitude, latitude):
    get_distance = lambda c: ((c[0]-longitude)**2 + (c[1]-latitude)**2)**0.5
    coordinates_list = list(map(get_coordinates, data))
    distances_list = list(map(get_distance, coordinates_list))
    smallest_distance = min(distances_list)
    closest_bar_id = distances_list.index(smallest_distance)
    return closest_bar_id


if __name__ == '__main__':
    filepath = "bars.json"
    json_content = load_data(filepath)
    bars = json_content.get("features")
    get_name = lambda bar: bar.get("properties").get("Attributes").get("Name")
    get_size = lambda bar:\
        bar.get("properties").get("Attributes").get("SeatsCount")
    get_coordinates = lambda bar: bar.get("geometry").get("coordinates")
    names_list = list(map(get_name, bars))

    print('Самый большой бар: ', names_list[get_biggest_bar(bars)])
    print('Самый маленький бар: ', names_list[get_smallest_bar(bars)])

    longitude = float(input('Введите долготу: '))  # Например, 37.62
    latitude = float(input('Введите широту: '))  # Например, 55.76

    print('Ближайший бар: ',
        names_list[get_closest_bar(bars, longitude, latitude)])
