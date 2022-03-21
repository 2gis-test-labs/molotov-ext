from argparse import Namespace
from functools import partial
from typing import Any

import molotov

from .formatters import DefaultFormatter
from .record_table import RecordTable
from .recorder import Recorder
from .reporter import Reporter
from .scenario import Scenario

__all__ = ("Reporter", "register_reporter", "scenario", "recorder")

recorder = Recorder(RecordTable())
scenario = partial(Scenario, recorder.on_starting_scenario)


@molotov.events()
async def event_listener(event: str, **info: Any) -> None:
    if event == "sending_request":
        recorder.on_sending_request(info["session"], info["request"])

    elif event == "response_received":
        recorder.on_response_received(info["session"], info["response"], info["request"])

    elif event == "scenario_success":
        recorder.on_scenario_success(info["scenario"]["name"], info["wid"])

    elif event == "scenario_failure":
        recorder.on_scenario_failure(info["scenario"]["name"], info["wid"], info['exception'])

    elif event == "current_workers":
        recorder.on_current_workers(info["workers"])


def register_reporter(args: Namespace) -> Reporter:
    if args.processes > 1:
        raise NotImplementedError('Возможность работы с несколькими процессами не поддерживается!')
    return Reporter(recorder, DefaultFormatter())
