#!/usr/bin/env python3
#  Copyright (C) 2021 RidgeRun, LLC (http://www.ridgerun.com)
#  Authors: Daniel Chaves <daniel.chaves@ridgerun.com>
#           Marisol Zeledon <marisol.zeledon@ridgerun.com>

import unittest

from rr.actions.action_manager import Filter, FilterError
from rr.actions.action_manager import Action, ActionError


class TestFilter(unittest.TestCase):
    def setUp(self):
        self._desc = {
            "name": "test",
            "labels": ["cat", "dog"],
            "probability": 0.5
        }

    def test_make_invalid(self):
        malformed = {"name": "value"}

        with self.assertRaises(FilterError) as e:
            Filter.make(malformed)

        self.assertEqual("Malformed filter description", str(e.exception))

    def common(self, desc, pred, expected):
        filter = Filter.make(desc)
        self.assertEqual(True, filter is not None)

        filter.apply(pred)

        self.assertEqual(expected, filter.is_triggered())

    def test_is_triggered_single_label(self):
        desc = {
            "name": "test",
            "labels": "cat",
            "probability": 0.5
        }

        pred = {"instances": [
            {"labels": [{"class": "cat", "probability": 0.5}]}]}
        self.common(desc, pred, True)

    def test_is_triggered_multi_label(self):
        pred = {"instances": [
            {"labels": [{"class": "dog", "probability": 0.5}]}]}

        self.common(self._desc, pred, True)

    def test_not_triggered_lower_prob(self):
        pred = {"instances": [
            {"labels": [{"class": "dog", "probability": 0.49}]}]}

        self.common(self._desc, pred, False)

    def test_not_triggered_no_class(self):
        pred = {"instances": [
            {"labels": [{"class": "snake", "probability": 0.9}]}]}

        self.common(self._desc, pred, False)


class TestAction(unittest.TestCase):

    def test_make_unkown_action(self):
        unknown = {"type": "unknown"}

        with self.assertRaises(ActionError) as e:
            Action.make(unknown)

        self.assertEqual('Unkown action "unknown"', str(e.exception))
