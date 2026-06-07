import streamlit as st
from typing import Dict, Any

from programs.cta_calendar import scheduled_dates, lookup_session
from programs.dates import today_eastern
from programs.counters import (
    next_committed_bhakti_session,
    next_morning_rounds_session,
    next_library_live_episode,
    next_rwwa_part,
)
from programs.titles import (
    build_cta_title,
    build_rwwa_title,
    build_bhakti_sastri_title,
    build_committed_bhakti_title,
    build_morning_rounds_title,
    build_library_live_title,
)
from services.youtube import load_youtube_service, get_playlist_titles
from config import PROGRAM_BY_KEY


def _show_previous_title(playlist_id: str) -> None:
    try:
        titles = _cached_playlist_titles(playlist_id)
        if titles:
            st.caption(f"Previous upload: {titles[0]}")
    except Exception:
        pass


def _editable_title(generated: str) -> str:
    return st.text_input("YouTube title (edit if needed)", value=generated)


@st.cache_data(ttl=300)
def _cached_playlist_titles(playlist_id: str):
    """Cache playlist titles for 5 minutes to avoid hitting the API on every re-render."""
    yt = load_youtube_service()
    return get_playlist_titles(yt, playlist_id)


def render_cta_form(session_date: date) -> Dict[str, Any]:
    _show_previous_title(PROGRAM_BY_KEY["cta"].playlist_id)
    dates = scheduled_dates()
    date_options = [d for d in dates if d <= today_eastern()]
    if not date_options:
        st.error("No past CTA sessions found in the calendar.")
        return {}

    selected_date = st.selectbox(
        "Session date",
        options=date_options,
        format_func=lambda d: f"{d.strftime('%b')} {d.day}, {d.year}",
        index=len(date_options) - 1,
    )
    try:
        session = lookup_session(selected_date)
    except KeyError:
        st.error("Could not find session for selected date.")
        return {}

    st.info(f"**{session.season} — {session.session_label}:** {session.class_title}")

    recording_options = ["Full Group"] + session.facilitators
    recording_type = st.selectbox("Recording type", recording_options)

    title = _editable_title(build_cta_title(session.season, session.session_label, recording_type, selected_date))
    return {
        "session_date": selected_date,
        "session_label": session.session_label,
        "season": session.season,
        "recording_type": recording_type,
        "title": title,
    }


def render_rwwa_form(session_date: date) -> Dict[str, Any]:
    _show_previous_title(PROGRAM_BY_KEY["rwwa"].playlist_id)
    topic_title = st.text_input("Session title")
    if not topic_title:
        return {}

    with st.spinner("Checking YouTube for existing parts..."):
        try:
            titles = _cached_playlist_titles(PROGRAM_BY_KEY["rwwa"].playlist_id)
            part_num = next_rwwa_part(titles, topic_title)
        except Exception:
            part_num = 1

    part_num = st.number_input("Part number", min_value=1, value=part_num, step=1)
    title = _editable_title(build_rwwa_title(topic_title, int(part_num), session_date))
    return {"title": title, "topic_title": topic_title, "part_num": int(part_num)}


def render_bhakti_sastri_form(session_date: date) -> Dict[str, Any]:
    _show_previous_title(PROGRAM_BY_KEY["bhakti_sastri"].playlist_id)
    verses = st.text_input("Verses (e.g. 2.1-2.5)")
    part_str = st.text_input("Part number (leave blank if not needed)")
    part_num = int(part_str) if part_str.strip().isdigit() else None
    if not verses:
        return {}
    title = _editable_title(build_bhakti_sastri_title(verses, part_num, session_date))
    return {"title": title, "verses": verses, "part_num": part_num}


def render_committed_bhakti_form(session_date: date) -> Dict[str, Any]:
    _show_previous_title(PROGRAM_BY_KEY["committed_bhakti"].playlist_id)
    with st.spinner("Fetching session number from YouTube..."):
        try:
            titles = _cached_playlist_titles(PROGRAM_BY_KEY["committed_bhakti"].playlist_id)
            session_num = next_committed_bhakti_session(titles)
        except Exception:
            session_num = 1

    session_num = st.number_input("Session number", min_value=1, value=session_num, step=1)
    topics = st.text_input("Topics")
    if not topics:
        return {}
    title = _editable_title(build_committed_bhakti_title(int(session_num), topics, session_date))
    return {"title": title, "session_num": int(session_num), "topics": topics}


def render_morning_rounds_form(session_date: date) -> Dict[str, Any]:
    _show_previous_title(PROGRAM_BY_KEY["morning_rounds"].playlist_id)
    with st.spinner("Fetching session number from YouTube..."):
        try:
            titles = _cached_playlist_titles(PROGRAM_BY_KEY["morning_rounds"].playlist_id)
            session_num = next_morning_rounds_session(titles)
        except Exception:
            session_num = 1

    session_num = st.number_input("Session number", min_value=1, value=session_num, step=1)
    topic = st.text_input("Topic")
    if not topic:
        return {}
    title = _editable_title(build_morning_rounds_title(int(session_num), topic, session_date))
    return {"title": title, "session_num": int(session_num), "topic": topic}


def render_library_live_form(session_date: date) -> Dict[str, Any]:
    _show_previous_title(PROGRAM_BY_KEY["library_live"].playlist_id)
    with st.spinner("Fetching episode number from YouTube..."):
        try:
            titles = _cached_playlist_titles(PROGRAM_BY_KEY["library_live"].playlist_id)
            episode_num = next_library_live_episode(titles)
        except Exception as e:
            st.warning(f"Could not fetch episode number from YouTube: {e}")
            episode_num = 1

    episode_num = st.number_input("Episode number", min_value=1, value=episode_num, step=1)
    ep_title = st.text_input("Episode title")
    if not ep_title:
        return {}
    title = _editable_title(build_library_live_title(int(episode_num), ep_title, session_date))
    return {"title": title, "episode_num": int(episode_num), "ep_title": ep_title}


FORM_RENDERERS = {
    "cta": render_cta_form,
    "rwwa": render_rwwa_form,
    "bhakti_sastri": render_bhakti_sastri_form,
    "committed_bhakti": render_committed_bhakti_form,
    "morning_rounds": render_morning_rounds_form,
    "library_live": render_library_live_form,
}
