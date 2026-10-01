from datetime import date
from programs.coaching_calendar import lookup_session

def test_lookup_class_session():
    s = lookup_session(date(2026, 10, 29))
    assert s.label == "Class 2"
    assert s.topic == "Powerful Questions"

def test_lookup_orientation_day():
    s = lookup_session(date(2026, 10, 17))
    assert s.label == "Day 1"
    assert s.topic == "Beginning the Journey"

def test_lookup_unknown_date_raises():
    import pytest
    with pytest.raises(KeyError):
        lookup_session(date(2026, 11, 26))
