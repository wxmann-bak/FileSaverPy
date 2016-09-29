import cmd
from datetime import datetime

from plugins import ssd

__author__ = 'tangz'


class Session(cmd.Cmd):
    def __init__(self):
        cmd.Cmd.__init__(self)
        self.contexts = {}
        self.intro = 'New session started at: ' + datetime.now().strftime('%b %m, %Y at %I:%M %p local time')


    def do_ssd(self, configfile):
        context = ssd.load_config(configfile)
        self.contexts[context.name] = context
        context.runall()

    def do_exit(self, s):
        for context_id in self.contexts:
            self.contexts[context_id].stopall()
        return True


def main():
    Session().cmdloop()


if __name__ == "__main__":
    main()