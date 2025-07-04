from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Dict, Optional

@dataclass
class Meeting:
    id: str
    title: str
    participants: List[str]
    start_time: datetime
    duration: int  # minutes
    preferences: Dict = field(default_factory=dict)
    agenda: List[str] = field(default_factory=list)
    effectiveness_score: float = 0.0
    status: str = "scheduled"

    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "title": self.title,
            "participants": self.participants,
            "start_time": self.start_time.isoformat(),
            "duration": self.duration,
            "preferences": self.preferences,
            "agenda": self.agenda,
            "effectiveness_score": self.effectiveness_score,
            "status": self.status
        }

    @classmethod
    def from_dict(cls, data: Dict) -> 'Meeting':
        data['start_time'] = datetime.fromisoformat(data['start_time'])
        return cls(**data)

@dataclass
class User:
    id: str
    timezone: str = "UTC"
    working_hours: Dict = field(default_factory=lambda: {
        "start": "09:00",
        "end": "17:00"
    })
    meeting_preferences: Dict = field(default_factory=dict)
    workload_metrics: Dict = field(default_factory=dict)

    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "timezone": self.timezone,
            "working_hours": self.working_hours,
            "meeting_preferences": self.meeting_preferences,
            "workload_metrics": self.workload_metrics
        }

    @classmethod
    def from_dict(cls, data: Dict) -> 'User':
        return cls(**data) 