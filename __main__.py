#!/usr/bin/env python

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

from Clamor.Constants import VERSION, SUPPORT_EMAIL_ADDRESS, CLAMOR, APP_STATUS
from Deployment.DeployProcessor import DeployProcessor

__author__ = CLAMOR
__copyright__ = "Copyright 2018, " + CLAMOR
__credits__ = [CLAMOR]
__license__ = "AGPLv3"
__version__ = VERSION
__maintainer__ = CLAMOR
__email__ = SUPPORT_EMAIL_ADDRESS
__status__ = APP_STATUS

if __name__ == "__main__":
    app = DeployProcessor()
    app.run()
