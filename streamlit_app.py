import streamlit as st
import json 
from datetime import datetime

building_list = ["CDS", "QST", "CGS", "COM", "ENG", "CAS"]
master_list = []

# for building in building_list: 
with open("QST.json") as file:
    data = json.load(file)
    master_list = master_list + data 
    file.close()

st.set_page_config(page_title="ClassroomFinder", layout="wide")

st.title("Classroom Finder")
st.markdown("For college and university students seeking quiet and accessible places to study, ClassroomFinder is a real-time classroom availability app that identifies unoccupied rooms across campus throughout the day. Unlike library systems or static scheduling boards, **ClassroomFinder** provides a fast, intuitive way to locate free classrooms—helping students maximize their productivity and make smarter use of existing campus space.")

#Current time 
now = datetime.now()
current_time = now.strftime("%I:%M %p")
current_day = now.strftime('%A')
st.markdown(f"**It is currently {current_day}, {current_time}**")

#Algo
def avail_class(class_list, selected_time, selected_day, selected_building):
    cur_day = selected_day
    cur_time = selected_time.hour + selected_time.minute / 60

    avail_room = dict()
    busy_room = set()

    time_map = {
        "Mo": [(0,24)],
        "Tu": [(0,24)],
        "We": [(0,24)],
        "Th": [(0,24)],
        "Fr": [(0,24)],
        "Sa": [(0,24)],
        "Su": [(0,24)],
    }

    for room in class_list: 
        avail_room[room['facility_id']] = []

    for key in avail_room: 
        for room in class_list:
            if room['facility_id'] == key:
                avail_room[key].append(room)
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
  day_end = 24 # 24/7 setup 
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

# Magic array (bit masking)
# 60 0s to represent an hour
# 60*24 will rep 1 day 
# we will map all meeting time minutes to the multiple 1's to rep busy minutes; 0's to rep free minutes 

    # for room in busy_room:
    #     avail_room.pop(room, None)
    # sorted_dict = dict(sorted(avail_room.items()))

    # if selected_building == "all":
    #     return sorted_dict 

    # filtered_building = dict()     
    
    # for key, value in sorted_dict.items():
    #     if selected_building in key :  # Example condition: key length greater than 5
    #         filtered_building[key] = value
    # return filtered_building

class_map = {
     "All Buildings": "all",
     "Computing & Data Sciences": "CDS",
     "Questrom School of Business": "HAR",
     "College of Communication": "CAS",
     "College of Communication": "COM",
     "College of Engineering": "ENG",
     "Metcalf Center (SCI)": "SCI",

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
selected_building = st.selectbox("Select a building", list(class_map.keys()))
building_abbr = class_map[selected_building]

#Second level button filter for current availability and future availability 
left, right = st.columns(2)
if left.button("Current availability", use_container_width=True):
    st.session_state.show_future = False 
    cur_time = datetime.now().time()
    available_room = avail_class(master_list, cur_time, day_map['Today'], building_abbr)
    st.write(f"### At {current_time}, found {len(available_room)} available room(s):")
    st.write(available_room if available_room else "No rooms available at this time.")

if "show_future" not in st.session_state:
    st.session_state.show_future = False

if right.button("Future availability", use_container_width=True):
    st.session_state.show_future = True 

if st.session_state.show_future: 
    selected_day = st.selectbox("Select a day", list(day_map.keys()))
    selected_time = st.time_input("Select a time", value="now")
    day_abbr = day_map[selected_day]
    #Display the available list based on selected time and 
    available_room = avail_class(master_list, selected_time, day_abbr, building_abbr)
    st.write(f"### At {selected_time}, found {len(available_room)} available room(s):")
    st.write(available_room if available_room else "No rooms available at this time.")

# if selected_time: 
    # available_room = avail_class(master_list, selected_time, day_abbr, building_abbr)
    # st.write(f"### At {selected_time}, found {len(available_room)} available room(s):")
    # st.write(available_room if available_room else "No rooms available at this time.")

# if "qst_clicked" not in st.session_state:
#       st.session_state.qst_clicked = False

# st.markdown("""
#     <style>
#     div[data-testid="stButton"] > button {
#         background-color: #ffffff;
#         border: 2px solid #e0e0e0;
#         border-radius: 16px;
#         padding: 24px;
#         width: 100%;
#         text-align: middle;
#         font-size: 16px;
#         transition: 0.3s;
#         box-shadow: 0 2px 6px rgba(0,0,0,0.05);
#     }
#         .pill {
#         background-color: #D50000;
#         color: white;
#         font-weight: bold;
#         border-radius: 999px;
#         padding: 6px 16px;
#         display: inline-block;
#         font-size: 14px;
#         margin-top: 12px;
#     }
#     div[data-testid="stButton"] > button:hover {
#         background-color: #f9f9f9;
#         transform: translateY(-2px);
#         box-shadow: 0 4px 12px rgba(0,0,0,0.1);
#         cursor: pointer;
#     }
#     </style>
# """, unsafe_allow_html=True)

# #Available room button 
# st.markdown('<div class="card-container">', unsafe_allow_html=True)
# st.markdown(f'<div class="pill">{len(available_room)} rooms available</div>', unsafe_allow_html=True)
# st.markdown('</div>', unsafe_allow_html=True)

# #QST Card 
# if st.button("🏢  \n**QST**  \nQuestrom School of Business"):
#     st.session_state.qst_clicked = not st.session_state.qst_clicked
#     if st.session_state.qst_clicked:
#         st.success(f"Found {len(available_room)} available room(s):")
#         for room in available_room:
#             st.markdown(f"""
#             <div class="room-card">
#                 <div class="room-title">{room}</div>
#             </div>
#             """, unsafe_allow_html=True)


# st.markdown("""
# <style>
# .room-card {
#     border: 1px solid #E0E0E0;
#     border-radius: 12px;
#     padding: 20px;
#     margin-bottom: 16px;
#     background-color: #ffffff;
#     box-shadow: 0 2px 5px rgba(0,0,0,0.05);
# }
# .room-title {
#     font-weight: bold;
#     font-size: 20px;
#     color: #d50000;
#     margin-bottom: 8px;
# }
# </style>
# """, unsafe_allow_html=True)