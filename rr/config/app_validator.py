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


def validate_dependency(obj, available_objs, err_msg):
    if obj not in available_objs:
        raise AppValidatortError(err_msg)


def validate_streams(cfg, triggers):
    validate_objects(
        cfg,
        'streams',
        list,
        "Streams field not found",
        "Found streams field, but is is not a list")
    streams = cfg['streams']

    for stream in streams:
        validate_objects(
            stream,
            'id',
            str,
            "Id field not found in stream",
            "Found id field in stream, but is is not a string")
        validate_objects(
            stream,
            'uri',
            str,
            "Uri field not found in stream",
            "Found uri field in stream, but is is not a string")
        validate_objects(
            stream,
            'triggers',
            list,
            "Triggers field not found in stream",
            "Found triggers field in stream, but is is not a list")

        stream_triggers = stream["triggers"]
        validate_lists(
            stream_triggers,
            str,
            "Found trigger element in stream, but it is not a string")

        for trigger in stream_triggers:
            validate_dependency(
                trigger, triggers, "Stream has a not defined trigger")


def validate_filters(cfg):
    validate_objects(
        cfg,
        'filters',
        list,
        "Filters field not found",
        "Found filters field, but is is not a list")
    filters = cfg['filters']

    filters_list = []
    for filt in filters:
        validate_objects(
            filt,
            'name',
            str,
            "Name field not found in filter",
            "Found name field in filter, but it is not a string")
        validate_objects(
            filt,
            'labels',
            list,
            "Labels field not found in filter",
            "Found labels field in filter, but it is not a list")
        validate_objects(
            filt,
            'threshold',
            float,
            "Threshold field not found in filter",
            "Found threshold field in filter, but it is not a number")

        filter_labels = filt['labels']
        validate_lists(
            filter_labels,
            str,
            "Found label element in filter, but it is not a string")

        filters_list.append(filt['name'])

    return filters_list


def validate_actions(cfg):
    validate_objects(
        cfg,
        'actions',
        list,
        "Actions field not found",
        "Found actions field, but is is not a list")
    actions = cfg['actions']

    actions_list = []
    for action in actions:
        validate_objects(
            action,
            'name',
            str,
            "Name field not found in action",
            "Found name field in action, but it is not a string")
        validate_objects(
            action,
            'type',
            str,
            "Type field not found in action",
            "Found type field in action, but it is not a string")
        validate_objects(
            action,
            'location',
            str,
            "Location field not found in action",
            "Found location field in action, but it is not a string")

        action_type = action['type']
        if (action_type == 'recording'):
            validate_objects(
                action,
                'lenght',
                int,
                "Lenght field not found in action of type recording",
                "Lenght field in action must be a whole number")

        actions_list.append(action['name'])

    return actions_list


def validate_triggers(cfg, actions, filters):
    validate_objects(
        cfg,
        'triggers',
        list,
        "Triggers field not found",
        "Found triggers field, but is is not a list")
    triggers = cfg['triggers']

    triggers_list = []
    for trigger in triggers:
        validate_objects(
            trigger,
            'name',
            str,
            "Name field not found in trigger",
            "Found name field in action, but it is not a string")
        validate_objects(
            trigger,
            'action',
            str,
            "Action field not found in trigger",
            "Found action field in trigger, but it is not a string")
        validate_objects(
            trigger,
            'filters',
            list,
            "Filters field not found in trigger",
            "Found filters field in trigger, but it is not a list")

        trigger_filters = trigger['filters']
        validate_lists(
            trigger_filters,
            str,
            "Found filter element in trigger, but it is not a string")

        for filt in trigger_filters:
            validate_dependency(
                filt, filters, "Trigger has a not defined filter")
        validate_dependency(
            trigger['action'],
            actions,
            "Trigger has a not defined action")

        triggers_list.append(trigger['name'])

    return triggers_list


class AppValidatortError(RuntimeError):
    pass


class AppValidator():

    def validate(self, cfg):
        filters = validate_filters(cfg)
        actions = validate_actions(cfg)
        triggers = validate_triggers(cfg, actions, filters)
        validate_streams(cfg, triggers)
