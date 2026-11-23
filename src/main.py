import pandas as pd


def load_players(path="data/players.csv") -> pd.DataFrame:
    """Load the career stats CSV into a pandas DataFrame."""
    return pd.read_csv(path)


def find_player(df: pd.DataFrame, name: str) -> pd.Series | None:
    """Return the first player whose name contains the search text (case-insensitive)."""
    matches = df[df["name"].str.contains(name.strip(), case=False, regex=False, na=False)]
    if matches.empty:
        return None
    return matches.iloc[0]


if __name__ == "__main__":
    df = load_players()
    player = find_player(df, input("Player name: "))
    if player is None:
        print("Player not found.")
    else:
        print(player)