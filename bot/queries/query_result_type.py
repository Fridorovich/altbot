from typing import Optional, Any
from enum import Enum
from vk_api.keyboard import VkKeyboard

class QueryResultStatus(Enum):
    IN_PROGRESS = "in_progress"
    FINISHED = "finished"
    ERROR = "error"
    IGNORED = "ignored"

class QueryResult:
    def __init__(
        self,
        status: QueryResultStatus,
        query = None,
        response: Optional[str] = None,
        keyboard: Optional[VkKeyboard] = None,
        error_message: Optional[str] = None
    ):
        self.status = status
        self.error_message = error_message
        self.response = response
        self.keyboard = keyboard
        self.query = query

    def is_in_progress(self) -> bool:
        return self.status == QueryResultStatus.IN_PROGRESS

    def is_finished(self) -> bool:
        return self.status == QueryResultStatus.FINISHED

    def is_error(self) -> bool:
        return self.status == QueryResultStatus.ERROR
    
    def is_ignored(self) -> bool:
        return self.status == QueryResultStatus.IGNORED
    