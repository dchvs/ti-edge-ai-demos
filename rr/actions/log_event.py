#!/usr/bin/env python3
#  Copyright (C) 2021 RidgeRun, LLC (http://www.ridgerun.com)
#  Authors: Daniel Chaves <daniel.chaves@ridgerun.com>
#           Marisol Zeledon <marisol.zeledon@ridgerun.com>

import csv
import threading


def log(path, media, image, inf_results, fieldnames):
    media_name = media.get_name()
    image_time = image.get_timestamp()

    f = open(path, 'a', newline='')
    csv_writer = csv.DictWriter(f, fieldnames=fieldnames)
    for instance in inf_results['instances']:
        label_max = find_max_probability(instance['labels'])
        csv_writer.writerow({'name': media_name,
                             'time': image_time,
                             'label': label_max['label'],
                             'probability': label_max['probability'],
                             'bbox-x': instance['bbox']['x'],
                             'bbox-y': instance['bbox']['y'],
                             'bbox-width': instance['bbox']['width'],
                             'bbox-height': instance['bbox']['height']})


def find_max_probability(labels):
    first_label = labels[0]
    label_max_prob = first_label
    for label in labels:
        if label['probability'] > label_max_prob['probability']:
            label_max_prob = label
    return label_max_prob


def validate_csv(path):
    if path.endswith('.csv'):
        return path
    else:
        raise LogEventError(
            "The file used for logging must have a .csv file extension")


def set_file_headers(path):
    fieldnames = [
        'name',
        'time',
        'label',
        'probability',
        'bbox-x',
        'bbox-y',
        'bbox-width',
        'bbox-height']
    with open(path, 'w', newline='') as f:
        csv_writer = csv.DictWriter(f, fieldnames=fieldnames)
        csv_writer.writeheader()
        return fieldnames


class LogEventError(RuntimeError):
    pass


class LogEvent:
    def __init__(self, path):
        self._path = validate_csv(path)
        self._fieldnames = set_file_headers(self._path)
        self._mutex = threading.Lock()

    def execute(self, media, image, inf_results):
        self._mutex.acquire()
        log(self._path, media, image, inf_results, self._fieldnames)
        self._mutex.release()
