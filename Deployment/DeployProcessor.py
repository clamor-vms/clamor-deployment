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

import argparse
import os
import sys
import json

from Skaioskit.Constants import SKAIOSKIT, APP_NAME, VERSION
from CLI.Logger import Logger
from CLI.ProcessHandlerMixin import ProcessHandlerMixin


class DeployProcessor(ProcessHandlerMixin):
    def __init__(self):
        self.config = None
        self.args = self.__parse_args()

        os.chdir(self.args.dir)

        with open('deploy.json') as data_file:
            self.config = json.load(data_file)

    def run(self):
        Logger.log(SKAIOSKIT + " deployment processor running for: " + self.config['Title'])
        if self.args.command is None:
            sys.exit("Missing command parameter")
        if self.args.command not in self.config["Commands"]:
            sys.exit("Unknown command " + self.args.command)

        self.__process_command(self.config["Commands"][self.args.command])

    def __parse_args(self):
        self.parser = argparse.ArgumentParser()
        self.parser.add_argument('command', action='store', help="Command Key")
        self.parser.add_argument('-d', '--dir', action='store', dest='dir', help='Directory where YAML config files is located', default=os.getcwd())
        self.parser.add_argument('--version', action='version', version=APP_NAME + ' ' + VERSION)

        return self.parser.parse_args()

    def __process_command(self, command):
        for required in command['Requires']:
            if required not in self.config["Commands"]:
                sys.exit("Unknown command " + required)
            self.__process_command(self.config["Commands"][required])

        for step in command['Steps']:
            if step['Type'] == "PrintMessage":
                self.__print_message(step)
            elif step['Type'] == 'ChildDeployment':
                self.__child_deployment(step)
            elif step['Type'] == 'RunCommand':
                self.__run_command(step)
            else:
                Logger.log("Unknown Deployment Type: " + step['Type'])

    def __print_message(self, step):
        Logger.log(step['Args']['Message'])

    def __child_deployment(self, step):

        self.run_process(['python', 'deploy', step['Args']['Command'], '-d', step['Args']['Dir']], None)

    def __run_command(self, step):
        self.run_process(map(self.__command_template_processor, step['Args']['Command']), None)

    def __command_template_processor(self, token):
        ret = token
        ret = ret.replace("${DIR}", os.getcwd())
        return ret
