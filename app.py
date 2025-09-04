import streamlit as st
import pandas as pd
import plotly.express as px

# --- Streamlit başlığı ---
st.set_page_config(page_title="Football Dashboard", layout="wide")
st.title("⚽ Football Dashboard")

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

# Takım listesi
teams = team_details['club_name'].dropna().unique()
selected_team = st.sidebar.selectbox("Takım Seç", teams)

# Oyuncu listesi, seçilen takıma göre filtreleme
players_df = player_profiles[player_profiles['current_club_name'] == selected_team]
players_df = players_df[players_df['player_name'].notna()]
players_df['player_display_name'] = players_df['player_name'].str.split(" \(").str[0]

players = players_df['player_display_name'].unique()

if len(players) > 0:
    selected_player = st.sidebar.selectbox("Oyuncu Seç", players)
else:
    st.sidebar.warning("Seçilen takımda oyuncu bulunamadı.")
    selected_player = None

# --- Oyuncu bilgisi ---
if selected_player:
    st.subheader(f"{selected_player} Bilgileri")
    player_info = players_df[players_df['player_display_name'] == selected_player]

    if not player_info.empty:
        st.dataframe(player_info)
        player_id = player_info['player_id'].values[0]
    else:
        st.write("Seçilen oyuncuya ait profil bulunamadı.")
        player_id = None
else:
    player_id = None

# --- Oyuncu performans grafiği ---
if player_id:
    st.subheader(f"{selected_player} Performans Grafiği")
    player_stats = player_performances[player_performances['player_id'] == player_id]

    if not player_stats.empty:
        fig = px.line(player_stats, x='match_date', y='goals', title="Gol Sayısı Zamanla")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.write("Bu oyuncuya ait performans verisi bulunamadı.")

# --- Sakatlık durumu ---
if player_id:
    st.subheader(f"{selected_player} Sakatlık Durumu")
    injuries = player_injuries[player_injuries['player_id'] == player_id]
    if not injuries.empty:
        st.dataframe(injuries)
    else:
        st.write("Bu oyuncuya ait sakatlık verisi bulunamadı.")

# --- Takım detayları ---
st.subheader(f"{selected_team} Takım Detayları")
team_info = team_details[team_details['club_name'] == selected_team]
if not team_info.empty:
    st.dataframe(team_info)
else:
    st.write("Bu takıma ait detay verisi bulunamadı.")

# --- Transfer geçmişi ---
if player_id:
    st.subheader(f"{selected_player} Transfer Geçmişi")
    player_transfers = transfer_history[transfer_history['player_id'] == player_id]
    if not player_transfers.empty:
        st.dataframe(player_transfers)
    else:
        st.write("Bu oyuncuya ait transfer geçmişi bulunamadı.")
