from typing import Dict, Hashable

from .records import ScenarioRecord


class RecordTable:
    def __init__(self) -> None:
        self._records: Dict[Hashable, ScenarioRecord] = {}

    def register(self, index: Hashable, record: ScenarioRecord) -> None:
        self._records[index] = record

    def delete(self, index: Hashable) -> None:
        del self._records[index]

    def get(self, index: Hashable) -> ScenarioRecord:
        return self._records[index]
