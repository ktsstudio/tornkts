import logging
import pkgutil
import sys
import traceback

import os

__author__ = 'grigory51'

os.environ['TORNKTS_ENV'] = 'manage'


class Manage(object):
    commands = ['help']

    def commands_list(self):
        return [name for _, name, _ in pkgutil.iter_modules(['commands'])] + ['help']

    def help(self):
        commands_list = self.commands_list()
        print('Available commands:\n - %s' % ('\n - '.join(commands_list)))

    def run(self, command):
        if command not in self.commands_list():
            logging.error('Command %s not found' % command)
            self.help()
        try:
            __import__('commands.%s' % command)
            return 0
        except Exception:
            traceback.print_exc()


if __name__ == '__main__':
    manage = Manage()
    manage.run(sys.argv[1])
