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
from random import randint
from platform import python_version
from pkg_resources import resource_filename

from klein import Klein
from jinja2 import Environment, PackageLoader
from twisted.python import log
from twisted.web.static import File
from twisted.internet.defer import inlineCallbacks, returnValue
from twisted.internet.task import deferLater
from twisted.internet.threads import deferToThread
from twisted.internet import reactor

from .utils import get_form, no_cache

APP = Klein()
JOBS = {}

# Initialize the Jinja2 template engine
J2 = Environment(loader=PackageLoader(__name__, "templates"))
J2.filters["render_image"] = lambda x: \
    (f'<img src="data:image/png;base64, {binascii.b2a_base64(x.read()).decode("utf-8")}"' +
     'alt="ML plot" height="500">') if x else "<!-- no such image -->"

def async_sleep(sleep_sec: int):
    """Sleep asynchronously. Returns a Deferred.
    """
    return deferLater(reactor, sleep_sec, lambda *x, **y: None)

def long_running_job(job_id):
    """This is a long-running job that should run in a thread.
    """
    log.msg(f"long_running_job(): job {job_id} started")
    time.sleep(10)
    log.msg(f"long_running_job(): job {job_id} finished")

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

@APP.route("/start-job")
def start_job(req):
    """A long-running process requiring a separate thread for running. This call returns a JSON
    containing an ID that will be used to query whether the processing has finished.
    """
    jobId = 0
    while jobId == 0 or jobId in JOBS:
        jobId = randint(1, 1000)
    log.msg(f"start_job(): created new job with id {jobId}")
    JOBS[jobId] = {"running": True, "finished": False}  # job is queued

    def job_finished(job_return, job_id):
        log.msg(f"job_finished(): job {job_id} returned {job_return}")
        JOBS[job_id]["running"] = False
        JOBS[job_id]["finished"] = True

    d = deferToThread(long_running_job, jobId)
    d.addCallback(job_finished, jobId)

    req.setHeader("Content-Type", "application/json")
    return json.dumps({"jobId": jobId})

@APP.route("/query-job")
def query_job(req):
    """Get status of all jobs, or a single one if `jobId` parameter is given.
    """
    req.setHeader("Content-Type", "application/json")
    no_cache(req)
    try:
        jobId = int(get_form(req, "jobId"))
    except (KeyError, ValueError):
        jobId = 0
    log.msg(f"Requested status of job {jobId}")
    if jobId == 0:
        return json.dumps(JOBS)  # beware, keys are converted to strings (hashable)
    return json.dumps({jobId: JOBS.get(jobId, {})})

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
