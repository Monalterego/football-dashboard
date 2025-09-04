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

# Takımlar alfabetik
teams = sorted(team_details['club_name'].unique())
selected_team = st.sidebar.selectbox("Takım Seç", teams)

# Sezon filtresi
seasons = sorted(player_performances['season_name'].dropna().unique())
selected_season = st.sidebar.selectbox("Sezon Seç", seasons)

# Competition filtresi
competitions = sorted(player_performances['competition_name'].dropna().unique())
selected_competition = st.sidebar.selectbox("Competition Seç", competitions)

# Country filtresi
countries = sorted(player_profiles['country_of_birth'].dropna().unique())
selected_country = st.sidebar.selectbox("Ülke Seç", countries)

# Position filtresi
positions = sorted(player_profiles['main_position'].dropna().unique())
selected_position = st.sidebar.selectbox("Pozisyon Seç", positions)

# Takım ID'sini bul
team_row = team_details[team_details['club_name'] == selected_team]
team_id = team_row['club_id'].values[0]

# Oyuncuları filtrele: takım + ülke + pozisyon
players_df = player_profiles[
    (player_profiles['current_club_id'] == team_id) &
    (player_profiles['country_of_birth'] == selected_country) &
    (player_profiles['main_position'] == selected_position)
]
players = sorted(players_df['player_name'].unique())

if len(players) == 0:
    st.sidebar.warning("Seçilen filtrelere uyan oyuncu bulunamadı.")
    selected_player = None
else:
    selected_player = st.sidebar.selectbox("Oyuncu Seç", players)

# --- Oyuncu bilgileri ve panini kart ---
if selected_player:
    player_info = player_profiles[player_profiles['player_name'] == selected_player]
    
    if not player_info.empty:
        # Panini kart tasarımı
        st.subheader(f"{selected_player} Bilgileri")
        card_col1, card_col2 = st.columns([1, 3])
        with card_col1:
            st.image(player_info['player_image_url'].values[0], use_column_width=True)
        with card_col2:
            st.markdown(f"**Doğum Tarihi:** {player_info['date_of_birth'].values[0]}")
            st.markdown(f"**Ülke:** {player_info['country_of_birth'].values[0]}")
            st.markdown(f"**Pozisyon:** {player_info['main_position'].values[0]}")
            st.markdown(f"**Mevcut Takım:** {player_info['current_club_name'].values[0]}")

        # --- Oyuncu performans grafiği ---
        st.subheader(f"{selected_player} Performans Grafiği")
        player_stats = player_performances[
            (player_performances['player_id'] == player_info['player_id'].values[0]) &
            (player_performances['season_name'] == selected_season) &
            (player_performances['competition_name'] == selected_competition)
        ]
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
    else:
        st.write("Seçilen oyuncuya ait profil bulunamadı.")

# --- Takım detayları ---
st.subheader(f"{selected_team} Takım Detayları")
team_info = team_details[team_details['club_id'] == team_id]
st.dataframe(team_info)
