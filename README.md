# Molotov Extensions

Library for collecting metrics for [Molotov](https://molotov.readthedocs.io/en/stable/)

## Installation

```shell
pip3 install molotov-ext
```

## Example

loadtest.py
```python
from argparse import Namespace

import molotov
from molotov.session import ClientSession as Session
from molotov_ext import scenario, register_reporter
from molotov_ext.formatters import PhantomFormatter


@molotov.global_setup()
def setup_global(args: Namespace):
    molotov.set_var("reporter", register_reporter(args))


@scenario(weight=1)
async def scenario(session: Session):
    async with session.get("http://localhost:8080") as resp:
        res = await resp.json()
        assert resp.status == 200


@molotov.global_teardown()
def teardown_global():
    reporter = molotov.get_var("reporter")
    reporter.save_workers_log("workers.csv")
    reporter.save_requests_log("requests.csv")
    reporter.save_client_errors_log("client_errors.csv")
    reporter.save_requests_log("phout_1.log", PhantomFormatter())
```

```sh
$ molotov --workers=1 --duration=1 --max-runs=1 -vv
```

### GatlingFormatter

```python
from argparse import Namespace

import molotov
from aiohttp import StringPayload, JsonPayload, ClientResponse as Response
from molotov.session import ClientSession as Session, LoggedClientRequest as Request

from molotov_ext import scenario, recorder, register_reporter
from molotov_ext.formatters import PhantomFormatter, GatlingFormatter
from molotov_ext.records import ScenarioRecord


def on_response(record: ScenarioRecord, response: Response, request: Request):
    if isinstance(request.body, (StringPayload, JsonPayload)):
        try:
            record.request_payload = request.body._value.decode(request.body.encoding)
        except:
            pass


recorder.register_response_hook(on_response)


@molotov.global_setup()
def setup_global(args: Namespace):
    molotov.set_var("reporter", register_reporter(args))


@scenario(weight=1)
async def scenario(session: Session):
    async with session.post("http://localhost:8080", json={"payload": "<payload>"}) as resp:
        res = await resp.json()
        assert resp.status == 200


@molotov.global_teardown()
def teardown_global():
    reporter = molotov.get_var("reporter")
    reporter.save_workers_log("workers.csv")
    reporter.save_requests_log("requests.csv")
    reporter.save_client_errors_log("client_errors.csv")
    reporter.save_requests_log("simulation.log", GatlingFormatter())
```
