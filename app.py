import streamlit as st
import pandas as pd
import plotly.express as px

# --- Sayfa ayarı ---
st.set_page_config(page_title="Football Dashboard", layout="wide")
st.title("⚽ Football Dashboard")

# --- Veri yükleme ---
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
teams = team_details['club_name'].unique()
selected_team = st.sidebar.selectbox("Takım Seç", teams)

players = player_profiles[player_profiles['current_club_name'] == selected_team]['player_name'].unique()
selected_player = st.sidebar.selectbox("Oyuncu Seç", players)

# --- Oyuncu bilgisi ---
st.subheader(f"{selected_player} Bilgileri")
player_info = player_profiles[player_profiles['player_name'] == selected_player]
st.dataframe(player_info[['player_name', 'position', 'current_club_name', 'height', 'date_of_birth']])

# --- Performans grafiği ---
st.subheader(f"{selected_player} Performans Grafiği")
player_stats = player_performances[player_performances['player_id'] == player_info['player_id'].values[0]]

if not player_stats.empty:
    fig = px.bar(player_stats, x='season_name', y='goals', color='competition_name', title="Gol Sayısı Sezon Bazlı")
    st.plotly_chart(fig, use_container_width=True)
else:
    st.write("Performans verisi bulunamadı.")

# --- Sakatlık durumu ---
st.subheader(f"{selected_player} Sakatlık Durumu")
injuries = player_injuries[player_injuries['player_id'] == player_info['player_id'].values[0]]
st.dataframe(injuries[['injury_reason','from_date','end_date','days_missed','games_missed']])

# --- Transfer geçmişi ---
st.subheader(f"{selected_player} Transfer Geçmişi")
player_transfers = transfer_history[transfer_history['player_id'] == player_info['player_id'].values[0]]
st.dataframe(player_transfers[['transfer_date','from_team_name','to_team_name','transfer_fee']])
