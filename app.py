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

# Takımlar alfabetik sırayla
teams = sorted(team_details['club_name'].unique())
selected_team = st.sidebar.selectbox("Takım Seç", teams)

# Takım ID ve ülke bilgisini al
team_row = team_details[team_details['club_name'] == selected_team]
team_id = team_row['club_id'].values[0]
team_country = team_row['country_name'].values[0]

# Ülke filtresi: sadece seçilen takımın ülkesi
selected_country = st.sidebar.selectbox("Ülke Seç", [team_country])

# Competition filtresi: sadece seçilen takımın oynadığı yarışmalar
competitions = team_details[team_details['club_id'] == team_id]['competition_name'].unique()
selected_competition = st.sidebar.selectbox("Competition Seç", sorted(competitions))

# Oyuncuları seçilen takım ID'sine göre filtrele ve alfabetik sırala
players_df = player_profiles[player_profiles['current_club_id'] == team_id]
players = sorted(players_df['player_name'].unique())

if len(players) == 0:
    st.sidebar.warning("Seçilen takımda oyuncu bulunamadı.")
    selected_player = None
else:
    selected_player = st.sidebar.selectbox("Oyuncu Seç", players)

# Eğer oyuncu seçildiyse sezon ve pozisyon filtrelerini daralt
if selected_player:
    player_info = player_profiles[player_profiles['player_name'] == selected_player]
    player_id = player_info['player_id'].values[0]

    # Sezon filtresi: sadece seçilen oyuncunun oynadığı sezonlar
    seasons = sorted(player_performances[player_performances['player_id'] == player_id]['season_name'].unique())
    selected_season = st.sidebar.selectbox("Sezon Seç", seasons)

    # Pozisyon filtresi: sadece seçilen oyuncunun pozisyonu
    positions = sorted(player_profiles[player_profiles['player_id'] == player_id]['main_position'].dropna().unique())
    selected_position = st.sidebar.selectbox("Pozisyon Seç", positions)
else:
    selected_season = None
    selected_position = None

# --- Oyuncu bilgileri (panini kartı) ---
if selected_player:
    if not player_info.empty:
        st.subheader(f"{selected_player} Bilgileri")
        st.image(player_info['player_image_url'].values[0], width=200)
        st.markdown(f"**Doğum Tarihi:** {player_info['date_of_birth'].values[0]}")
        st.markdown(f"**Doğum Yeri:** {player_info['place_of_birth'].values[0]}")
        st.markdown(f"**Ülke:** {player_info['country_of_birth'].values[0]}")
        st.markdown(f"**Pozisyon:** {player_info['main_position'].values[0]}")
        st.markdown(f"**Boy:** {player_info['height'].values[0]} cm")
        st.markdown(f"**Mevcut Kulüp:** {player_info['current_club_name'].values[0]}")

        # --- Oyuncu performans grafiği ---
        st.subheader(f"{selected_player} Performans Grafiği")
        player_stats = player_performances[player_performances['player_id'] == player_id]
        if selected_season:
            player_stats = player_stats[player_stats['season_name'] == selected_season]
        if not player_stats.empty:
            fig = px.line(player_stats, x='season_name', y='goals', title="Gol Sayısı Zamanla")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.write("Bu oyuncuya ait performans verisi bulunamadı.")

        # --- Sakatlık durumu ---
        st.subheader(f"{selected_player} Sakatlık Durumu")
        injuries = player_injuries[player_injuries['player_id'] == player_id]
        st.dataframe(injuries)

        # --- Transfer geçmişi ---
        st.subheader(f"{selected_player} Transfer Geçmişi")
        player_transfers = transfer_history[transfer_history['player_id'] == player_id]
        st.dataframe(player_transfers)
    else:
        st.write("Seçilen oyuncuya ait profil bulunamadı.")

# --- Takım detayları ---
st.subheader(f"{selected_team} Takım Detayları")
team_info = team_details[team_details['club_id'] == team_id]
st.dataframe(team_info)
