import streamlit as st
import json 
from datetime import datetime


st.set_page_config(page_title="ClassroomFinder", layout="wide")

#CSS STUFF START 

st.markdown("""
<style>
.card {
    display: flex;
    justify-content: flex-start;
    align-items: center;
    gap: 12px;
    padding: 12px 18px;
    margin-bottom: 12px;
    border: 1px solid #e0e0e0;
    border-radius: 12px;
    background-color: #ffffff;
    box-shadow: 0 1px 4px rgba(0,0,0,0.04);
    font-family: 'Segoe UI', sans-serif;
}

.room-label {
    font-size: 14px;
    font-weight: 600;
    color: #2e2e2e;
}

.time-label {
    font-size: 14px;
    color: #444;
}
</style>
""", unsafe_allow_html=True)

##CSS STUFF END 

building_list = [
        "CDS", 
        "QST", 
        "CGS", 
        "COM", 
        "ENG", 
        "CAS", 
        "MET", 
        "GRS", 
        "CFA", 
        "SAR", 
        "SDM", 
        "SHA", 
        "LAW", 
        "MED",
        "SPH",
        "SSW",
        "STH",
        "WED",
    ]
master_list = []

for building in building_list: 
    with open(building+".json") as file:
        data = json.load(file)
        master_list = master_list + data 
        file.close()

#Current time 
now = datetime.now()
current_time = now.strftime("%I:%M %p")
current_day = now.strftime('%A')

st.write("")
st.markdown("**ClassroomFinder @ BU**"
)

#SPACE
st.write("")

#Algo
def avail_class(class_list, selected_time, selected_day, selected_building):
    cur_day = selected_day
    cur_time = selected_time.hour + selected_time.minute / 60

    avail_room = dict()
    busy_room = set()

    for room in class_list: 
        if selected_building in room['facility_id']:  
            avail_room[room['facility_id']] = []
        elif selected_building == "all":
            avail_room[room['facility_id']] = []

    for key in avail_room: 
        for room in class_list:
            if room['facility_id'] == key:
                avail_room[key].append(room)
    
    for room in avail_room: 
        busytime_map = {
            "Mo": [],
            "Tu": [],
            "We": [],
            "Th": [],
            "Fr": [],
            "Sa": [],
            "Su": [],
        }
        freetime_map = {
            "Mo": [(0,22)],
            "Tu": [(0,22)],
            "We": [(0,22)],
            "Th": [(0,22)],
            "Fr": [(0,22)],
            "Sa": [(0,22)],
            "Su": [(0,22)],
        }
        
        room_info = avail_room[room]
        
        for meeting in room_info:
            days = meeting['days'] 
            day_list = [days[i:i+2] for i in range(0, len(days), 2)]
            for day in day_list: 
                busytime_map[day].append((meeting['start_time'], meeting['end_time']))
        for day in freetime_map: 
            busytime_map[day] = merge_intervals(busytime_map[day])
            freetime_map[day] = free_times(busytime_map[day])
        avail_room[room] = freetime_map
        room_freetime_slots = avail_room[room][cur_day]
        for freetime_slot in room_freetime_slots:
            if freetime_slot[0] <= cur_time <= freetime_slot[1]: 
                avail_room[room] = freetime_slot 
                break 
            avail_room[room] = None 
    #Remove all none values for rooms
    avail_room = {key: value for key, value in avail_room.items() if value} 
    for room in avail_room: 
        avail_for = avail_room[room][1] - cur_time
        minute_str = str(int((avail_for%1) * 60))
        hour_str = str(int(avail_for))
        avail_room[room] = "Available for "+ hour_str +" hours " + minute_str+" minutes"
    return avail_room

def merge_intervals(intervals): 
  if not intervals: 
      return [] 

  # Sort intervals based on start time 
  intervals.sort(key=lambda x: x[0]) 

  merged = [intervals[0]] 

  for current in intervals[1:]: 
      last = merged[-1] 
      # Check if there is an overlap 
      if current[0] <= last[1]:
    #Merge intervals
          merged[-1] = (last[0], max(last[1], current[1])) 
      else: 
          merged.append(current)

  return merged 

def free_times(meeting_times):
  free_times = []
  day_start = 0
  day_end = 22 # 10PM set for all  
  meeting_times = merge_intervals(meeting_times)

  current_time = day_start
  for start, end in meeting_times: 
    if current_time < start: 
        free_times.append((current_time, start)) 
    current_time = max(current_time, end) 

  # Check for free time at the end of the day 
  if current_time < day_end: 
    free_times.append((current_time, day_end)) 

  return free_times

class_map = {
    "All Buildings": "all",
    "African-American Studies": "AAS",
    "Anthropology, Philosophy, Political Science, African Studies Center": "PLS",
    "Babcock Street": "BAB",
    "Biology Research Building": "BRB",
    "CAS Religion": "REL",
    "Center for English Language & Orientation Programs": "EOP",
    "Clinical Psychology": "CLN",
    "College of Arts & Science": "CAS",
    "College of Communication": "COM",
    "College of Engineering": "ENG",
    "College of Fine Arts": "CFA",
    "College of General Studies": "CGS",
    "Engineering Manufacturing Building": "EMB",
    "Engineering Product Innovation Center": "EPC",
    "Engineering Research Annex": "ERA",
    "Engineering Research Building": "ERB",
    "English Faculty Offices": "EGL",
    "Faculty Computing & Data Sci": "CDS",
    "Fitness & Recreation Center": "FRC",
    "Fuller Building": "FLR",
    "Global Development Policy Center": "GDB",
    "History and American Studies": "HIS",
    "International Education Center": "IES",
    "International Relations Building": "IRB",
    "International Relations Center": "IRC",
    "Joan & Edgar Booth Theatre": "THA",
    "Judaic Studies Center": "JSC",
    "Kenmore Classroom Building": "KCB",
    "Life Science & Engineering Building": "LSE",
    "Math & Computer Science": "MCS",
    "Metcalf Science Center": "SCI",
    "Metropolitan College": "MET",
    "Morse Auditorium": "MOR",
    "Mugar Memorial Library": "MUG",
    "Physics Research Building": "PRB",
    "Photonics Building": "PHO",
    "Psychology": "PSY",
    "Questrom School of Business": "HAR",
    "Romance Studies, Modern Foreign Languages & Comparative Literature": "LNG",
    "Sargent College": "SAR",
    "School of Hospitality Admin": "SHA",
    "School of Law": "LAW",
    "School of Social Work": "SSW",
    "School of Theology": "STH",
    "Sociology": "SOC",
    "Stone Science Building": "STO",
    "Wheelock College of Education": "WED",
    "Yawkey Center for Student Services": "YAW",
}

day_map = {
    "Today": now.strftime('%a')[:2],
    "Monday": "Mo",
    "Tuesday": "Tu",
    "Wednesday": "We",
    "Thursday": "Th",
    "Friday": "Fr",
    "Saturday": "Sa",
    "Sunday": "Su",
}

#First level filter for building 
selected_building = st.selectbox("**Select a Building**", list(class_map.keys()))
building_abbr = class_map[selected_building]

#SPACING 
st.write("")

#Second level button filter for current availability and future availability 
left, right = st.columns(2)
if left.button("**Available Now**", use_container_width=True):
    st.session_state.show_future = False 
    cur_time = datetime.now().time()
    available_room = avail_class(master_list, cur_time, day_map['Today'], building_abbr)
    st.write(f"**At {current_day} at {current_time}, found {len(available_room)} available room(s):**")
    # st.write(available_room if available_room else "No rooms available at this time.")
    room_items = list(available_room.items())
    cols = st.columns(2)
    for i, (room, available_room[room]) in enumerate(room_items):
        with cols[i%2]:
            st.markdown(f"""
    <div class="card">
        <span class="room-label">🏫 <strong>{room}</strong></span>
        <span class="time-label">⏰ {available_room[room]}</span>
    </div>
    """, unsafe_allow_html=True)
        
if "show_future" not in st.session_state:
    st.session_state.show_future = False

if right.button("**Future availability**", use_container_width=True):
    st.session_state.show_future = True 

if st.session_state.show_future: 
    selected_day = st.selectbox("**Select a Day**", list(day_map.keys()))
    selected_time = st.time_input("**Select a Time**", value="now")
    day_abbr = day_map[selected_day]
    #Display the available list based on selected time and 
    available_room = avail_class(master_list, selected_time, day_abbr, building_abbr)
    st.write(f"**At {selected_day} at {selected_time}, found {len(available_room)} available room(s):**")
    # st.write(available_room if available_room else "No rooms available at this time.")
    room_items = list(available_room.items())
    cols = st.columns(2)
    for i, (room, available_room[room]) in enumerate(room_items):
        with cols[i%2]:
            st.markdown(f"""
    <div class="card">
        <span class="room-label">🏫 <strong>{room}</strong></span>
        <span class="time-label">⏰ {available_room[room]}</span>
    </div>
    """, unsafe_allow_html=True)

    
    
    
        # room_items = list(available_room.items())
        # cols = st.columns(2)
        # for i, (room, available_room[room]) in enumerate(room_items):
        #     with cols[i%2]:
        #             st.markdown("---")
        #             st.markdown(f" **🏫 {room}** ")
        #             st.write(f"⏰ *{available_room[room]}*")
        #             st.markdown("---")
                #st.markdown(f"""
                 #           **🏫 {room}** 
                 #           \n ⏱️ *{available_room[room]}* """)
    
    #for room, available_room[room] in available_room.items():
    #    with st.container():
     #       st.markdown(f"**🏫 {room}** \n⏱️ *{available_room[room]}* ")