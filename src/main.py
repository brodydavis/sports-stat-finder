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


def fmt(value, suffix="") -> str:
    """Format a stat, showing N/A when it wasn't tracked in that player's era."""
    if pd.isna(value):
        return "N/A"
    return f"{value}{suffix}"


def print_summary(player: pd.Series) -> None:
    """Print a clean career summary for one player."""
    title = f"{player['name']} - career stats ({int(player['gp'])} games)"
    print()
    print(title)
    print("-" * len(title))
    print(f"Points per game:    {fmt(player['pts'])}")
    print(f"Rebounds per game:  {fmt(player['reb'])}")
    print(f"Assists per game:   {fmt(player['ast'])}")
    print(f"Steals per game:    {fmt(player['stl'])}")
    print(f"Blocks per game:    {fmt(player['blk'])}")
    print(f"Field goal %:       {fmt(player['fg_pct'], '%')}")
    print(f"3-point %:          {fmt(player['fg3_pct'], '%')}")
    print(f"Free throw %:       {fmt(player['ft_pct'], '%')}")
    print()


def main():
    df = load_players()
    player = find_player(df, input("Player name: "))
    if player is None:
        print("Player not found.")
    else:
        print_summary(player)


if __name__ == "__main__":
    main()