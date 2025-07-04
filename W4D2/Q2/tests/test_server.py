import pytest
from datetime import datetime, timedelta
from src.models import Meeting, User
from src.storage import MemoryStore

@pytest.fixture
def store():
    return MemoryStore()

@pytest.fixture
def sample_users(store):
    users = [
        User(id="user1"),
        User(id="user2"),
        User(id="user3")
    ]
    for user in users:
        store.add_user(user)
    return users

@pytest.fixture
def sample_meeting():
    return Meeting(
        id="test-meeting-1",
        title="Test Meeting",
        participants=["user1", "user2"],
        start_time=datetime.now(),
        duration=30,
        agenda=["Item 1", "Item 2"]
    )

def test_add_meeting(store, sample_meeting):
    store.add_meeting(sample_meeting)
    assert store.get_meeting(sample_meeting.id) == sample_meeting
    
    # Check user calendars
    for participant in sample_meeting.participants:
        user_meetings = store.get_user_meetings(participant)
        assert sample_meeting in user_meetings

def test_get_user_meetings_in_range(store, sample_users):
    now = datetime.now()
    
    # Create meetings at different times
    meetings = [
        Meeting(
            id="meeting1",
            title="Past Meeting",
            participants=["user1"],
            start_time=now - timedelta(days=2),
            duration=30
        ),
        Meeting(
            id="meeting2",
            title="Current Meeting",
            participants=["user1"],
            start_time=now,
            duration=30
        ),
        Meeting(
            id="meeting3",
            title="Future Meeting",
            participants=["user1"],
            start_time=now + timedelta(days=2),
            duration=30
        )
    ]
    
    for meeting in meetings:
        store.add_meeting(meeting)
    
    # Test range query
    range_start = now - timedelta(days=1)
    range_end = now + timedelta(days=1)
    range_meetings = store.get_user_meetings_in_range(
        "user1",
        range_start,
        range_end
    )
    
    assert len(range_meetings) == 1
    assert range_meetings[0].id == "meeting2"

def test_update_meeting(store, sample_meeting):
    store.add_meeting(sample_meeting)
    
    # Update meeting
    updated_meeting = Meeting(
        id=sample_meeting.id,
        title="Updated Meeting",
        participants=sample_meeting.participants,
        start_time=sample_meeting.start_time,
        duration=45
    )
    
    store.update_meeting(updated_meeting)
    retrieved_meeting = store.get_meeting(sample_meeting.id)
    
    assert retrieved_meeting.title == "Updated Meeting"
    assert retrieved_meeting.duration == 45

def test_delete_meeting(store, sample_meeting):
    store.add_meeting(sample_meeting)
    store.delete_meeting(sample_meeting.id)
    
    assert store.get_meeting(sample_meeting.id) is None
    for participant in sample_meeting.participants:
        assert sample_meeting not in store.get_user_meetings(participant) 