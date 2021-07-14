#!/usr/bin/env python3
#  Copyright (C) 2021 RidgeRun, LLC (http://www.ridgerun.com)
#  Authors: Daniel Chaves <daniel.chaves@ridgerun.com>
#           Marisol Zeledon <marisol.zeledon@ridgerun.com>


def validate_objects(dict, key, expected_type, key_err_msg, type_err_msg):
    try:
        value = dict[key]
    except KeyError as e:
        raise AppValidatortError(key_err_msg) from e

    if not isinstance(value, expected_type):
        raise AppValidatortError(type_err_msg)


def validate_lists(in_list, expected_type, type_err_msg):
    for list_object in in_list:
        if not isinstance(list_object, expected_type):
            raise AppValidatortError(type_err_msg)


def validate_streams(cfg):
    validate_objects(
        cfg,
        'streams',
        list,
        "Streams object not found",
        "Invalid streams format")
    streams = cfg['streams']

    for stream in streams:
        validate_objects(
            stream,
            'id',
            str,
            "id property not found in stream",
            "Invalid id format")
        validate_objects(
            stream,
            'uri',
            str,
            "uri property not found in stream",
            "Invalid uri format")
        validate_objects(
            stream,
            'triggers',
            list,
            "triggers property not found in stream",
            "Invalid triggers format")

        stream_triggers = stream["triggers"]
        validate_lists(
            stream_triggers,
            str,
            "Invalid trigger format in streams triggers")


def validate_filters(cfg):
    validate_objects(
        cfg,
        'filters',
        list,
        "filters object not found",
        "Invalid filters format")
    filters = cfg['filters']

    for filt in filters:
        validate_objects(
            filt,
            'name',
            str,
            "name property not found in filter",
            "Invalid name format in filter")
        validate_objects(
            filt,
            'labels',
            list,
            "labels property not found in filter",
            "Invalid labels format in filter")
        validate_objects(
            filt,
            'threshold',
            float,
            "threshold property not found in filter",
            "Invalid threshold format")

        filter_labels = filt['labels']
        validate_lists(
            filter_labels,
            str,
            "Invalid label format in filter labels")


def validate_actions(cfg):
    validate_objects(
        cfg,
        'actions',
        list,
        "actions object not found",
        "Invalid actions format")
    actions = cfg['actions']

    for action in actions:
        validate_objects(
            action,
            'name',
            str,
            "name property not found in action",
            "Invalid name format in action")
        validate_objects(
            action,
            'type',
            str,
            "type property not found in action",
            "Invalid type format in action")
        validate_objects(
            action,
            'location',
            str,
            "location property not found in action",
            "Invalid location format in action")

        action_type = action['type']
        if (action_type == 'recording'):
            validate_objects(
                action,
                'lenght',
                int,
                "lenght property not found in action of type recording",
                "Invalid lenght format in action of type recording")


def validate_triggers(cfg):
    validate_objects(
        cfg,
        'triggers',
        list,
        "triggers object not found",
        "Invalid triggers format")
    triggers = cfg['triggers']

    for trigger in triggers:
        validate_objects(
            trigger,
            'name',
            str,
            "name property not found in triggers",
            "Invalid name format in triggers")
        validate_objects(
            trigger,
            'action',
            str,
            "action property not found in triggers",
            "Invalid action format in triggers")
        validate_objects(
            trigger,
            'filters',
            list,
            "filters property not found in triggers",
            "Invalid filters format in triggers")

    trigger_filters = trigger['filters']
    validate_lists(
        trigger_filters,
        str,
        "Invalid filter format in triggers filters")


class AppValidatortError(RuntimeError):
    pass


class AppValidator():

    def validate(self, cfg):
        validate_streams(cfg)
        validate_filters(cfg)
        validate_actions(cfg)
        validate_triggers(cfg)
