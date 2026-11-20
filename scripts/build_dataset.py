import pandas as pd

raw = pd.read_csv("data/raw/Player Totals.csv")

# NBA only, and drop the combined rows for traded players ("TOT", "2TM", "3TM")
# so their per-team rows don't get double-counted
raw = raw[
    (raw["lg"] == "NBA")
    & (raw["team"] != "TOT")
    & (~raw["team"].str.contains("TM", na=False))
]

def per_game(col):
    # only count games from seasons where the stat was actually tracked
    tracked = raw[raw[col].notna()]
    return tracked.groupby("player_id")[col].sum() / tracked.groupby("player_id")["g"].sum()

def pct(made, att):
    m = raw.groupby("player_id")[made].sum()
    a = raw.groupby("player_id")[att].sum()
    return m / a.where(a > 0) * 100

out = pd.DataFrame({
    "name": raw.groupby("player_id")["player"].first(),
    "gp": raw.groupby("player_id")["g"].sum(),
    "pts": per_game("pts"),
    "reb": per_game("trb"),
    "ast": per_game("ast"),
    "stl": per_game("stl"),
    "blk": per_game("blk"),
    "fg_pct": pct("fg", "fga"),
    "fg3_pct": pct("x3p", "x3pa"),
    "ft_pct": pct("ft", "fta"),
}).round(1)

# most-played first, so name searches return the best-known match
out = out.sort_values("gp", ascending=False)
out.to_csv("data/players.csv", index=False)
print(f"Wrote {len(out)} players to data/players.csv")