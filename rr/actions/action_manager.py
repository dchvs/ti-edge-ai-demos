#!/usr/bin/env python3
#  Copyright (C) 2021 RidgeRun, LLC (http://www.ridgerun.com)
#  Authors: Daniel Chaves <daniel.chaves@ridgerun.com>
#           Marisol Zeledon <marisol.zeledon@ridgerun.com>

from rr.actions.log_event import LogEvent


class FilterError(RuntimeError):
    pass


class Filter:
    def __init__(self, name, labels, probability):
        self._name = name
        self._labels = labels
        self._probability = probability
        self._is_triggered = False

    def apply(self, prediction):
        self._is_triggered = False

        for instance in prediction["instances"]:
            for label in instance["labels"]:
                if label["class"] in self._labels and label["probability"] >= self._probability:
                    self._is_triggered = True
                    return

    def is_triggered(self):
        return self._is_triggered

    @classmethod
    def make(cls, desc):
        try:
            name = desc["name"]
            labels = desc["labels"] if isinstance(
                desc["labels"], list) else [desc["labels"]]
            probability = desc["probability"]
        except KeyError as e:
            raise FilterError("Malformed filter description") from e

        return Filter(name, labels, probability)


class ActionError(RuntimeError):
    pass


class Action:
    @classmethod
    def make(cls, desc):
        try:
            atype = desc["type"]
        except KeyError as e:
            raise ActionError("No type specified for action") from e

        if atype == "log_event":
            return LogEvent.make(desc)
        else:
            raise ActionError('Unkown action "%s"' % atype)
