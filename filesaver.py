import argparse
from datetime import datetime

from core import saver
from plugins import pluginpackage


__author__ = 'tangz'

user_session = None


def main():
    _init_session()

    root_parser = argparse.ArgumentParser(description='FileSaver script')
    subparsers = root_parser.add_subparsers(description='FileSaver options', dest='mode')
    plugin_parser = subparsers.add_parser('plugin', help='Begin saving images')
    plugin_parser.add_argument('name', help='Name of the plugin to use')
    plugin_parser.add_argument('file', help='Config file for plugin settings')

    args = root_parser.parse_args()
    if args.mode == 'plugin':
        _handle_plugin(args)
    else:
        root_parser.print_usage()


def _init_session():
    global user_session
    user_session = saver.Session()
    print('New session started at: ' + datetime.now().strftime('%b %m, %Y at %H:%M %p local time'))


def _handle_plugin(args):
    plugin = pluginpackage.retrieve(args.name)
    context = plugin(args.file)
    user_session.add_context(context)
    context.runall()


if __name__ == "__main__":
    main()