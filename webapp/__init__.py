# This file is part of Twisted Klein webapp template.
# Author: Dario Berzano <dario.berzano@gmail.com>
#
# Twisted Klein webapp template is free software: you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free Software Foundation, either
# version 3 of the License, or (at your option) any later version.
#
# Twisted Klein webapp template is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR
# PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with Twisted Klein webapp
# template. If not, see <http://www.gnu.org/licenses/>.

"""This is the Twisted/Klein webapp template. Fork this sample web application based on Twisted and
Klein to create an asynchronous Python web application preconfigured to suit most use cases.

Twisted is a popular framework for asynchronous processing in Python. `asyncio`, and Python 3.5+,
have incorporated many concepts from Twisted. Twisted has its own event loop and in a Klein
application that is the one that should be used.

For more information see:

* https://asyncio.readthedocs.io/en/latest/twisted.html
* https://snarky.ca/how-the-heck-does-async-await-work-in-python-3-5/
* https://docs.python.org/3/reference/datamodel.html?#awaitable-objects
* https://stackoverflow.com/q/9708902
* https://www.aeracode.org/2018/02/19/python-async-simplified/

Features:

* Jinja2 rendering engine
* Form handling
* Asynchronous examples
* Preconfigured directories for templates (`templates`) and static files (`static`)
* Pylint and copyright notice checks for Travis (work locally as well)
"""

import binascii
import os.path
import json
import time
from platform import python_version
from pkg_resources import resource_filename

from klein import Klein
from jinja2 import Environment, PackageLoader
from twisted.web.static import File
from twisted.internet.defer import inlineCallbacks, returnValue
from twisted.internet.task import deferLater
from twisted.internet import reactor

from .utils import get_form

APP = Klein()

# Initialize the Jinja2 template engine
J2 = Environment(loader=PackageLoader(__name__, "templates"))
J2.filters["render_image"] = lambda x: \
    (f'<img src="data:image/png;base64, {binascii.b2a_base64(x.read()).decode("utf-8")}"' +
     'alt="ML plot" height="500">') if x else "<!-- no such image -->"

def async_sleep(sleep_sec: int):
    """Sleep asynchronously. Returns a Deferred.
    """
    return deferLater(reactor, sleep_sec, lambda *x, **y: None)

@APP.route("/")
def root(req):  # pylint: disable=unused-argument
    """Serve the home page.
    """
    return J2.get_template("index.html.j2").render(title=__name__, pyver=python_version())

@APP.route("/async-old")
@inlineCallbacks
def async_old(req):
    """Example of an asynchronous function using old-school inlineCallbacks decorator and extended
    generators. One must use `returnValue` to return the value that Klein will render.
    """
    waitSec = 3
    t0 = time.time()
    yield async_sleep(waitSec)
    req.setHeader("Content-Type", "application/json")
    returnValue(json.dumps({"status": "ok", "waitRequested": waitSec, "waitedFor": time.time()-t0}))

@APP.route("/async")
async def async_new(req):
    """Asynchronous function using the new Python 3.5+ syntax supporting coroutines. This is what
    should be used now, and it is 1:1 equivalent to `async_old`.
    """
    waitSec = 3
    t0 = time.time()
    await async_sleep(waitSec)
    req.setHeader("Content-Type", "application/json")
    return json.dumps({"status": "ok", "waitRequested": waitSec, "waitedFor": time.time()-t0})

@APP.route("/static/", branch=True)
def static(req):  # pylint: disable=unused-argument
    """Serve all static files. Works for pip-installed packages too. See:
    https://klein.readthedocs.io/en/latest/introduction/1-gettingstarted.html#static-files.
    """
    staticPrefix = resource_filename(__name__, "static")
    return File(staticPrefix)

def main():
    """Entry point. Executes the web application by reading some configuration bits from the
    environment.
    """
    APP.run(host=os.environ.get("WEBAPP_HOST", "127.0.0.1"),
            port=int(os.environ.get("WEBAPP_PORT", "8080")))
