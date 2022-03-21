from typing import List, Optional

from molotov.util import stop_reason

from .formatters import Formatter
from .recorder import Recorder
from .records import Record


class Reporter:
    def __init__(self, recorder: Recorder, default_formatter: Formatter) -> None:
        self._recorder = recorder
        self._formatter = default_formatter

    def save_requests_log(self, filename: str, formatter: Optional[Formatter] = None) -> None:
        records = self._recorder.get_requests_log()
        self._save_log(filename, records, formatter)

    def save_workers_log(self, filename: str, formatter: Optional[Formatter] = None) -> None:
        records = self._recorder.get_workers_log()
        self._save_log(filename, records, formatter)

    def save_client_errors_log(self, filename: str, formatter: Optional[Formatter] = None) -> None:
        errors = stop_reason()
        self._save_log(filename, errors, formatter)

    def _save_log(self, filename: str, records: List[Record], formatter: Optional[Formatter] = None):
        if formatter is None:
            formatter = self._formatter

        with open(filename, "w") as f:
            for record in records:
                formatted = formatter.format(record)
                row = "	".join(map(str, formatted.values()))
                f.write(f"{row}\n")
