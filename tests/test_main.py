import sys
from pathlib import Path

import pandas as pd
import pytest

# let the tests import main.py from the src folder
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from main import compare_players, find_player, fmt, get_rankings  # noqa: E402


def make_players() -> pd.DataFrame:
    return pd.DataFrame([
        {"name": "Alpha One", "gp": 1000, "pts": 25.0, "reb": 5.0, "ast": 5.0,
         "stl": 1.0, "blk": 1.0, "fg_pct": 50.0, "fg3_pct": 35.0, "ft_pct": 80.0},
        {"name": "Beta Two", "gp": 900, "pts": 20.0, "reb": 5.0, "ast": 8.0,
         "stl": None, "blk": 0.5, "fg_pct": 45.0, "fg3_pct": None, "ft_pct": 80.0},
    ])


def test_find_player_is_case_insensitive():
    df = make_players()
    assert find_player(df, "alpha")["name"] == "Alpha One"


def test_find_player_matches_partial_name_and_strips_spaces():
    df = make_players()
    assert find_player(df, "  two ")["name"] == "Beta Two"


def test_find_player_returns_none_when_missing():
    df = make_players()
    assert find_player(df, "zzzz") is None


def test_fmt_handles_values_suffixes_and_missing():
    assert fmt(25.0) == "25.0"
    assert fmt(50.0, "%") == "50.0%"
    assert fmt(float("nan")) == "N/A"


def test_compare_players_edges():
    df = make_players()
    table = compare_players(df.iloc[0], df.iloc[1]).set_index("Stat")

    assert table.loc["Points per game", "Edge"] == "Alpha One"
    assert table.loc["Assists per game", "Edge"] == "Beta Two"
    assert table.loc["Rebounds per game", "Edge"] == "Tie"
    assert table.loc["Steals per game", "Edge"] == "N/A"   # Beta Two has no steals data
    assert table.loc["Games played", "Edge"] == "-"        # no edge for games played

def test_get_rankings_sorts_descending():
    ranked = get_rankings(make_players(), "pts", top_n=10, min_games=0)
    assert list(ranked["name"]) == ["Alpha One", "Beta Two"]
    assert ranked.index[0] == 1


def test_get_rankings_applies_min_games():
    ranked = get_rankings(make_players(), "pts", min_games=950)
    assert list(ranked["name"]) == ["Alpha One"]


def test_get_rankings_skips_missing_stat():
    ranked = get_rankings(make_players(), "stl", min_games=0)
    assert list(ranked["name"]) == ["Alpha One"]


def test_get_rankings_rejects_unknown_stat():
    with pytest.raises(ValueError):
        get_rankings(make_players(), "bogus")