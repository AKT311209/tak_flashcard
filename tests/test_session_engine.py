"""Test session engine."""

from tak_flashcard.core.session_engine import (
    Question,
    Session,
    SessionOptions,
    create_session,
)
from tak_flashcard.db.models import Word


def test_question_creation():
    """Test Question dataclass creation."""
    question = Question(
        word_id=1,
        prompt="test",
        expected_answer="kiểm tra",
        choices=["kiểm tra", "thử nghiệm"],
    )

    assert question.word_id == 1
    assert question.prompt == "test"
    assert question.expected_answer == "kiểm tra"
    assert len(question.choices) == 2
    assert not question.revealed
    assert not question.answered


def test_session_creation():
    """Test Session creation."""
    options = SessionOptions(
        mode="Endless", direction="E->V", question_count=5
    )

    session = Session(session_id=1, options=options)

    assert session.id == 1
    assert session.options.mode == "Endless"
    assert session.score == 0
    assert session.hp == 3
    assert len(session.queue) == 0


def test_session_add_question():
    """Test adding questions to session."""
    options = SessionOptions()
    session = Session(session_id=1, options=options)

    question1 = Question(
        word_id=1, prompt="test1", expected_answer="answer1"
    )
    question2 = Question(
        word_id=2, prompt="test2", expected_answer="answer2"
    )

    session.add_question(question1)
    session.add_question(question2)

    assert len(session.queue) == 2
    assert session.get_current_question() == question1


def test_session_submit_correct_answer():
    """Test submitting correct answer."""
    options = SessionOptions()
    session = Session(session_id=1, options=options)

    question = Question(
        word_id=1, prompt="test", expected_answer="kiểm tra"
    )
    session.add_question(question)

    # Submit correct answer
    is_correct = session.submit_answer("kiểm tra")

    assert is_correct
    assert question.answered
    assert question.correct
    assert session.score == 10


def test_session_submit_wrong_answer():
    """Test submitting wrong answer."""
    options = SessionOptions(initial_hp=3)
    session = Session(session_id=1, options=options)

    question = Question(
        word_id=1, prompt="test", expected_answer="kiểm tra"
    )
    session.add_question(question)

    # Submit wrong answer
    is_correct = session.submit_answer("wrong")

    assert not is_correct
    assert question.answered
    assert not question.correct
    assert session.hp == 2  # Lost 1 HP


def test_session_reveal_answer():
    """Test revealing answer."""
    options = SessionOptions(reveal_penalty_points=5, initial_hp=3)
    session = Session(session_id=1, options=options)

    question = Question(
        word_id=1, prompt="test", expected_answer="kiểm tra"
    )
    session.add_question(question)

    # Reveal answer
    answer = session.reveal_answer()

    assert answer == "kiểm tra"
    assert question.revealed
    assert session.hp == 2  # Lost 1 HP
    assert session.score == -5  # Penalty applied


def test_session_next_question():
    """Test moving to next question."""
    options = SessionOptions()
    session = Session(session_id=1, options=options)

    question1 = Question(
        word_id=1, prompt="test1", expected_answer="answer1"
    )
    question2 = Question(
        word_id=2, prompt="test2", expected_answer="answer2"
    )

    session.add_question(question1)
    session.add_question(question2)

    assert session.get_current_question() == question1

    next_q = session.next_question()
    assert next_q == question2
    assert session.current_index == 1


def test_session_end():
    """Test ending session."""
    options = SessionOptions()
    session = Session(session_id=1, options=options)

    question = Question(
        word_id=1, prompt="test", expected_answer="kiểm tra"
    )
    session.add_question(question)
    session.submit_answer("kiểm tra")

    summary = session.end_session()

    assert summary["session_id"] == 1
    assert summary["score"] == 10
    assert summary["total_questions"] == 1
    assert summary["correct_count"] == 1
    assert len(summary["results"]) == 1


def test_create_session_with_words(db_session):
    """Test creating session with words from database."""
    # Add some words to database
    words = [
        Word(word="test1", meaning_vn="kiểm tra 1", difficulty=1),
        Word(word="test2", meaning_vn="kiểm tra 2", difficulty=1),
        Word(word="test3", meaning_vn="kiểm tra 3", difficulty=2),
    ]

    for word in words:
        db_session.add(word)
    db_session.commit()

    # Create session
    options = SessionOptions(
        mode="Endless",
        direction="E->V",
        difficulty=2,
        question_count=3,
    )

    session = create_session(db_session, options)

    assert session.id > 0
    assert len(session.queue) <= 3
    assert session.options.mode == "Endless"
