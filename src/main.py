import pandas as pd

# (column, label shown in the table, suffix)
STATS = [
    ("gp", "Games played", ""),
    ("pts", "Points per game", ""),
    ("reb", "Rebounds per game", ""),
    ("ast", "Assists per game", ""),
    ("stl", "Steals per game", ""),
    ("blk", "Blocks per game", ""),
    ("fg_pct", "Field goal %", "%"),
    ("fg3_pct", "3-point %", "%"),
    ("ft_pct", "Free throw %", "%"),
]


def load_players(path="data/players.csv") -> pd.DataFrame:
    """Load the career stats CSV into a pandas DataFrame."""
    return pd.read_csv(path)


def find_player(df: pd.DataFrame, name: str) -> pd.Series | None:
    """Return the first player whose name contains the search text (case-insensitive)."""
    matches = df[df["name"].str.contains(name.strip(), case=False, regex=False, na=False)]
    if matches.empty:
        return None
    return matches.iloc[0]


def fmt(value, suffix="") -> str:
    """Format a stat, showing N/A when it wasn't tracked in that player's era."""
    if pd.isna(value):
        return "N/A"
    return f"{value}{suffix}"


def compare_players(a: pd.Series, b: pd.Series) -> pd.DataFrame:
    """Build a side-by-side table of two players with an 'Edge' column."""
    rows = []
    for key, label, suffix in STATS:
        x, y = a[key], b[key]
        if key == "gp":
            edge = "-"  # more games isn't "better", so no edge
        elif pd.isna(x) or pd.isna(y):
            edge = "N/A"
        elif x == y:
            edge = "Tie"
        else:
            edge = a["name"] if x > y else b["name"]
        rows.append({
            "Stat": label,
            a["name"]: fmt(x, suffix),
            b["name"]: fmt(y, suffix),
            "Edge": edge,
        })
    return pd.DataFrame(rows)


# stats that can be ranked (3-point % is left out because the dataset has no
# attempt counts, so players with only a handful of threes would skew the list)
RANK_STATS = {
    "pts": "Points per game",
    "reb": "Rebounds per game",
    "ast": "Assists per game",
    "stl": "Steals per game",
    "blk": "Blocks per game",
    "fg_pct": "Field goal %",
    "ft_pct": "Free throw %",
}


def get_rankings(df: pd.DataFrame, stat: str, top_n: int = 10, min_games: int = 500) -> pd.DataFrame:
    """Return the top players for a stat, among players with at least min_games games."""
    if stat not in RANK_STATS:
        raise ValueError(f"Unknown stat '{stat}'")
    eligible = df[df["gp"] >= min_games].dropna(subset=[stat])
    top = eligible.sort_values(stat, ascending=False).head(top_n)
    result = top[["name", "gp", stat]].reset_index(drop=True)
    result.index += 1
    result.index.name = "Rank"
    return result


def ask_int(prompt: str, default: int) -> int:
    """Ask for a positive whole number, falling back to a default."""
    raw = input(prompt).strip()
    if not raw:
        return default
    if raw.isdigit() and int(raw) > 0:
        return int(raw)
    print(f"Invalid number, using {default}.")
    return default


def run_comparison(df: pd.DataFrame) -> None:
    """Prompt for two players and print the side-by-side comparison."""
    player_a = find_player(df, input("First player: "))
    player_b = find_player(df, input("Second player: "))

    if player_a is None or player_b is None:
        print("Couldn't find one or both players.")
        return
    if player_a["name"] == player_b["name"]:
        print("Please pick two different players.")
        return

    print()
    print(compare_players(player_a, player_b).to_string(index=False))
    print()


def run_rankings(df: pd.DataFrame) -> None:
    """Prompt for a stat and print the top players for it."""
    keys = list(RANK_STATS)
    print("\nStats you can rank:")
    for i, key in enumerate(keys, 1):
        print(f"  {i}. {RANK_STATS[key]}")

    choice = input("Pick a stat number: ").strip()
    if not choice.isdigit() or not 1 <= int(choice) <= len(keys):
        print("Invalid choice.")
        return
    stat = keys[int(choice) - 1]

    top_n = ask_int("How many players? (default 10): ", 10)
    min_games = ask_int("Minimum games played? (default 500): ", 500)

    ranked = get_rankings(df, stat, top_n=top_n, min_games=min_games)
    if ranked.empty:
        print("No players match those filters.")
        return

    ranked = ranked.rename(columns={"name": "Player", "gp": "Games", stat: RANK_STATS[stat]})
    print(f"\nTop {len(ranked)} by {RANK_STATS[stat]} (minimum {min_games} games)\n")
    print(ranked.to_string())
    print()


def main():
    df = load_players()
    print("1) Compare two players")
    print("2) Top player rankings")
    mode = input("Choose 1 or 2: ").strip()
    if mode == "1":
        run_comparison(df)
    elif mode == "2":
        run_rankings(df)
    else:
        print("Please enter 1 or 2.")


if __name__ == "__main__":
    main()