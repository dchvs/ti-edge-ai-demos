#!/usr/bin/env python3
#  Copyright (C) 2021 RidgeRun, LLC (http://www.ridgerun.com)
#  Authors: Daniel Chaves <daniel.chaves@ridgerun.com>
#           Marisol Zeledon <marisol.zeledon@ridgerun.com>


class AppValidatortError(RuntimeError):
    pass


class AppValidator():

    def validate_streams(self, cfg):
        try:
            streams = cfg['streams']
        except KeyError as e:
            raise AppValidatortError("streams object not found") from e

        if (not isinstance(streams, list)):
            raise AppValidatortError("Invalid streams format")

        for stream in streams:
            try:
                stream_id = stream['id']
            except KeyError as e:
                raise AppValidatortError(
                    "id property not found in stream") from e
            try:
                stream_uri = stream['uri']
            except KeyError as e:
                raise AppValidatortError(
                    "uri property not found in stream") from e
            try:
                stream_triggers = stream['triggers']
            except KeyError as e:
                raise AppValidatortError(
                    "triggers property not found in stream") from e

            if (not isinstance(stream_id, str)):
                raise AppValidatortError("Invalid id format")
            if (not isinstance(stream_uri, str)):
                raise AppValidatortError("Invalid uri format")
            if (not isinstance(stream_triggers, list)):
                raise AppValidatortError("Invalid triggers format")

    def validate_filters(self, cfg):
        try:
            filters = cfg['filters']
        except KeyError as e:
            raise AppValidatortError("filters object not found") from e

        if (not isinstance(filters, list)):
            raise AppValidatortError("Invalid filters format")

        for filt in filters:
            try:
                filter_name = filt['name']
            except KeyError as e:
                raise AppValidatortError(
                    "name property not found in filter") from e
            try:
                filter_labels = filt['labels']
            except KeyError as e:
                raise AppValidatortError(
                    "labels property not found in filter") from e
            try:
                filter_thresh = filt['threshold']
            except KeyError as e:
                raise AppValidatortError(
                    "threshold property not found in filter") from e

            if (not isinstance(filter_name, str)):
                raise AppValidatortError("Invalid name format in filter")
            if (not isinstance(filter_labels, list)):
                raise AppValidatortError("Invalid labels format in filter")
            if (not isinstance(filter_thresh, float)):
                raise AppValidatortError("Invalid threshold format")

            for label in filter_labels:
                if (not isinstance(label, str)):
                    raise AppValidatortError(
                        "Invalid label format in filter labels")
