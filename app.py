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

# Takımları alfabetik sırayla
teams = sorted(team_details['club_name'].unique())
selected_team = st.sidebar.selectbox("Takım Seç", teams)

# Takım ID'sini bul
team_row = team_details[team_details['club_name'] == selected_team]
team_id = team_row['club_id'].values[0]

# Oyuncuları seçilen takım ID'sine göre filtrele ve alfabetik sırala
players_df = player_profiles[player_profiles['current_club_id'] == team_id]
players = sorted(players_df['player_name'].unique())

if len(players) == 0:
    st.sidebar.warning("Seçilen takımda oyuncu bulunamadı.")
    selected_player = None
else:
    selected_player = st.sidebar.selectbox("Oyuncu Seç", players)

# --- Oyuncu bilgisi (Panini Kartı Stili, renklendirilmiş) ---
if selected_player and not players_df.empty:
    player_info = player_profiles[player_profiles['player_name'] == selected_player]
    
    if not player_info.empty:
        player_row = player_info.iloc[0]  # Tek satırlık DataFrame

        # Panini kartı için HTML + CSS (renkli)
        panini_card = f"""
        <div style="
            background: linear-gradient(135deg, #ffffff, #e0f7fa); 
            border:3px solid #0288d1; 
            border-radius:15px; 
            padding:20px; 
            width:320px;
            text-align:center;
            box-shadow: 5px 5px 15px rgba(0,0,0,0.3);
            margin-bottom:25px;
        ">
            <div style="
                background-color:#0288d1; 
                color:white; 
                padding:8px; 
                border-radius:10px;
                font-weight:bold;
                margin-bottom:10px;
            ">
                {player_row['current_club_name']}
            </div>
            <img src="{player_row['player_image_url']}" alt="{player_row['player_name']}" 
                 style="width:100%; border-radius:10px; margin-bottom:10px; border:2px solid #0288d1;">
            <h3 style="margin:5px 0; color:#d32f2f;">{player_row['player_name']}</h3>
            <p style="margin:3px 0;"><b>Pozisyon:</b> {player_row['main_position']}</p>
            <p style="margin:3px 0;"><b>Doğum Tarihi:</b> {player_row['date_of_birth']}</p>
            <p style="margin:3px 0;"><b>Boy:</b> {player_row['height']} cm</p>
            <p style="margin:3px 0;"><b>Ülke:</b> {player_row['country_of_birth']}</p>
            <div style="
                background-color:#0288d1; 
                color:white; 
                padding:5px; 
                border-radius:5px;
                margin-top:10px;
                font-weight:bold;
            ">
                Sezon Başarıları
            </div>
            <p style="margin:2px 0;"><b>Gol:</b> {player_performances[player_performances['player_id'] == player_row['player_id']]['goals'].sum()}</p>
            <p style="margin:2px 0;"><b>Asist:</b> {player_performances[player_performances['player_id'] == player_row['player_id']]['assists'].sum()}</p>
        </div>
        """
        st.markdown(panini_card, unsafe_allow_html=True)

        # --- Oyuncu performans grafiği ---
        st.subheader(f"{selected_player} Performans Grafiği")
        player_stats = player_performances[player_performances['player_id'] == player_row['player_id']]
        if not player_stats.empty:
            fig = px.line(player_stats, x='season_name', y='goals', title="Gol Sayısı Zamanla")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.write("Bu oyuncuya ait performans verisi bulunamadı.")

        # --- Sakatlık durumu ---
        st.subheader(f"{selected_player} Sakatlık Durumu")
        injuries = player_injuries[player_injuries['player_id'] == player_row['player_id']]
        st.dataframe(injuries)

        # --- Transfer geçmişi ---
        st.subheader(f"{selected_player} Transfer Geçmişi")
        player_transfers = transfer_history[transfer_history['player_id'] == player_row['player_id']]
        st.dataframe(player_transfers)
    else:
        st.write("Seçilen oyuncuya ait profil bulunamadı.")

# --- Takım detayları ---
st.subheader(f"{selected_team} Takım Detayları")
team_info = team_details[team_details['club_id'] == team_id]
st.dataframe(team_info)
