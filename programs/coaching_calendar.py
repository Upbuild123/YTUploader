from datetime import date
from dataclasses import dataclass
from typing import List, Dict


@dataclass
class CoachingSession:
    date: date
    label: str
    topic: str


COACHING_CALENDAR: List[CoachingSession] = [
    CoachingSession(date(2026, 10, 17), "Day 1", "Beginning the Journey"),
    CoachingSession(date(2026, 10, 18), "Day 2", "The Foundations of Upbuild Coaching and the Meta-Skills"),
    CoachingSession(date(2026, 10, 22), "Class 1", "Listening and Curiosity"),
    CoachingSession(date(2026, 10, 29), "Class 2", "Powerful Questions"),
    CoachingSession(date(2026, 11, 5),  "Class 3", "Let's Make It Real"),
    CoachingSession(date(2026, 11, 12), "Class 4", "Structuring a Coaching Session"),
    CoachingSession(date(2026, 11, 19), "Class 5", "The Client Agenda, Part 1. Presenting and Deeper Agendas"),
    CoachingSession(date(2026, 12, 3),  "Class 6", "Deepening Action"),
    CoachingSession(date(2026, 12, 10), "Class 7", "Working with Values"),
    CoachingSession(date(2026, 12, 17), "Class 8", "Let's Make It Real"),
    CoachingSession(date(2027, 1, 7),   "Class 9", "The Client Agenda, Part 2 (Transformational Agenda)"),
    CoachingSession(date(2027, 1, 14),  "Class 10", "Let's Make It Real"),
    CoachingSession(date(2027, 1, 21),  "Class 11", "Coaching the Person, Not the Problem"),
    CoachingSession(date(2027, 1, 28),  "Class 12", "Turning Up the Heat"),
    CoachingSession(date(2027, 2, 4),   "Class 13", "The Business of Coaching"),
    CoachingSession(date(2027, 2, 11),  "Class 14", "Acknowledging and Championing"),
    CoachingSession(date(2027, 2, 18),  "Class 15", "Wisdom of the Body and Emotions"),
    CoachingSession(date(2027, 2, 25),  "Class 16", "Intuition"),
    CoachingSession(date(2027, 3, 4),   "Class 17", "Working with the Inner Critic, Part 1"),
    CoachingSession(date(2027, 3, 11),  "Class 18", "Working with the Inner Critic, Part 2"),
    CoachingSession(date(2027, 3, 18),  "Class 19", "Let's Make It Real"),
    CoachingSession(date(2027, 3, 25),  "Class 20", "The Cycle of Transformation"),
    CoachingSession(date(2027, 4, 1),   "Class 21", "Identity in Coaching"),
    CoachingSession(date(2027, 4, 8),   "Class 22", "Working with Controlling Consciousness"),
    CoachingSession(date(2027, 4, 15),  "Class 23", "Visioning"),
    CoachingSession(date(2027, 4, 22),  "Class 24", "Your Future Self"),
    CoachingSession(date(2027, 4, 24),  "Day 3", "The Coach's Stand"),
    CoachingSession(date(2027, 4, 25),  "Day 4", "Completion and Celebration"),
]

_CALENDAR_BY_DATE: Dict[date, CoachingSession] = {s.date: s for s in COACHING_CALENDAR}


def lookup_session(d: date) -> CoachingSession:
    """Return the CoachingSession for a given date. Raises KeyError if not found."""
    if d not in _CALENDAR_BY_DATE:
        raise KeyError(f"No Coaching Training session found for {d}. Check coaching_calendar.py.")
    return _CALENDAR_BY_DATE[d]


def scheduled_dates() -> List[date]:
    """Return all Coaching Training session dates in chronological order."""
    return sorted(_CALENDAR_BY_DATE.keys())
