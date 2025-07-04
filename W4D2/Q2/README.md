# Smart Meeting Assistant with AI Scheduling

An MCP server that manages meetings and calendars with AI-powered features like conflict resolution, optimal time suggestions, and meeting insights analysis.

## Features

- Intelligent meeting scheduling with conflict detection
- Optimal time slot recommendations based on participant availability
- Meeting pattern analysis (frequency, duration, productivity trends)
- Automatic agenda generation from meeting history
- Participant workload balancing
- Meeting effectiveness scoring and improvement suggestions

## API Endpoints

### Meeting Management
- `create_meeting` - Schedule new meeting
- `find_optimal_slots` - AI-powered time recommendations
- `detect_scheduling_conflicts` - Conflict identification

### Analytics
- `analyze_meeting_patterns` - Meeting behavior analysis
- `generate_agenda_suggestions` - Smart agenda creation
- `calculate_workload_balance` - Meeting load distribution
- `score_meeting_effectiveness` - Productivity assessment

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the server:
```bash
python src/server.py
```

## Usage Example

```python
# Create a meeting
meeting_data = {
    "title": "Team Sync",
    "participants": ["user1", "user2"],
    "start_time": "2024-03-20T10:00:00",
    "duration": 30,
    "preferences": {"priority": "high"},
    "agenda": ["Project updates", "Blockers"]
}

# Find optimal slots
slot_request = {
    "participants": ["user1", "user2"],
    "duration": 30,
    "date_range": {
        "start": "2024-03-20T09:00:00",
        "end": "2024-03-20T17:00:00"
    }
}
```

## Data Storage
The application uses in-memory storage for the MVP version. All data is stored in Python dictionaries and will be lost when the server restarts.

## Project Structure
```
.
├── README.md
├── requirements.txt
├── src/
│   ├── server.py
│   ├── models.py
│   └── storage.py
└── tests/
    └── test_server.py
``` 