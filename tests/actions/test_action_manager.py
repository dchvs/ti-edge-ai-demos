#!/usr/bin/env python3
#  Copyright (C) 2021 RidgeRun, LLC (http://www.ridgerun.com)
#  Authors: Daniel Chaves <daniel.chaves@ridgerun.com>
#           Marisol Zeledon <marisol.zeledon@ridgerun.com>

import unittest
from unittest.mock import MagicMock

from rr.actions.action_manager import Filter, FilterError
from rr.actions.action_manager import Action, ActionError
from rr.actions.action_manager import Trigger, TriggerError


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


class MockTriggerFilter1:
    def __init__(self):
        self.apply = MagicMock()

    def get_name(self):
        return "mock_filter1"


class MockTriggerFilter2:
    def __init__(self):
        self.apply = MagicMock()

    def get_name(self):
        return "mock_filter2"


class MockTriggerAction:
    def __init__(self):
        self.execute = MagicMock()

    def get_name(self):
        return "mock_action"


class MockTriggerImage:
    pass


class MockTriggerMedia:
    pass


class TestTrigger(unittest.TestCase):

    def setUp(self):
        self.desc = {
            "name": "trigger_name",
            "action": "mock_action",
            "filters": [
                "mock_filter1",
                "mock_filter2",
            ]
        }

        self.action = MockTriggerAction()
        self.filter1 = MockTriggerFilter1()
        self.filter2 = MockTriggerFilter2()
        self.filters = [self.filter1, self.filter2]

    def test_trigger_success(self):
        trigger = Trigger.make(self.desc, [self.action], self.filters)
        self.assertEqual('trigger_name', trigger._name)

        image = MockTriggerImage()
        media = MockTriggerMedia()
        pred = {"mock": "prediction"}

        trigger.execute(pred, image, media)
        self.filter1.apply.assert_called_with(pred)
        self.filter2.apply.assert_called_with(pred)
        self.action.execute.assert_called_with(
            media, image, pred, self.filters)

    def test_trigger_malformed_desc(self):
        # remove name
        self.desc.pop("name")

        with self.assertRaises(TriggerError) as e:
            Trigger.make(self.desc, [self.action], self.filters)

        self.assertEqual("Malformed trigger description", str(e.exception))

    def test_trigger_unkown_action(self):
        self.desc["action"] = "other_action"

        with self.assertRaises(TriggerError) as e:
            Trigger.make(self.desc, [self.action], self.filters)

        self.assertEqual('Unknown action "other_action"', str(e.exception))

    def test_trigger_unkown_filter(self):
        self.desc["filters"].append("mock_filter3")

        with self.assertRaises(TriggerError) as e:
            Trigger.make(self.desc, [self.action], self.filters)

        self.assertEqual('Unknown filter "mock_filter3"', str(e.exception))
