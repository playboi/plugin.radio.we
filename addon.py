# -*- coding: utf-8 -*-
# Module: addon
# Author: Mike Knight
# Created on: 12.09.2019
# License MIT

import sys
import json

from urllib import urlencode
from urlparse import parse_qsl

import xbmcaddon
import xbmcgui
import xbmcplugin

_url = sys.argv[0]
_handle = int(sys.argv[1])
ADDON = xbmcaddon.Addon('plugin.radio.we')
CWD = ADDON.getAddonInfo('path').decode('utf-8')


def get_url(**kwargs):
    return '{0}?{1}'.format(_url, urlencode(kwargs))


def get_stations_list():
    with open(CWD + '/resources/data/stations.json', 'r') as f:
        STATIONS = json.load(f)

    return STATIONS


def list_stations():
    xbmcplugin.setPluginCategory(_handle, 'Stations')
    xbmcplugin.setContent(_handle, 'songs')

    stations = get_stations_list()

    for station in stations:
        list_item = xbmcgui.ListItem(
            label=station['name'], thumbnailImage=station['thumb'])
        list_item.setArt({
            'thumb': CWD + '/resources/media/thumb/' + station['thumb'],
            'icon': CWD + '/resources/media/icon/' + station['thumb'],
            'fanart': CWD + '/resources/media/fanart/' + station['fanart']
        })

        list_item.setInfo(
            'music', {'title': station['name'], 'genre': station['genre'], 'mediatype': 'episode'})

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
