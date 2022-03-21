from time import time
from typing import Callable, List, Optional, Union

import molotov.util
from aiohttp import ClientConnectorError
from aiohttp import ClientResponse as Response
from molotov.session import ClientSession as Session
from molotov.session import LoggedClientRequest as Request
from molotov.session import SessionTracer, get_context

from .record_table import RecordTable
from .records import ErrorRecord, ScenarioRecord, WorkerAccumRecord
from .scenario import Scenario

ResponseHookType = Callable[[ScenarioRecord, Response, Request], None]


class Recorder:
    CLIENT_CLOSED_REQUEST = 499

    def __init__(self, record_table: RecordTable) -> None:
        self._record_table = record_table
        self._requests_log: List[ScenarioRecord] = []
        self._workers_log: List[WorkerAccumRecord] = []
        self._response_hook: Union[ResponseHookType, None] = None

    def register_response_hook(self, callaback: ResponseHookType) -> None:
        self._response_hook = callaback

    def get_requests_log(self) -> List[ScenarioRecord]:
        return self._requests_log

    def get_workers_log(self) -> List[WorkerAccumRecord]:
        return self._workers_log

    def on_starting_scenario(self, scenario: Scenario, session: Session) -> None:
        context = get_context(session)
        record = ScenarioRecord(
            worker_id=context.worker_id,
            scenario_name=context.scenario_name,
            scenario_started=time(),
            scenario_status="STARTED",
        )
        self._record_table.register((context.scenario_name, context.worker_id), record)

    def on_scenario_success(self, scenario_name: str, worker_id: int) -> None:
        record = self._record_table.get((scenario_name, worker_id))
        record.scenario_ended = time()
        record.scenario_status = "SUCCESS"

        self._requests_log.append(record)
        self._record_table.delete((scenario_name, worker_id))

    def on_scenario_failure(self, scenario_name: str, worker_id: int, exception: Optional[Exception] = None) -> None:
        record = self._record_table.get((scenario_name, worker_id))
        record.scenario_ended = time()
        if isinstance(exception, ClientConnectorError):
            error_record = ErrorRecord(worker_id, scenario_name, record.scenario_ended, repr(exception))
            molotov.util.stop(error_record)
        if isinstance(exception, AssertionError):
            record.scenario_assert_message = str(exception)
        record.scenario_status = "FAILED"
        # если по какой то причине нет времени начала/конца запроса, то берем время начала/конца сценария
        if record.request_started is None:
            record.request_started = record.scenario_started
        if record.request_ended is None:
            record.request_ended = record.scenario_ended
            record.response_status = Recorder.CLIENT_CLOSED_REQUEST

        self._requests_log.append(record)
        self._record_table.delete((scenario_name, worker_id))

    def on_sending_request(self, session: Session, request: Request) -> None:
        request.started_at = time()

    def on_response_received(self, session: SessionTracer, response: Response, request: Request) -> None:
        context = session.context
        record = self._record_table.get((context.scenario_name, context.worker_id))
        record.request_started = request.started_at
        record.request_ended = time()
        record.response_status = response.status
        record.request_url = request.url
        if self._response_hook:
            self._response_hook(record, response, request)

    def on_current_workers(self, worker_count: int) -> None:
        record = WorkerAccumRecord(time(), worker_count)
        self._workers_log.append(record)
