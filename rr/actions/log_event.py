#!/usr/bin/env python3
#  Copyright (C) 2021 RidgeRun, LLC (http://www.ridgerun.com)
#  Authors: Daniel Chaves <daniel.chaves@ridgerun.com>
#           Marisol Zeledon <marisol.zeledon@ridgerun.com>

import csv
import threading


def log(path, media, image, inf_results, fieldnames):
    """ Logs the event to the logging file

    Parameters
    ----------
    path : str
        The path to the logging file
    media : media obj
        The media object
    image : image obj
        The image object
    inf_results : dict
        The inference results
    fieldnames : list
        The list with the file fieldnames
    """

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
    """ Finds the label with the highest probability

    Parameters
    ----------
    labels : list
        A list with the inference result labels
    """

    first_label = labels[0]
    label_max_prob = first_label
    for label in labels:
        if label['probability'] > label_max_prob['probability']:
            label_max_prob = label
    return label_max_prob


def validate_csv(path):
    """ Validates that the file is a csv file

    Parameters
    ----------
    path : str
        The path to the csv file

    Raises
    ------
    LogEventError
        If the file is not a csv file
    """

    if path.endswith('.csv'):
        return path
    else:
        raise LogEventError(
            "The file used for logging must have a .csv file extension")


def set_file_headers(path):
    """ Sets the headers for the logging file

    Parameters
    ----------
    path : str
        The path to the csv file
    """

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


class LogEvent():
    """
    Class that loggs events to a file

    Attributes
    ----------
    _path: string
        A private string with the log file path
    _fieldnames: list
        A private list with the file's fieldnames
    _mutex: lock object
        A private lock to control file writing

    Methods
    -------
    execute(media : media obj, image: image obj, inf_results: dict)
        Execute the file logging
    """

    def __init__(self, path):
        """ Constructor for the Log Event object
        """

        self._path = validate_csv(path)
        self._fieldnames = set_file_headers(self._path)
        self._mutex = threading.Lock()

    def execute(self, media, image, inf_results):
        """ Executes the log action

        Parameters
        ----------
        media : media obj
            The media object
        image : image obj
            The image object
        inf_results : dict
            The inference results
        """

        self._mutex.acquire()
        log(self._path, media, image, inf_results, self._fieldnames)
        self._mutex.release()
