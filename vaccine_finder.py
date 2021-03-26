'''
:Script:       vaccine_finder.py
:Version:      1.0.2
:Release Date: 26 March 2021
:Purpose:      Finds available vaccines in a given zip/state from multiple
               sources and notifies appropriately about availability thorugh a
               easy-to-use GUI interface. 

Script Process
==============
1) Takes in zip, state, frequency information from user and or list of cities
2) Makes API calls to CVS, Walgreens and CDC and gets data back
3) Displays availability data in respective text boxes
4) A separate process thread is started right after to run the API calls based
   on given frequency. If user resubmits information, thread is killed and a 
   new one is started based on new input
5) Quit button kills the thread, destroys the GUI and quits the program

Change History
==============
==========  =======  ===================  =====================================
   Date     Version     Author                   Description
==========  =======  ===================  =====================================
2021-02-28  0.9.9    Raghu Veer Madiraju  Initial Release
2021-03-02  1.0.0    Raghu Veer Madiraju  - Text boxes allow for copying and
                                            pasting
                                          - Clarified language
2021-03-20  1.0.1    Raghu Veer Madiraju  Error handling for Walgreens
2021-03-26  1.0.2    Raghu Veer Madiraju  Updated links and added J&J vaccine
==========  =======  ===================  =====================================

Script Functions
================
'''

import json
import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog
import tkinter.scrolledtext as st
from tkinter.constants import E, FIRST, W
import threading, time
from datetime import datetime, timedelta

# library for zip code to lat and long conversion
import pgeocode

import requests.exceptions
import sys
import requests as tr

def query_caller(state, cities_list, lat, long, dates):
    '''
    Makes calls to data sources
    '''

    cdc_url = {"visit_for_more_info" : "https://vaccinefinder.org/search/"}
    cvs_url = {"visit_for_more_info": 
        "https://www.cvs.com/immunizations/covid-19-vaccine"}

    # Generating 3 new text areas so that the boxes can be essentially
    # refreshed on every call with new information

    text_area = st.ScrolledText(root, 
                            width = 45,  
                            height = 20,  
                            font = ("Calibri", 
                                    12)) 
  
    text_area.grid(row=10, column = 0, pady = 10, padx = 10)
    label_f1 = tk.Label(root, text="Availability at CVS")
    label_f1.grid(row=11, column=0, pady=5, sticky=tk.NW)

    text_area2 = st.ScrolledText(root, 
                            width = 45,  
                            height = 20,  
                            font = ("Calibri", 
                                    12)) 
  
    text_area2.grid(row=10, column = 1, pady = 10, padx = 10)
    label_f2 = tk.Label(root, text="Availability at Walgreens")
    label_f2.grid(row=11, column=1, pady=5, sticky=tk.NW)

    text_area3 = st.ScrolledText(root, 
                            width = 45,  
                            height = 20,  
                            font = ("Calibri", 
                                    12)) 
  
    text_area3.grid(row=10, column = 2, pady = 10, padx = 10)
    label_f3 = tk.Label(root, text="Availability at Other Locations")
    label_f3.grid(row=11, column=2, pady=5, sticky=tk.NW)

    # CVS

    url = 'https://www.cvs.com/immunizations/covid-19-vaccine.vaccine-status' \
        '.%s.json?vaccineinfo' % state
    
    headers = {'user-agent': 'Mozilla/5.0  Chrome/88.0.4324.153 Safari/537.36',
               'referer': 'https://www.cvs.com/immunizations/covid-19-vaccine',
               'origin': 'https://www.cvs.com',
               'content-type': 'application/json',
               'accept': 'application/json',
               'sec-fetch-dest': 'empty',
               'sec-fetch-mode': 'cors',
               'sec-fetch-site': 'same-origin',
               'path': '/immunizations/covid-19-vaccine.vaccine-status.%s.' \
                   'json?vaccineinfo' % state,
               'authority': 'www.cvs.com',
               'method': 'GET'
               }

    r = tr.get(url, headers = headers)
    response = r.json()
    
    # Checking for specific cities

    result_list = []
    city_check_list = []
    for result in response['responsePayloadData']['data'][state]:
        if not len(cities_list) == 0 and not cities_list[0] == "":
            for city in cities_list:
                if not city in str(response['responsePayloadData']['data']
                    [state]):
                    result_city = {f"Participating CVS not found in {city}" 
                        f", {state}"}
                    city_check_list.append(result_city)
                    text = json.dumps(city_check_list, indent=4,
                        sort_keys=True)
                    text_area.insert(tk.INSERT, text)
                    text_area.configure(state ='disabled')
                elif city.upper() == result['city'] and not \
                    result['status'] == "Fully Booked":
                    result_list.append(result)
        elif not result['status'] == "Fully Booked":
            result_list.append(result)

    # Displaying results based on availability
    
    if len(result_list) > 0 or len(city_check_list) > 0:
        result_list.extend(city_check_list)
        messagebox.showinfo(title="From CVS", 
                message="CVS appointments available")
        result_list.append(cvs_url)
        text = json.dumps(result_list, indent=4, sort_keys=True)
        text_area.insert(tk.INSERT, text)
        text_area.configure(state ='disabled')
    else:
        current_time = '{0:%h %d %Y %I:%M:%S %p}'.format(datetime.now())
        text = {"No CVS appointments found as of": current_time}
        text = json.dumps(text, indent=4, sort_keys=True)
        text_area.insert(tk.INSERT, text)
        text_area.configure(state ='disabled')

    # Walgreens

    url = 'https://www.walgreens.com/hcschedulersvc/svc/v1/' \
        'immunizationLocations/availability'

    payload = {"serviceId":"99","position":{"latitude":lat,"longitude":long}, \
        "appointmentAvailability":{"startDateTime":dates},"radius":25}

    headers = {'user-agent': 'Mozilla/5.0 Chrome/88.0.4324.153 Safari/537.36',
               'referer': 'https://www.walgreens.com/findcare/vaccination/' \
                   'covid-19/location-screening',
               'origin': 'https://www.walgreens.com',
               'content-type': 'application/json',
               'accept': 'application/json',
               'sec-fetch-dest': 'empty',
               'sec-fetch-mode': 'cors',
               'sec-fetch-site': 'same-origin',
               'path': '/hcschedulersvc/svc/v1/immunizationLocations/' \
                   'availability',
               'authority': 'www.walgreens.com',
               'method': 'POST'}

    r = tr.post(url, headers = headers, json = payload)
    if r.status_code == 200:
        response = r.json()
        if response['appointmentsAvailable'] == True:
            result_list.append(cdc_url)
            messagebox.showinfo(title="From Walgreens", 
                text="Walgreens Appointments available")
            text = json.dumps(text, indent=4, sort_keys=True)
            text_area2.insert(tk.INSERT, text)
            text_area2.configure(state ='disabled')
        else:
            current_time = '{0:%h %d %Y %I:%M:%S %p}'.format(datetime.now())
            text = {"No Walgreens appointments found as of": current_time}
            text = json.dumps(text, indent=4, sort_keys=True)
            text_area2.insert(tk.INSERT, text)
            text_area2.configure(state ='disabled')
    else:
        current_time = '{0:%h %d %Y %I:%M:%S %p}'.format(datetime.now())
        text = {"Walgreens functionality not working as of": current_time}
        text = json.dumps(text, indent=4, sort_keys=True)
        text_area2.insert(tk.INSERT, text)
        text_area2.configure(state ='disabled')

    # CDC - uses url parameters

    url = ("https://api.us.castlighthealth.com/vaccine-finder/" +
        "v1/provider-locations/search?")

    payload = {"medicationGuids": ["779bfe52-0dd8-4023-a183-457eb100fccc",
        "a84fb9ed-deb4-461c-b785-e17c782ef88b",
        "784db609-dc1f-45a5-bad6-8db02e79d44f"],
    "lat": lat,
    "long": long,
    "radius": 50
    }

    headers = {'User-Agent': 'Mozilla/5.0 Chrome/88.0.4324.186 Safari/537.36',
               'Host': 'api.us.castlighthealth.com',
               'Accept': 'text/html,application/xhtml+xml,application/xml;q=' \
                   '0.9,image/avif,image/webp,image/apng,*/*;q=0.8,' \
                    'application/signed-exchange;v=b3;q=0.9',
               'Sec-Fetch-Dest': 'document',
               'Sec-Fetch-Mode': 'navigate',
               'Sec-Fetch-Site': 'none',
               }

    r = tr.get(url, headers = headers, params = payload)
    response = r.json()
    result_list = []
    for result in response["providers"]:
        result_dict = {}
        if not "CVS" in result["name"] and result["in_stock"] == True:
            result_dict["name"] = result["name"]
            result_dict["city"] = result["city"]
            result_dict["distance"] = result["distance"]
            result_dict["state"] = result["state"]
            result_dict["phone"] = result["phone"]
            result_dict["address"] = result["address1"]
            result_dict["in_stock"] = result["in_stock"]
            result_list.append(result_dict)
    if len(result_list) > 0:
        messagebox.showinfo(title="From CDC", message = "Appointments at " + 
            "other locations available")
        result_list.append(cdc_url)
        text = json.dumps(result_list, indent=4, sort_keys=True)
        text_area3.insert(tk.INSERT, text)
        text_area3.configure(state ='disabled')
    else:
        current_time = '{0:%h %d %Y %I:%M:%S %p}'.format(datetime.now())
        text = {"No other appointments found as of": current_time}
        text = json.dumps(result_list, indent=4, sort_keys=True)
        text_area3.insert(tk.INSERT, text)
        text_area3.configure(state ='disabled')
        

class Job(threading.Thread):
    '''
    Using a threading object to run a repeated job based on a given interval
    '''
    def __init__(self, interval, execute, *args, **kwargs):
        threading.Thread.__init__(self)
        self.daemon = False
        self.stopped = threading.Event()
        self.interval = interval
        self.execute = execute
        self.args = args
        self.kwargs = kwargs
    def stop(self):
                self.stopped.set()
                self.join()
    def run(self):
            while not self.stopped.wait(self.interval.total_seconds()):
                self.execute(*self.args, **self.kwargs)



def get_entry_fields(entry1, entry2, entry4, entry5):
    '''
    Parses entry fields that user has input and makes calls to API call method
    '''

    # If thread is already running, kill it so a new one based on new user
    # input can be started

    global job
    try:
        job.stop()
    except:
        pass

    states = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DC", "DE", "FL", "GA", 
          "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD", 
          "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", 
          "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC", 
          "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"]
    try:
        zip_code = str(entry1.get())
    except ValueError as err:
        zip_code = simpledialog.askstring("Input", "Please input a valid zip")
        entry1.delete(0, tk.END)
        entry1.insert(0, zip_code)
    try:
        wait_time_minutes = float(entry5.get())
    except ValueError as err:
        wait_time_minutes = simpledialog.askfloat("Input", 
            "Please enter a valid number for frequency")
        entry5.delete(0, tk.END)
        entry5.insert(0, wait_time_minutes)
    
    if not len(str(zip_code)) == 5:
        zip_code = simpledialog.askstring('Input', "Please enter a valid zip")
        entry1.delete(0, tk.END)
        entry1.insert(0, zip_code)
    try:
        state = str(entry2.get()).upper()
    except:
        state = simpledialog.askstring("Input", "Enter valid state").upper()
        entry2.insert(0, state)
        entry2.insert(0, state)
        
    if not state in states:

        state = simpledialog.askstring("Input", "Enter valid state").upper()
        entry2.delete(0, tk.END)
        entry2.insert(0, state)

    # Translating zip to lat and long and validating

    nomi = pgeocode.Nominatim(country)
    lat = float(nomi.query_postal_code(zip_code)['latitude'])
    long = float(nomi.query_postal_code(zip_code)['longitude'])

    try:
        float(lat)
    except:
        zip_code = simpledialog.askstring("Input", "Enter valid zip")
        entry1.delete(0, tk.END)
        entry1.insert(0, zip_code)
        lat = float(nomi.query_postal_code(zip_code)['latitude'])
        long = float(nomi.query_postal_code(zip_code)['longitude'])
    
    if str(lat) and str(long) == "nan":
        zip_code = simpledialog.askstring("Input", "Enter valid zip")
        entry1.delete(0, tk.END)
        entry1.insert(0, zip_code)
        lat = float(nomi.query_postal_code(zip_code)['latitude'])
        long = float(nomi.query_postal_code(zip_code)['longitude'])

    # Getting cities and converting to list

    try:
        cities_list = str(entry4.get()).upper()
        cities_list = cities_list.split(',')
        cities_list = [city.strip(' ') for city in cities_list]
        
        # Making first call to catch any errors so user has 3 total chances for 
        # inputting valid data after previous entry validations

        query_caller(state, cities_list, lat, long, dates)

        wait_time_seconds = wait_time_minutes * 60

    except requests.exceptions.HTTPError as err:
        messagebox.showerror("error", str(err))
        sys_exit()
    except requests.exceptions.ConnectionError as err:
        messagebox.showerror("error", str(err))
        sys_exit()
    except requests.exceptions.Timeout as err:
        messagebox.showerror("error", str(err))
        sys_exit()
    except requests.exceptions.RequestException as err:
        messagebox.showerror("error", str(err))
        sys_exit()
    except KeyError as err:
        state = simpledialog.askstring("Input", "enter valid state: ")
        entry2.delete(0, tk.END)
        entry2.insert(0, state)
    except json.JSONDecodeError as error:
        pass
    try:
        # making second call to ensure there are no errors and if any exit

        query_caller(state, cities_list, lat, long, dates)
        wait_time_seconds = wait_time_minutes * 60
    except:
        err = 'Fatal Error, Exiting Program!'
        messagebox.showerror("Error", err)
        sys_exit()
    
    # Starting thread based on user input and interval time

    job = Job(interval=timedelta(seconds=wait_time_seconds), 
            execute=lambda arg2 = state, 
            arg3 = cities_list, arg4 = lat, arg5 = long, arg6 = dates
            : query_caller(state, cities_list, lat, long, dates))

    job.start()
    

def sys_exit():
    '''
    Exits the program gracefully
    '''

    try:
        job.stop()
    except:
        pass
    root.destroy()
    sys.exit()

if __name__ == "__main__":

    country = "US"
    dates = (datetime.today() + timedelta(days=3)).strftime ('%Y-%m-%d')

    # Creating a window called root

    root= tk.Tk()
    root.title("Vaccine Finder App")
    
    text_area0 = st.ScrolledText(root, 
                            width = 52,  
                            height = 3,  
                            font = ("Calibri", 
                                    13)) 
  
    text_area0.grid(row=9, column = 0, pady = 10, padx = 0, columnspan=2,
        sticky=tk.NW)
    cdc_url = "Sources for info: https://vaccinefinder.org/search/" \
    "\nhttps://www.cvs.com/immunizations/covid-19-vaccine\n" \
    "https://www.walgreens.com/topic/promotion/covid-vaccine.jsp"

    text_area0.insert(tk.INSERT, cdc_url)
    text_area0.configure(state ='normal', bg="yellow")
    label_f1 = tk.Label(root, text="Availability at CVS")
    label_f1.grid(row=11, column=0, pady=5, sticky=tk.NW)

    # Creating 3 text boxes at the begining that will be overlaid by later
    # slightly larger text boxes so initial window is sized correctly without
    # user having to resize once data is returned back

    text_area6 = st.ScrolledText(root, 
                            width = 35,  
                            height = 15,  
                            font = ("Calibri", 
                                    14)) 
  
    text_area6.grid(row=10, column = 0, pady = 10, padx = 0)
    text_area6.insert(tk.INSERT, "Search first to see results at CVS")
    text_area6.configure(state ='disabled')
    label_f1 = tk.Label(root, text="Availability at CVS")
    label_f1.grid(row=11, column=0, pady=5, sticky=tk.NW)

    text_area7 = st.ScrolledText(root, 
                            width = 35,  
                            height = 15,  
                            font = ("Calibri", 
                                    14)) 
  
    text_area7.grid(row=10, column = 1, pady = 10, padx = 0)
    text_area7.insert(tk.INSERT, "Search first to see results at Walgreens")
    text_area7.configure(state ='disabled')
    label_f2 = tk.Label(root, text="Availability at Walgreens")
    label_f2.grid(row=11, column=1, pady=5, sticky=tk.NW)

    text_area8 = st.ScrolledText(root, 
                            width = 35,  
                            height = 15,  
                            font = ("Calibri", 
                                    14,)) 
  
    text_area8.grid(row=10, column = 2, pady = 10, padx = 0)
    text_area8.insert(tk.INSERT, "Search first to see results at other places")
    text_area8.configure(state ='disabled')
    label_f3 = tk.Label(root, text="Availability at Other Locations")
    label_f3.grid(row=11, column=2, pady=5, sticky=tk.NW)

    # Creating labels- will stick to middle or right side of column

    label1 = tk.Label(root, text='Vaccine Finder: Shows appointments' +
         ' at CVS, Walgreens and other participating locations in state/zip',
         font = ("Calibri", 18)).grid(row=0, columnspan=3)
    
    label2 = tk.Label(root, text='Enter Zip Code', font = ("Calibri", 14)
        ).grid(row=1, sticky=E, columnspan=2)
    label3 = tk.Label(root, text='Enter State Abbreviation', font = 
        ("Calibri", 14)).grid(row=2, sticky=E, columnspan=2)

    label5 = tk.Label(root, text='Enter Cities to check (CVS only filter)',
        font = ("Calibri", 14)).grid(row=4, column=0, sticky=E, columnspan=2)
    label6 = tk.Label(root, text='If no city locations are entered' +
        ' all available cities in state are checked', font = ("Calibri", 14)
        ).grid(row=5, sticky=E, columnspan=2)
    label5 = tk.Label(root, text='Enter how often to check for open ' + 
        'appointment slots (in minutes)', font = ("Calibri", 14)
        ).grid(row=6, sticky=E, columnspan=2)

    # Creating entry boxes- will use column 2 and stick to the left

    entry1 = tk.Entry (root)
    entry1.grid(row=1, column=2, sticky=W)

    entry2 = tk.Entry (root)
    entry2.grid(row=2, column=2, sticky=W)

    entry4 = tk.Entry (root)
    entry4.grid(row=4, column=2, sticky=W)
    entry5 = tk.Entry(root)
    entry5.grid(row=6, column=2, sticky=W)

    # Creating buttons

    button1 = tk.Button (root, text='Find Availability', bg='palegreen2', 
        font=('Calibri', 11, 'bold')) 
    button1['command'] = lambda arg1 = entry1, arg2 = entry2, \
        arg4 = entry4, arg5 = entry5 : get_entry_fields(arg1, arg2, arg4, arg5)
    button1.grid(row=7, column=2, sticky=W)
    label7 = tk.Label(root, text='Checks twice automatically when "Find ' +
        'Availability" is clicked', font = ("Calibri", 14)
        ).grid(row=7, column=0, columnspan=2, sticky=E)

    button2 = tk.Button (root, text='Quit', bg='red', 
    font=('Calibri', 11, 'bold')) 
    button2['command'] = sys_exit
    button2.grid(row=7, column=2, sticky=E)
    
    # Running the root window on a loop

    root.mainloop()
