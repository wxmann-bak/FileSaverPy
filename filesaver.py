import cmd
from datetime import datetime
import logging
from tabulate import tabulate

from plugins import ssd

__author__ = 'tangz'


class Session(cmd.Cmd):
    prompt = '(FileSaver) '

    def __init__(self):
        cmd.Cmd.__init__(self)
        self._contexts = {}
        self.intro = 'New session started at: ' + datetime.now().strftime('%b %m, %Y at %I:%M %p local time')

    def do_info(self, s):
        context_separator = ['---', '---', '---']
        table = []
        headers = ['Contexts', 'Jobs', 'Job Status']
        for context_id in self._contexts:
            context = self._contexts[context_id]
            i = 0
            for job in context:
                firstcol = context.name if i == 0 else ''
                status = 'Running' if job.is_running() else 'Stopped'
                table.append([firstcol, job.name, status])
                i += 1
            table.append(context_separator)
        print(tabulate(table, headers=headers))

    def do_ssd(self, configfile):
        context = ssd.load_config(configfile)
        self._contexts[context.name] = context
        context.runall()

    def do_kill_all(self, contextid):
        if contextid not in self._contexts:
            logging.warning('Cannot find context: ' + contextid)
        else:
            self._contexts[contextid].stopall()

    def do_kill_job(self, jobid):
        for contextid in self._contexts:
            context = self._contexts[contextid]
            if context.hasjob(jobid):
                context.stop(jobid)

    def do_exit(self, s):
        for context_id in self._contexts:
            self._contexts[context_id].stopall()
        return True


def main():
    Session().cmdloop()


if __name__ == "__main__":
    main()