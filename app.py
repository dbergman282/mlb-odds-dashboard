import streamlit as st
import pandas as pd

st.set_page_config(page_title="MLB Odds Dashboard", layout="wide")
st.title("MLB Web Odds Viewer")

# === Refresh Button ===
if st.sidebar.button("🔄 Refresh All Data"):
    st.cache_data.clear()

# === Helper: Numeric Slider ===
def numeric_slider(df, column, label):
    min_val = float(df[column].min())
    max_val = float(df[column].max())
    return st.sidebar.slider(
        label,
        min_value=min_val,
        max_value=max_val,
        value=(min_val, max_val),
        step=(max_val - min_val) / 100
    )

# === Load Game Odds ===
@st.cache_data
def load_game_odds():
    url = "https://www.dropbox.com/scl/fi/yzjy8pwhlvxf45ccr92a4/all_game_odds.csv?rlkey=u3wz73ngkdu6ng74hbi2tstb4&dl=1"
    df = pd.read_csv(url)
    df = df[df["market"] != "spreads"]
    df = df.rename(columns={"matchup_folder": "Game", "price": "Decimal Odds"})
    df["ROI (%)"] = df["roi"] * 100
    cols = [
        "Game", "last_modified", "bookmaker", "market", "name", "Decimal Odds",
        "americanOdds", "point", "away_or_home", "prob_hit", "prob_push",
        "ROI (%)", "kelly"
    ]
    return df[cols]

# === Load Batter Props ===
@st.cache_data
def load_batter_props():
    url = "https://www.dropbox.com/scl/fi/za45vwhyl8nbtqgfpqu45/analyzed_batter_prop_df.csv?rlkey=aohu3pvszy3s1f8b6hyj6buvm&dl=1"
    df = pd.read_csv(url)
    df = df.rename(columns={"matchup_folder": "Game", "price": "Decimal Odds"})
    df["ROI (%)"] = df["roi"] * 100
    cols = [
        "Game", "last_modified", "player_id", "player_name", "bookmaker", "market",
        "name", "point", "Decimal Odds", "prob", "ROI (%)", "kelly"
    ]
    return df[cols]

# === Load Pitcher Props ===
@st.cache_data
def load_pitcher_props():
    url = "https://www.dropbox.com/scl/fi/jxwanz1h6ki5g0cx3zi5p/analyzed_pitcher_prop_df.csv?rlkey=9bebuvrznodi810tobu6o1ov8&dl=1"
    df = pd.read_csv(url)
    df = df.rename(columns={"matchup_folder": "Game", "price": "Decimal Odds"})
    df["ROI (%)"] = df["roi"] * 100
    cols = [
        "Game", "last_modified", "player_id", "player_name", "bookmaker", "market",
        "name", "point", "Decimal Odds", "prob", "ROI (%)", "kelly"
    ]
    return df[cols]

# === Load Player DFS Summary ===
@st.cache_data
def load_player_dfs_summary():
    url = "https://www.dropbox.com/scl/fi/x6nlu8z4orxmg4pft4u52/player_dfs_summary.csv?rlkey=uq9biujytslhfk5edmp0qwrya&dl=1"
    df = pd.read_csv(url)
    df = df.rename(columns={"game_key": "Game", "player_id": "Player ID"})
    return df

# === SECTION 1: Game Odds ===
df_game = load_game_odds()
st.header("All Game Odds")

st.sidebar.header("Game Odds Filters")
game_selected = st.sidebar.multiselect("Game", sorted(df_game["Game"].dropna().unique()), default=[])
market_selected = st.sidebar.multiselect("Market (Game)", sorted(df_game["market"].dropna().unique()), default=[])
bookmaker_selected = st.sidebar.multiselect("Bookmaker (Game)", sorted(df_game["bookmaker"].dropna().unique()), default=[])

roi_range_game = numeric_slider(df_game, "ROI (%)", "ROI (%) Range (Game)")
kelly_range_game = numeric_slider(df_game, "kelly", "Kelly Range (Game)")
odds_range_game = numeric_slider(df_game, "americanOdds", "American Odds Range")

filtered_game = df_game.copy()
if game_selected:
    filtered_game = filtered_game[filtered_game["Game"].isin(game_selected)]
if market_selected:
    filtered_game = filtered_game[filtered_game["market"].isin(market_selected)]
if bookmaker_selected:
    filtered_game = filtered_game[filtered_game["bookmaker"].isin(bookmaker_selected)]

filtered_game = filtered_game[
    filtered_game["ROI (%)"].between(*roi_range_game) &
    filtered_game["kelly"].between(*kelly_range_game) &
    filtered_game["americanOdds"].between(*odds_range_game)
]

st.dataframe(filtered_game, use_container_width=True)

# === SECTION 2: Batter Props ===
df_batter = load_batter_props()
st.header("Batter Props")

st.sidebar.markdown("---")
st.sidebar.header("Batter Props Filters")

game_selected_batter = st.sidebar.multiselect("Game (Batter)", sorted(df_batter["Game"].dropna().unique()), default=[])
player_names = sorted(df_batter["player_name"].dropna().unique())
selected_players = st.sidebar.multiselect("Player Name (Batter)", player_names, default=[])

bookmaker_batter = st.sidebar.multiselect("Bookmaker (Batter)", sorted(df_batter["bookmaker"].dropna().unique()), default=[])
market_batter = st.sidebar.multiselect("Market (Batter)", sorted(df_batter["market"].dropna().unique()), default=[])

roi_range_batter = numeric_slider(df_batter, "ROI (%)", "ROI (%) Range (Batter)")
kelly_range_batter = numeric_slider(df_batter, "kelly", "Kelly Range (Batter)")

filtered_batter = df_batter.copy()
if game_selected_batter:
    filtered_batter = filtered_batter[filtered_batter["Game"].isin(game_selected_batter)]
if selected_players:
    filtered_batter = filtered_batter[filtered_batter["player_name"].isin(selected_players)]
if bookmaker_batter:
    filtered_batter = filtered_batter[filtered_batter["bookmaker"].isin(bookmaker_batter)]
if market_batter:
    filtered_batter = filtered_batter[filtered_batter["market"].isin(market_batter)]

filtered_batter = filtered_batter[
    filtered_batter["ROI (%)"].between(*roi_range_batter) &
    filtered_batter["kelly"].between(*kelly_range_batter)
]

st.dataframe(filtered_batter, use_container_width=True)

# === SECTION 3: Pitcher Props ===
df_pitcher = load_pitcher_props()
st.header("Pitcher Props")

st.sidebar.markdown("---")
st.sidebar.header("Pitcher Props Filters")

game_selected_pitcher = st.sidebar.multiselect("Game (Pitcher)", sorted(df_pitcher["Game"].dropna().unique()), default=[])
player_names_pitcher = sorted(df_pitcher["player_name"].dropna().unique())
selected_players_pitcher = st.sidebar.multiselect("Player Name (Pitcher)", player_names_pitcher, default=[])

bookmaker_pitcher = st.sidebar.multiselect("Bookmaker (Pitcher)", sorted(df_pitcher["bookmaker"].dropna().unique()), default=[])
market_pitcher = st.sidebar.multiselect("Market (Pitcher)", sorted(df_pitcher["market"].dropna().unique()), default=[])

roi_range_pitcher = numeric_slider(df_pitcher, "ROI (%)", "ROI (%) Range (Pitcher)")
kelly_range_pitcher = numeric_slider(df_pitcher, "kelly", "Kelly Range (Pitcher)")

filtered_pitcher = df_pitcher.copy()
if game_selected_pitcher:
    filtered_pitcher = filtered_pitcher[filtered_pitcher["Game"].isin(game_selected_pitcher)]
if selected_players_pitcher:
    filtered_pitcher = filtered_pitcher[filtered_pitcher["player_name"].isin(selected_players_pitcher)]
if bookmaker_pitcher:
    filtered_pitcher = filtered_pitcher[filtered_pitcher["bookmaker"].isin(bookmaker_pitcher)]
if market_pitcher:
    filtered_pitcher = filtered_pitcher[filtered_pitcher["market"].isin(market_pitcher)]

filtered_pitcher = filtered_pitcher[
    filtered_pitcher["ROI (%)"].between(*roi_range_pitcher) &
    filtered_pitcher["kelly"].between(*kelly_range_pitcher)
]

st.dataframe(filtered_pitcher, use_container_width=True)

# === SECTION 4: Player DFS Summary ===
df_dfs_summary = load_player_dfs_summary()
st.header("Player DFS Summary Stats")

st.sidebar.markdown("---")
st.sidebar.header("Player DFS Filters")

game_selected_dfs = st.sidebar.multiselect(
    "Game (DFS)", sorted(df_dfs_summary["Game"].dropna().unique()), default=[]
)

name_selected_dfs = st.sidebar.multiselect(
    "Player Name (DFS)", sorted(df_dfs_summary["roster_fullName"].dropna().unique()), default=[]
)

position_selected = st.sidebar.multiselect(
    "Roster Position", sorted(df_dfs_summary["roster_rosterPosition"].dropna().unique()), default=[]
)

mean_range = numeric_slider(df_dfs_summary, "dfs_mean", "Mean DFS Points")
sd_range = numeric_slider(df_dfs_summary, "dfs_sd", "Standard Deviation (DFS)")
q95_range = numeric_slider(df_dfs_summary, "dfs_q95", "95th Percentile (DFS)")

filtered_dfs_summary = df_dfs_summary.copy()
if game_selected_dfs:
    filtered_dfs_summary = filtered_dfs_summary[filtered_dfs_summary["Game"].isin(game_selected_dfs)]
if name_selected_dfs:
    filtered_dfs_summary = filtered_dfs_summary[filtered_dfs_summary["roster_fullName"].isin(name_selected_dfs)]
if position_selected:
    filtered_dfs_summary = filtered_dfs_summary[filtered_dfs_summary["roster_rosterPosition"].isin(position_selected)]

filtered_dfs_summary = filtered_dfs_summary[
    filtered_dfs_summary["dfs_mean"].between(*mean_range) &
    filtered_dfs_summary["dfs_sd"].between(*sd_range) &
    filtered_dfs_summary["dfs_q95"].between(*q95_range)
]

st.dataframe(filtered_dfs_summary, use_container_width=True)


# === SECTION 5: Historical Tables ===
st.header("📊 Historical Props Summary")

# Batter Prop History
@st.cache_data
def load_batter_prop_history():
    url = "https://www.dropbox.com/scl/fi/cb3hcmjmd2q36x6jeisbc/batter_props_history.csv?rlkey=zr6d53mf2p7n1nh8udu1vfus9&dl=1"
    df = pd.read_csv(url)
    df = df.rename(columns={"matchup_folder": "Game"})
    return df

st.subheader("🧾 Batter Prop History")
df_batter_history = load_batter_prop_history()
st.dataframe(df_batter_history, use_container_width=True)

