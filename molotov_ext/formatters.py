from abc import ABC, abstractmethod
from dataclasses import fields
from typing import Any, Dict

from .records import Record, ScenarioRecord


class Formatter(ABC):
    @abstractmethod
    def format(self, record: Record) -> Dict[str, Any]:
        pass


class DefaultFormatter(Formatter):
    def format(self, record: Record) -> Dict[str, Any]:
        return {x.name: getattr(record, x.name) for x in fields(record)}


class PhantomFormatter(Formatter):
    def format(self, record: Record) -> Dict[str, Any]:
        assert isinstance(record, ScenarioRecord)
        request_time = record.request_ended - record.request_started
        return {
            "time": int(record.request_started * 1000) / 1000,
            "tag": record.scenario_name,
            "interval_real": int(request_time * 10 ** 6),
            "connect_time": 0,
            "send_time": 0,
            "latency": 0,
            "receive_time": 0,
            "interval_event": 0,
            "size_out": 0,
            "size_in": 0,
            "net_code": 0 if record.scenario_status == "SUCCESS" else 1,
            "proto_code": record.response_status,
        }


class GatlingFormatter(Formatter):
    def format(self, record: Record) -> Dict[str, Any]:
        assert isinstance(record, ScenarioRecord)

        request_payload = ""
        if record.request_payload is not None:
            assert isinstance(record.request_payload, str)
            request_payload = record.request_payload

        return {
            "row_type": "REQUEST",  # Единственный тип записи из simulation.log, который использует Perfberry
            "simulation_name": "",  # Не используется в Perfberry
            "worker_id": record.worker_id,
            "group_name": "",  # Не используется в Perfberry
            "scenario_name": record.scenario_name,
            "start_time": int(record.request_started * 1000),
            "end_time": int(record.request_ended * 1000),
            "status": "OK" if record.scenario_status == "SUCCESS" else "KO",
            "status_exc_message": record.scenario_assert_message,
            "status_code": record.response_status,
            "url": record.request_url,
            "payload": request_payload,
        }
