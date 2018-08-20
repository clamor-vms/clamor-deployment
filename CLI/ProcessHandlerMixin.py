"""
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as
    published by the Free Software Foundation, either version 3 of the
    License, or (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

from __future__ import print_function

import os
import sys
from threading import Thread
from subprocess import Popen, PIPE


class ProcessHandlerMixin(object):
    def run_process(self, command, cwd):
        self.__direct_command_output(Popen(command, stdout=PIPE, stderr=PIPE, cwd=cwd))

    def pipe_processes(self, sourceCommand, targetCommand, cwd):
        process = Popen(sourceCommand, stdout=PIPE, cwd=cwd)
        process2 = Popen(targetCommand, stdin=process.stdout, stdout=PIPE, stderr=PIPE, env=os.environ, cwd=cwd)
        process.wait()

        self.__direct_command_output(process2)

    def __direct_command_output(self, process):
        thread = Thread(target=self.__direct_stdout, args=[process])
        thread.start()

        thread2 = Thread(target=self.__direct_stderr, args=[process])
        thread2.start()

        process.wait()
        
        thread.join()
        thread2.join()

    def __direct_stdout(self, proc):
        try:
            with proc.stdout:
                for line in iter(proc.stdout.readline, b''):
                    self.__pipe_to_stdout(line)
        finally:
            pass

    def __direct_stderr(self, proc):
        try:
            with proc.stderr:
                for line in iter(proc.stderr.readline, b''):
                    self.__pipe_to_stderr(line)
        finally:
            pass

    def __pipe_to_stdout(self, value):
        if sys.version_info[0] < 3:
            sys.stdout.write(value)
            sys.stdout.flush()
        else:
            sys.stdout.buffer.write(value)
            sys.stdout.flush()

    def __pipe_to_stderr(self, value):
        if sys.version_info[0] < 3:
            sys.stderr.write(value)
            sys.stderr.flush()
        else:
            sys.stderr.buffer.write(value)
            sys.stderr.flush()
