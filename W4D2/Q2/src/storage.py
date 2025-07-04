from typing import List, Dict, Optional
from datetime import datetime, timedelta
from .models import Meeting, User

class MemoryStore:
    def __init__(self):
        self.meetings: Dict[str, Meeting] = {}
        self.users: Dict[str, User] = {}
        self.user_calendars: Dict[str, List[Meeting]] = {}

    def add_meeting(self, meeting: Meeting) -> None:
        """Add a meeting to storage and update user calendars."""
        self.meetings[meeting.id] = meeting
        for participant in meeting.participants:
            if participant not in self.user_calendars:
                self.user_calendars[participant] = []
            self.user_calendars[participant].append(meeting)

    def get_meeting(self, meeting_id: str) -> Optional[Meeting]:
        """Get a meeting by ID."""
        return self.meetings.get(meeting_id)

    def get_user_meetings(self, user_id: str) -> List[Meeting]:
        """Get all meetings for a user."""
        return self.user_calendars.get(user_id, [])

    def add_user(self, user: User) -> None:
        """Add a user to storage."""
        self.users[user.id] = user
        if user.id not in self.user_calendars:
            self.user_calendars[user.id] = []

    def get_user(self, user_id: str) -> Optional[User]:
        """Get a user by ID."""
        return self.users.get(user_id)

    def get_user_meetings_in_range(
        self, 
        user_id: str, 
        start_time: datetime, 
        end_time: datetime
    ) -> List[Meeting]:
        """Get all meetings for a user within a time range."""
        meetings = self.get_user_meetings(user_id)
        return [
            m for m in meetings 
            if (m.start_time >= start_time and 
                m.start_time + timedelta(minutes=m.duration) <= end_time)
        ]

    def update_meeting(self, meeting: Meeting) -> None:
        """Update an existing meeting."""
        if meeting.id not in self.meetings:
            raise KeyError(f"Meeting {meeting.id} not found")
        
        # Remove from user calendars
        old_meeting = self.meetings[meeting.id]
        for participant in old_meeting.participants:
            if participant in self.user_calendars:
                self.user_calendars[participant] = [
                    m for m in self.user_calendars[participant] 
                    if m.id != meeting.id
                ]
        
        # Add updated meeting
        self.add_meeting(meeting)

    def delete_meeting(self, meeting_id: str) -> None:
        """Delete a meeting and remove it from user calendars."""
        if meeting_id not in self.meetings:
            return
        
        meeting = self.meetings[meeting_id]
        for participant in meeting.participants:
            if participant in self.user_calendars:
                self.user_calendars[participant] = [
                    m for m in self.user_calendars[participant] 
                    if m.id != meeting_id
                ]
        
        del self.meetings[meeting_id] 