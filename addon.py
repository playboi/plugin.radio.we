# -*- coding: utf-8 -*-
# Module: addon
# Author: Mike Knight
# Created on: 12.09.2019
# License MIT

import sys
import json

from urllib import urlencode
from urlparse import parse_qsl

import xbmcgui
import xbmcplugin

_url = sys.argv[0]
_handle = int(sys.argv[1])

with open('./stations.json', 'r') as f:
    STATIONS = json.load(f)


def get_url(**kwargs):
    return '{0}?{1}'.format(_url, urlencode(kwargs))


def get_stations_list():
    return STATIONS


def list_stations():
    xbmcplugin.setPluginCategory(_handle, 'My Caribbean Radio Stations')
    xbmcplugin.setContent(_handle, 'songs')

    stations = get_stations_list()

    for station in stations:
        list_item = xbmcgui.ListItem(label=station['name'])
        list_item.setArt({
            'thumb': station['thumb'],
            'icon': station['thumb'],
            'fanart': station['thumb']
        })

        list_item.setInfo(
            'audio', {'title': station['name'], 'genre': '', 'mediatype': 'audio'})

        # This is mandatory for playable items!
        list_item.setProperty('IsPlayable', 'true')

        url = get_url(action='play', stream=station['stream'])

        is_folder = False

        xbmcplugin.addDirectoryItem(_handle, url, list_item, is_folder)

    xbmcplugin.endOfDirectory(_handle)


def play_stream(path):
    play_item = xbmcgui.ListItem(path=path)
    xbmcplugin.setResolvedUrl(_handle, True, listitem=play_item)


def router(paramstring):
    """
    Router function that calls other functions
    depending on the provided paramstring

    :param paramstring: URL encoded plugin paramstring
    :type paramstring: str
    """
    # Parse a URL-encoded paramstring to the dictionary of
    # {<parameter>: <value>} elements
    params = dict(parse_qsl(paramstring))
    # Check the parameters passed to the plugin
    if params:
        if params['action'] == 'listing':
            # Display the list of stations .
            list_stations()
        elif params['action'] == 'play':
            # Play a video from a provided URL.
            play_stream(params['stream'])
        else:
            # If the provided paramstring does not contain a supported action
            # we raise an exception. This helps to catch coding errors,
            # e.g. typos in action names.
            raise ValueError('Invalid paramstring: {0}!'.format(paramstring))
    else:
        # If the plugin is called from Kodi UI without any parameters,
        # display the list of video categories
        list_stations()


if __name__ == '__main__':
    # Call the router function and pass the plugin call parameters to it.
    # We use string slicing to trim the leading '?' from the plugin call paramstring
    router(sys.argv[2][1:])
