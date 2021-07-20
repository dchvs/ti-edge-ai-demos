#!/usr/bin/env python3
#  Copyright (C) 2021 RidgeRun, LLC (http://www.ridgerun.com)
#  Authors: Daniel Chaves <daniel.chaves@ridgerun.com>
#           Marisol Zeledon <marisol.zeledon@ridgerun.com>

import csv


def log(path, media, image, inf_results):
    with open(path, 'a', newline='') as f:
        pass


def validate_csv(path):
    if path.endswith('.csv'):
        return path
    else:
        raise LogEventError(
            "The file used for logging must have a .csv file extension")


def set_file_headers(path):
    with open(path, 'w', newline='') as f:
        pass


class LogEventError(RuntimeError):
    pass


class LogEvent:
    def __init__(self, path):
        self._path = validate_csv(path)

    def execute():
        pass
