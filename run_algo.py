from bs4 import BeautifulSoup
import requests
import time
import json
import csv 
import datetime 

def avail_class(class_list, time_input):
    cur_day = time.strftime('%a')[:2]
    cur_time = float(time_input)
    print(cur_day, cur_time)
    
    avail_room = set()
    busy_room = set()

    for room in class_list: 
        # print(room)
        days = room['days'] 
        day_list = [days[i:i+2] for i in range(0, len(days), 2)]
        for day in day_list: 
            if cur_time < room["start_time"] or cur_time > room["end_time"]:
                avail_room.add(room['facility_id'])
            elif cur_time >= room["start_time"] and cur_time <= room["end_time"] and day == cur_day:
                busy_room.add(room['facility_id'])
    
    avail_room -= busy_room
    
    building_select = set() 

    for room in avail_room: 
        building_select.add(room.split(" ")[0])
    print(building_select)

    building_input = input("Enter building").strip().upper()
    for room in list(avail_room):
        if not room.startswith(building_input):
            avail_room.discard(room)
    
    print(avail_room)

def main():
    with open("CAS.json") as file:
        data = json.load(file)
    
    # print(data)
    time_input = input("Enter your time (HH.MM): ")
    
    # class_list = parjson(data)
    avail_class(data, time_input)

if __name__ == "__main__":
    main()