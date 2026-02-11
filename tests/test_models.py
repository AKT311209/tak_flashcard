"""Test database models."""

from tak_flashcard.db.models import Setting, Session, SessionResult, Word


def test_create_word(db_session):
    """Test creating a word."""
    word = Word(
        word="test",
        meaning_vn="kiểm tra",
        pos="noun",
        difficulty=1,
        tags="test",
    )

    db_session.add(word)
    db_session.commit()

    # Query back
    result = db_session.query(Word).filter(Word.word == "test").first()
    assert result is not None
    assert result.word == "test"
    assert result.meaning_vn == "kiểm tra"
    assert result.difficulty == 1


def test_create_session(db_session):
    """Test creating a session."""
    session = Session(
        mode="Endless",
        direction="E->V",
        start_ts="2024-01-01T00:00:00",
        score=100,
        total_questions=10,
    )

    db_session.add(session)
    db_session.commit()

    # Query back
    result = db_session.query(Session).first()
    assert result is not None
    assert result.mode == "Endless"
    assert result.score == 100


def test_create_session_result(db_session):
    """Test creating a session result."""
    # Create word and session first
    word = Word(word="test", meaning_vn="kiểm tra", difficulty=1)
    session = Session(
        mode="Endless",
        direction="E->V",
        start_ts="2024-01-01T00:00:00",
    )

    db_session.add(word)
    db_session.add(session)
    db_session.commit()

    # Create result
    result = SessionResult(
        session_id=session.id,
        word_id=word.id,
        asked_text="test",
        expected_answer="kiểm tra",
        given_answer="kiểm tra",
        correct=1,
        revealed=0,
        penalty=0,
    )

    db_session.add(result)
    db_session.commit()

    # Query back
    query_result = db_session.query(SessionResult).first()
    assert query_result is not None
    assert query_result.correct == 1
    assert query_result.word_id == word.id


def test_create_setting(db_session):
    """Test creating a setting."""
    setting = Setting(key="volume", value="0.7")

    db_session.add(setting)
    db_session.commit()

    # Query back
    result = db_session.query(Setting).filter(Setting.key == "volume").first()
    assert result is not None
    assert result.value == "0.7"
