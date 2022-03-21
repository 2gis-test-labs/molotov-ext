from dataclasses import dataclass
from typing import Any, Optional


@dataclass
class Record:
    pass


@dataclass(order=True)
class ScenarioRecord(Record):
    worker_id: Optional[int] = None
    scenario_name: Optional[str] = None
    scenario_started: Optional[float] = None
    scenario_ended: Optional[float] = None
    scenario_status: Optional[str] = None
    request_started: Optional[float] = None
    request_ended: Optional[float] = None
    response_status: Optional[int] = None
    request_payload: Optional[Any] = None
    request_url: Optional[str] = None
    scenario_assert_message: str = ""


@dataclass(order=True)
class WorkerAccumRecord(Record):
    timestamp: float
    worker_count: int


@dataclass(order=True)
class ErrorRecord(Record):
    worker_id: Optional[int] = None
    scenario_name: Optional[str] = None
    scenario_ended: Optional[float] = None
    error: Optional[str] = None
