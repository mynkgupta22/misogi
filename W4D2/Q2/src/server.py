from fastmcp import FastMCP, Request, Response
from datetime import datetime, timedelta
import uuid
from typing import List, Dict
import pytz
from .models import Meeting, User
from .storage import MemoryStore

app = FastMCP()
store = MemoryStore()

@app.mcp("/create_meeting")
async def create_meeting(request: Request) -> Response:
    """Create a new meeting with conflict detection."""
    data = request.json
    
    # Create meeting object
    meeting = Meeting(
        id=str(uuid.uuid4()),
        title=data["title"],
        participants=data["participants"],
        start_time=datetime.fromisoformat(data["start_time"]),
        duration=data["duration"],
        preferences=data.get("preferences", {}),
        agenda=data.get("agenda", [])
    )
    
    # Check for conflicts
    conflicts = detect_scheduling_conflicts(
        meeting.participants,
        meeting.start_time,
        meeting.duration
    )
    
    if conflicts:
        return Response({
            "status": "error",
            "message": "Scheduling conflicts detected",
            "conflicts": conflicts
        })
    
    store.add_meeting(meeting)
    return Response({
        "status": "success",
        "meeting_id": meeting.id,
        "meeting": meeting.to_dict()
    })

@app.mcp("/find_optimal_slots")
async def find_optimal_slots(request: Request) -> Response:
    """Find optimal meeting time slots based on participant availability."""
    data = request.json
    participants = data["participants"]
    duration = data["duration"]
    start_time = datetime.fromisoformat(data["date_range"]["start"])
    end_time = datetime.fromisoformat(data["date_range"]["end"])
    
    available_slots = []
    current = start_time
    
    while current < end_time:
        if current.hour >= 9 and current.hour < 17:  # Business hours
            if not detect_scheduling_conflicts(participants, current, duration):
                available_slots.append(current)
        current += timedelta(minutes=30)  # 30-minute intervals
    
    return Response({
        "available_slots": [slot.isoformat() for slot in available_slots]
    })

def detect_scheduling_conflicts(
    participants: List[str],
    start_time: datetime,
    duration: int
) -> List[Dict]:
    """Detect scheduling conflicts for participants."""
    conflicts = []
    meeting_end = start_time + timedelta(minutes=duration)
    
    for participant in participants:
        user_meetings = store.get_user_meetings(participant)
        for meeting in user_meetings:
            meeting_start = meeting.start_time
            meeting_end = meeting_start + timedelta(minutes=meeting.duration)
            
            if (start_time < meeting_end and meeting_start < meeting_end):
                conflicts.append({
                    "participant": participant,
                    "conflicting_meeting": meeting.title,
                    "meeting_time": meeting_start.isoformat()
                })
    
    return conflicts

@app.mcp("/analyze_meeting_patterns")
async def analyze_meeting_patterns(request: Request) -> Response:
    """Analyze meeting patterns for a user."""
    data = request.json
    user_id = data["user_id"]
    period_days = data.get("period", 30)  # Default to 30 days
    
    end_time = datetime.now(pytz.UTC)
    start_time = end_time - timedelta(days=period_days)
    
    meetings = store.get_user_meetings_in_range(user_id, start_time, end_time)
    
    if not meetings:
        return Response({
            "message": "No meetings found in the specified period"
        })
    
    total_meetings = len(meetings)
    total_duration = sum(m.duration for m in meetings)
    avg_duration = total_duration / total_meetings
    
    # Analyze meeting distribution
    meeting_hours = {}
    for meeting in meetings:
        hour = meeting.start_time.hour
        meeting_hours[hour] = meeting_hours.get(hour, 0) + 1
    
    peak_hour = max(meeting_hours.items(), key=lambda x: x[1])[0]
    
    return Response({
        "total_meetings": total_meetings,
        "average_duration": avg_duration,
        "meetings_per_day": total_meetings / period_days,
        "peak_meeting_hour": peak_hour,
        "meeting_hour_distribution": meeting_hours
    })

@app.mcp("/generate_agenda_suggestions")
async def generate_agenda_suggestions(request: Request) -> Response:
    """Generate agenda suggestions based on meeting topic and participants."""
    data = request.json
    topic = data["meeting_topic"]
    participants = data["participants"]
    
    # Simple agenda generation based on common patterns
    common_items = [
        f"Discuss {topic}",
        "Review previous action items",
        "Team updates",
        "Next steps",
        "Action items"
    ]
    
    # Add participant-specific items
    for participant in participants:
        user_meetings = store.get_user_meetings(participant)
        if user_meetings:
            recent_meeting = max(user_meetings, key=lambda m: m.start_time)
            if recent_meeting.agenda:
                common_items.extend(recent_meeting.agenda)
    
    # Remove duplicates and limit suggestions
    unique_items = list(dict.fromkeys(common_items))[:7]
    
    return Response({
        "suggested_agenda": unique_items
    })

@app.mcp("/calculate_workload_balance")
async def calculate_workload_balance(request: Request) -> Response:
    """Calculate meeting workload distribution among team members."""
    data = request.json
    team_members = data["team_members"]
    period_days = data.get("period", 7)  # Default to 7 days
    
    end_time = datetime.now(pytz.UTC)
    start_time = end_time - timedelta(days=period_days)
    
    workload = {}
    for member in team_members:
        meetings = store.get_user_meetings_in_range(member, start_time, end_time)
        total_hours = sum(m.duration for m in meetings) / 60
        workload[member] = {
            "total_hours": total_hours,
            "meetings_count": len(meetings),
            "average_meeting_duration": total_hours * 60 / len(meetings) if meetings else 0
        }
    
    # Calculate team averages
    team_total_hours = sum(w["total_hours"] for w in workload.values())
    team_avg_hours = team_total_hours / len(team_members)
    
    return Response({
        "workload_distribution": workload,
        "team_average_hours": team_avg_hours,
        "period_days": period_days
    })

@app.mcp("/score_meeting_effectiveness")
async def score_meeting_effectiveness(request: Request) -> Response:
    """Score meeting effectiveness and provide improvement suggestions."""
    data = request.json
    meeting_id = data["meeting_id"]
    
    meeting = store.get_meeting(meeting_id)
    if not meeting:
        return Response({
            "status": "error",
            "message": "Meeting not found"
        })
    
    # Calculate effectiveness score
    score = 0.0
    suggestions = []
    
    # Duration score (0-0.3)
    if meeting.duration <= 30:
        score += 0.3
    elif meeting.duration <= 60:
        score += 0.2
    else:
        score += 0.1
        suggestions.append("Consider shorter meeting duration")
    
    # Agenda score (0-0.3)
    agenda_score = min(len(meeting.agenda) * 0.1, 0.3)
    score += agenda_score
    if agenda_score < 0.2:
        suggestions.append("Add more detailed agenda items")
    
    # Participants score (0-0.4)
    participant_count = len(meeting.participants)
    if 2 <= participant_count <= 8:
        score += 0.4
    elif participant_count < 2:
        score += 0.1
        suggestions.append("Consider adding more participants")
    else:
        score += 0.2
        suggestions.append("Consider reducing number of participants")
    
    meeting.effectiveness_score = score
    store.update_meeting(meeting)
    
    return Response({
        "meeting_id": meeting_id,
        "effectiveness_score": score,
        "suggestions": suggestions
    })

if __name__ == "__main__":
    # Add some sample users
    for user_id in ["user1", "user2", "user3"]:
        store.add_user(User(id=user_id))
    
    app.run() 