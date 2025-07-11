import streamlit as st
import json 
from datetime import datetime
from streamlit_autorefresh import st_autorefresh 

with open("QST.json") as file:
        data = json.load(file)

st.set_page_config(page_title="ClassroomFinder", layout="wide")

st.title("Classroom Finder")
st.markdown("For college and university students seeking quiet and accessible places to study, ClassroomFinder is a real-time classroom availability app that identifies unoccupied rooms across campus throughout the day. Unlike library systems or static scheduling boards, **ClassroomFinder** provides a fast, intuitive way to locate free classrooms—helping students maximize their productivity and make smarter use of existing campus space.")

#Current time 
st_autorefresh(interval=10 * 1000, key ="refresh")
now = datetime.now()
current_time = now.strftime("%I:%M %p")
current_day = now.strftime('%A')
st.markdown(f"**It is currently {current_day}, {current_time}**")

#Algo
def avail_class(class_list):
    now = datetime.now()
    cur_day = now.strftime('%a')[:2]
    cur_time = now.hour + now.minute / 60

    avail_room = set()
    busy_room = set()

    for room in class_list: 
        days = room['days'] 
        day_list = [days[i:i+2] for i in range(0, len(days), 2)]
        for day in day_list:
            if cur_time < room["start_time"] or cur_time > room["end_time"]:
                avail_room.add(room['facility_id'])
            elif room["start_time"] <= cur_time <= room["end_time"] and day == cur_day:
                busy_room.add(room['facility_id'])
   
    avail_room -= busy_room
    return sorted(avail_room)

available_room = avail_class(data)

if "qst_clicked" not in st.session_state:
      st.session_state.qst_clicked = False

st.markdown("""
    <style>
    div[data-testid="stButton"] > button {
        background-color: #ffffff;
        border: 2px solid #e0e0e0;
        border-radius: 16px;
        padding: 24px;
        width: 100%;
        text-align: middle;
        font-size: 16px;
        transition: 0.3s;
        box-shadow: 0 2px 6px rgba(0,0,0,0.05);
    }
        .pill {
        background-color: #D50000;
        color: white;
        font-weight: bold;
        border-radius: 999px;
        padding: 6px 16px;
        display: inline-block;
        font-size: 14px;
        margin-top: 12px;
    }
    div[data-testid="stButton"] > button:hover {
        background-color: #f9f9f9;
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        cursor: pointer;
    }
    </style>
""", unsafe_allow_html=True)

#Available room button 
st.markdown('<div class="card-container">', unsafe_allow_html=True)
st.markdown(f'<div class="pill">{len(available_room)} rooms available</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# QST
if st.button("🏢  \n**QST**  \nQuestrom School of Business"):
    st.session_state.qst_clicked = not st.session_state.qst_clicked
    if st.session_state.qst_clicked:
        # st.success(f"Found {len(available_room)} available room(s):")
        for room in available_room:
            st.markdown(f"""
            <div class="room-card">
                <div class="room-title">{room}</div>
            </div>
            """, unsafe_allow_html=True)



st.markdown("""
<style>
.room-card {
    border: 1px solid #E0E0E0;
    border-radius: 12px;
    padding: 20px;
    margin-bottom: 16px;
    background-color: #ffffff;
    box-shadow: 0 2px 5px rgba(0,0,0,0.05);
}
.room-title {
    font-weight: bold;
    font-size: 20px;
    color: #d50000;
    margin-bottom: 8px;
}
</style>
""", unsafe_allow_html=True)




import streamlit as st
import json 
from datetime import datetime
from streamlit_autorefresh import st_autorefresh 
import streamlit.components.v1 as components 

with open("QST.json") as file:
        data = json.load(file)

st.set_page_config(page_title="ClassroomFinder", layout="wide")

st.title("Classroom Finder")
st.markdown("For college and university students seeking quiet and accessible places to study, ClassroomFinder is a real-time classroom availability app that identifies unoccupied rooms across campus throughout the day. Unlike library systems or static scheduling boards, **ClassroomFinder** provides a fast, intuitive way to locate free classrooms—helping students maximize their productivity and make smarter use of existing campus space.")

#Current time 
st_autorefresh(interval=10 * 1000, key ="refresh")
now = datetime.now()
current_time = now.strftime("%I:%M %p")
current_day = now.strftime('%A')
st.markdown(f"**It is currently {current_day}, {current_time}**")

#ALGO DO NOT TOUCH  
def avail_class(class_list):
    now = datetime.now()
    cur_day = now.strftime('%a')[:2]
    cur_time = now.hour + now.minute / 60

    avail_room = set()
    busy_room = set()

    for room in class_list: 
        days = room['days'] 
        day_list = [days[i:i+2] for i in range(0, len(days), 2)]
        for day in day_list:
            if cur_time < room["start_time"] or cur_time > room["end_time"]:
                avail_room.add(room['facility_id'])
            elif room["start_time"] <= cur_time <= room["end_time"] and day == cur_day:
                busy_room.add(room['facility_id'])
   
    avail_room -= busy_room
    return sorted(avail_room)

available_room = avail_class(data)

# You can adjust this to reflect dynamic count, emoji, etc.
rooms_available = 12

selected = st.session_state.get("selected") == "QST"

# HTML + JS + CSS Card
components.html(f"""
<div style="
    border: 2px solid {'#D50000' if selected else '#e0e0e0'};
    border-radius: 20px;
    padding: 24px;
    text-align: center;
    width: 100%;
    cursor: pointer;
    transition: 0.2s;
    box-shadow: 0 2px 6px rgba(0,0,0,0.05);
"
    onclick="fetch('/?select=QST').then(() => window.location.reload())"
    onmouseover="this.style.boxShadow='0 4px 12px rgba(0,0,0,0.1)'"
    onmouseout="this.style.boxShadow='0 2px 6px rgba(0,0,0,0.05)'"
>
    <div style="font-size: 2em;">🏢</div>
    <h2 style="margin: 6px 0;">QST</h2>
    <p style="margin: 0;">Questrom School of Business</p>
    <div style="
        background-color: #D50000;
        color: white;
        font-weight: bold;
        border-radius: 999px;
        padding: 6px 16px;
        display: inline-block;
        font-size: 14px;
        margin-top: 16px;
    ">
        {rooms_available} rooms available
    </div>
</div>
""", height=220)

# Capture selection
query_params = st.query_params
if query_params.get("select") == ["QST"]:
    st.session_state.qst_clicked = True

# QST
if st.button("🏢  \n**QST**  \nQuestrom School of Business"):
    st.session_state.qst_clicked = not st.session_state.qst_clicked
    if st.session_state.qst_clicked:
        # st.success(f"Found {len(available_room)} available room(s):")
        for room in available_room:
            st.markdown(f"""
            <div class="room-card">
                <div class="room-title">{room}</div>
            </div>
            """, unsafe_allow_html=True)



st.markdown("""
<style>
.room-card {
    border: 1px solid #E0E0E0;
    border-radius: 12px;
    padding: 20px;
    margin-bottom: 16px;
    background-color: #ffffff;
    box-shadow: 0 2px 5px rgba(0,0,0,0.05);
}
.room-title {
    font-weight: bold;
    font-size: 20px;
    color: #d50000;
    margin-bottom: 8px;
}
</style>
""", unsafe_allow_html=True)

