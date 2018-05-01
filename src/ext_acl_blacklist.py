#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
from os import path
import sys
import signal
from urlparse import urlparse
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer
import logging
import logging.handlers

logger = None
observer = None
bli = None
bl = None


class PySquidBlacklistsImporter:
    def __init__(self, file):
        self.file = file
        self.make_ram_db()

    def make_ram_db(self):
        self.cache = None
        lib = set()
        with open(self.file, 'r') as blacklist_file:
            for line in blacklist_file:
                line = line.strip().lstrip('.')
                if not line.startswith('#') and line:
                    lib.add(line)
        self.cache = lib


class PySquidBlacklistsRunner:
    def __init__(self, bli):
        self.update_cache(bli)

    def update_cache(self, bli):
        self.cache = bli.cache

    def domain_compare(self):
        result = False
        if self.outline in self.cache:
            result = True
        return result

    def loop(self):
        while True:
            try:
                input = sys.stdin.readline()
                if len(input) == 0:
                    raise RuntimeError
                else:
                    input = input.split()

            except Exception:
                break
                sys.exit()

            try:
                id = input[0]
                url = input[1]
                self.outline = urlparse(url).netloc
                if self.domain_compare():
                    self.response('{} OK'.format(id))
                else:
                    self.response('{} ERR'.format(id))
            except:
                continue

    @staticmethod
    def response(r):
        sys.stdout.write("%s\n" % r)
        sys.stdout.flush()


class BliEventHandler(FileSystemEventHandler):
    def __init__(self, filename):
        self.filename = filename

    def handler(self, event):
        if not event.is_directory and path.basename(self.filename) == path.basename(event.src_path):
            bli.make_ram_db()
            bl.update_cache(bli)
            logger.info('Squid external acl blacklist updated successfully')

    def on_modified(self, event):
        self.handler(event)

    def on_created(self, event):
        self.handler(event)


def signal_handler(signal, frame):
    global observer
    observer.unschedule_all()
    observer.stop()
    sys.exit(0)


def create_cli():
    parser = argparse.ArgumentParser(description='Squid external acl blacklist helper')
    parser.add_argument('-f', '--blacklist-file', required=True,
                        help='blacklist file')
    parser.add_argument('-l', '--log-file', default='/var/log/squid/blacklist.log',
                        help='log file path (defaults to %(default)s)')
    return parser


def main():
    signal.signal(signal.SIGINT, signal_handler)

    global observer
    global bli
    global bl
    global logger

    parser = create_cli()
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)
    args = parser.parse_args()

    logger = logging.getLogger('ext_acl_blacklist')
    hdlr = logging.handlers.WatchedFileHandler(args.log_file)
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    hdlr.setFormatter(formatter)
    logger.addHandler(hdlr)
    logger.setLevel(logging.INFO)

    if not path.isfile(args.blacklist_file):
        print('Squid external acl blacklist file {} not found'.format(args.blacklist_file))
        logger.warning('Squid external acl blacklist file {} not found'.format(args.blacklist_file))
        sys.exit()

    bli = PySquidBlacklistsImporter(args.blacklist_file)
    bl = PySquidBlacklistsRunner(bli)

    event_handler = BliEventHandler(args.blacklist_file)
    observer = Observer()
    observer.schedule(event_handler, path=path.dirname(args.blacklist_file))
    observer.daemon = True
    observer.start()

    bl.loop()


if __name__ == '__main__':
    main()
