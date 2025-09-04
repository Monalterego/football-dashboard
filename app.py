import streamlit as st
import pandas as pd
import plotly.express as px

# --- Sayfa ayarları ---
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
teams = team_details['club_name'].dropna().unique()
selected_team = st.sidebar.selectbox("Takım Seç", teams)

players = player_profiles[player_profiles['current_club_name'] == selected_team]['player_name'].dropna()
players = players.str.split(" \(").str[0]  # Parantezli ID kısmını çıkar
selected_player = st.sidebar.selectbox("Oyuncu Seç", players)

# --- Oyuncu bilgisi ---
st.subheader(f"{selected_player} Bilgileri")
player_info = player_profiles[
    player_profiles['player_name'].notna() &
    (player_profiles['player_name'].str.split(" \(").str[0] == selected_player)
]

if not player_info.empty:
    st.dataframe(player_info)
    player_id = player_info['player_id'].values[0]
else:
    st.write("Seçilen oyuncuya ait profil bulunamadı.")
    player_id = None

# --- Oyuncu performans grafiği ---
st.subheader(f"{selected_player} Performans Grafiği")
if player_id:
    player_stats = player_performances[player_performances['player_id'] == player_id]
    if not player_stats.empty:
        fig = px.line(player_stats, x='match_date', y='goals', title="Gol Sayısı Zamanla")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.write("Bu oyuncuya ait performans verisi bulunamadı.")

# --- Sakatlık durumu ---
st.subheader(f"{selected_player} Sakatlık Durumu")
if player_id:
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
    st.write("Takım bilgisi bulunamadı.")

# --- Transfer geçmişi ---
st.subheader(f"{selected_player} Transfer Geçmişi")
if player_id:
    player_transfers = transfer_history[transfer_history['player_id'] == player_id]
    if not player_transfers.empty:
        st.dataframe(player_transfers)
    else:
        st.write("Bu oyuncuya ait transfer geçmişi bulunamadı.")
