import os
import json
import random


def event_generator(count=None,
                    mandatory_types=set(), mandatory_keys=set(), mandatory_values={},
                    restricted_types=set(), restricted_keys=set(), restricted_values={},
                    log=True, shuffle=True):
    data_folder = 'events'
    cur_count = 0
    filenames = os.listdir(data_folder)
    if shuffle:
        random.shuffle(filenames)
    for filename in filenames:
        if log:
            print(f'Event generator: started reading from {filename}')
        with open(os.path.join(data_folder, filename), 'r', encoding='utf-8') as file:
            for line in file:
                event = json.loads(line)
                keys = event.keys()
                conditions = []
                conditions.append(not mandatory_types or event['type']['displayName'] in mandatory_types)
                conditions.append(not mandatory_keys or mandatory_keys.issubset(keys))
                conditions.append(not mandatory_values or all([event.get(k) == v for k, v in mandatory_values.items()]))
                conditions.append(not restricted_types or event['type']['displayName'] not in restricted_types)
                conditions.append(not restricted_keys or restricted_keys.isdisjoint(keys))
                conditions.append(
                    not restricted_values or all([event.get(k) != v for k, v in restricted_values.items()]))
                if all(conditions):
                    yield event
                    cur_count += 1
                    if count and cur_count == count:
                        if log:
                            print(f'Event generator: finished reading {count} events')
                        return
        if log:
            print(f'Event generator: finished reading from {filename}')


if __name__ == '__main__':
    e = event_generator(shuffle=False)
    for x, y in enumerate(e):
        if x and not x % 1000000:
            print(f'{x} done')
    print(x)
