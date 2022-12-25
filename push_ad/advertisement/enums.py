from enum import Enum


class AdPriorityType(Enum):
    LOW = "LOW"
    MID = "MID"
    HIGH = "HIGH"

    @classmethod
    def choices(cls):
        return tuple((i.name, i.value) for i in cls)


class AdStatus(Enum):
    INITIATED = "INITIATED",
    PENDING = "PENDING",
    COMPLETED = "COMPLETED",
    FAILED = "FAILED"
    ERROR = "ERROR"

    @classmethod
    def choices(cls):
        return tuple((i.name, i.value) for i in cls)
