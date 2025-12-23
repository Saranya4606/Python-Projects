import tkinter as tk
from geopy.geocoders import Nominatim
import pytz
from datetime import datetime
import time
from timezonefinder import TimezoneFinder
def get_timezone(location):
    geolocator = Nominatim(user_agent="timezone_locator")
    location = geolocator.geocode(location)
    if location:
        latitude = location.latitude
        longitude = location.longitude
        tz_finder = TimezoneFinder()
        timezone_str = tz_finder.timezone_at(lng=longitude, lat=latitude)
        return timezone_str
    else:
        return None
def get_current_time(timezone_str):
    timezone = pytz.timezone(timezone_str)
    time_in_timezone = datetime.now(timezone)
    return time_in_timezone.strftime('%H:%M:%S')
def update_time():
    global timezone_str
    location = location_input.get()
    if timezone_str is None:  
        timezone_str = get_timezone(location)
    if timezone_str:
        current_time = get_current_time(timezone_str)
    else:
        current_time = "Location not found"
    time_label.config(text=current_time)
    window.after(1000, update_time)
window = tk.Tk()
window.title("Animated Time Clock")
window.geometry("400x200")
time_label = tk.Label(window, font=("Helvetica", 48), fg="black")
time_label.pack(pady=30)
location_label = tk.Label(window, text="Enter your location:")
location_label.pack()
location_input = tk.Entry(window)
location_input.pack()
location_input.insert(0, "New York")
timezone_str = None
start_button = tk.Button(window, text="Start Clock", command=update_time)
start_button.pack(pady=20)
window.mainloop()