# from filesaver import user_session, root_parser
import logging
from plugins import ssd

__author__ = 'tangz'


_packaged_plugins = {
    'ssd': ssd.load_config
}


def register_plugin(name, plugin_func):
    if name in _packaged_plugins:
        raise ValueError("Plugin {0} already exists".format(name))
    _packaged_plugins[name] = plugin_func


def retrieve(name):
    try:
        return _packaged_plugins.get[name]
    except KeyError:
        logging.error("Plugin {0} does not exist")

