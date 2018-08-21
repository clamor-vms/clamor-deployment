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

import os
import sys
import json

from Skaioskit.Constants import SKAIOSKIT
from CLI.Logger import Logger
from CLI.ProcessHandlerMixin import ProcessHandlerMixin


class DeployProcessor(ProcessHandlerMixin):
    def __init__(self):
        self.config = None
        with open('deploy.json') as data_file:
            self.config = json.load(data_file)

    def run(self):
        Logger.log(SKAIOSKIT + " deployment processor running for: " + self.config['Title'])
        if not len(sys.argv) > 1:
            sys.exit("Missing command parameter")
        if sys.argv[1] not in self.config["Commands"]:
            sys.exit("Unknown command " + sys.argv[1])

        self.process_command(self.config["Commands"][sys.argv[1]])

    def process_command(self, command):
        for required in command['Requires']:
            if required not in self.config["Commands"]:
                sys.exit("Unknown command " + required)
            self.process_command(self.config["Commands"][required])

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
        self.run_process(['python', '../../deploy', step['Args']['Command']], step['Args']['Dir'])

    def __run_command(self, step):
        self.run_process(map(self.__command_template_processor, step['Args']['Command']), None)

    def __command_template_processor(self, token):
        ret = token
        ret = ret.replace("${DIR}", os.getcwd())
        return ret
