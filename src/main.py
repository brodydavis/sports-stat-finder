import pandas as pd


def load_players(path="data/players.csv") -> pd.DataFrame:
    """Load the career stats CSV into a pandas DataFrame."""
    return pd.read_csv(path)


if __name__ == "__main__":
    df = load_players()
    print(f"Loaded {len(df)} players")
    print(df.head())