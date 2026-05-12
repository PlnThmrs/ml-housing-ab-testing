# tests/test_ab_router.py
from backend.services.ab_router import choose_variant


def test_same_user_gets_same_variant():
    first = choose_variant("alice")
    second = choose_variant("alice")
    assert first == second


def test_variant_is_a_or_b():
    assert choose_variant("bob") in ["A", "B"]


def test_zero_percent_b_returns_a():
    assert choose_variant("alice", traffic_b_percent=0) == "A"


def test_full_percent_b_returns_b():
    assert choose_variant("alice", traffic_b_percent=100) == "B"
