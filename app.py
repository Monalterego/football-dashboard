import streamlit as st
import pandas as pd
import plotly.express as px

# --- Streamlit başlığı ---
st.set_page_config(page_title="Football Analytics", layout="wide")
st.title("⚽ Football Analytics")

# --- Veri Yükleme ---
@st.cache_data
def load_data():
    player_profiles = pd.read_csv("player_profiles.csv")
    player_performances = pd.read_csv("player_performances.csv")
    player_injuries = pd.read_csv("player_injuries.csv")
    team_details = pd.read_csv("team_details.csv")
    transfer_history = pd.read_csv("transfer_history.csv")
    return player_profiles, player_performances, player_injuries, team_details, transfer_history

player_profiles, player_performances, player_injuries, team_details, transfer_history = load_data()

# --- Sidebar filtreleri ---
st.sidebar.header("Filtreler")

# Takımlar alfabetik ve searchable
teams = sorted(team_details['club_name'].unique())
selected_team = st.sidebar.selectbox("Takım Seç", teams)

# Seçilen takıma ait oyuncular alfabetik
players_df = player_profiles[player_profiles['current_club_name'] == selected_team]
players = sorted(players_df['player_name'].dropna().unique())

if players:
    selected_player = st.sidebar.selectbox("Oyuncu Seç", players)
else:
    selected_player = None
    st.sidebar.warning("Seçilen takımda oyuncu bulunamadı.")

# --- Oyuncu bilgisi ---
if selected_player:
    st.subheader(f"{selected_player} Bilgileri")
    player_info = player_profiles[player_profiles['player_name'] == selected_player]
    st.dataframe(player_info)

    # --- Oyuncu performans grafiği ---
    st.subheader(f"{selected_player} Performans Grafiği")
    player_stats = player_performances[player_performances['player_id'] == player_info['player_id'].values[0]]
    if not player_stats.empty:
        fig = px.line(player_stats, x='season_name', y='goals', title="Gol Sayısı Zamanla")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.write("Bu oyuncuya ait performans verisi bulunamadı.")

    # --- Sakatlık durumu ---
    st.subheader(f"{selected_player} Sakatlık Durumu")
    injuries = player_injuries[player_injuries['player_id'] == player_info['player_id'].values[0]]
    st.dataframe(injuries)

    # --- Transfer geçmişi ---
    st.subheader(f"{selected_player} Transfer Geçmişi")
    player_transfers = transfer_history[transfer_history['player_id'] == player_info['player_id'].values[0]]
    st.dataframe(player_transfers)

# --- Takım detayları ---
st.subheader(f"{selected_team} Takım Detayları")
team_info = team_details[team_details['club_name'] == selected_team]
st.dataframe(team_info)
