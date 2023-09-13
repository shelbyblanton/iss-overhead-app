import requests
import smtplib
import time
from datetime import datetime
from dotenv import load_dotenv
import os

# Load OS variables from .env file
load_dotenv()

# Set global variables to those set in .env file
MY_LAT = int(os.getenv('MY_LAT'))
MY_LNG = int(os.getenv('MY_LNG'))
MY_EMAIL = os.getenv('MY_EMAIL')
MY_EMAIL_PASSWORD = os.getenv('MY_EMAIL_PASSWORD')


def iss_within_range():
    """
    Query the International Space Station (ISS) location API to determine if the station is within range
    of our MY_LAT and MY_LNG global variables.
    This function returns boolean true if the MY_LAT, MY_LNG are within 5 degrees of the ISS' LAT, LNG;
    boolean false if the station is not within 5 degrees.
    :return:
    """
    iss_response = requests.get(url="http://api.open-notify.org/iss-now.json")
    iss_response.raise_for_status()
    iss_data = iss_response.json()
    return MY_LAT - 5 <= iss_data["iss_position"]["latitude"] <= MY_LAT + 5 and MY_LNG - 5 <= iss_data["iss_position"]["longitude"] <= MY_LNG + 5


def is_dark():
    """
    Check to see if it is dark enough outside to view the ISS with the naked eye. Using MY_LAT, and MY_LNG, query the
    scheduled sunrise and sunset times for our location via the sunrise-sunset API, and then compare those times to the
    local time to determine if we are still in night. Returns boolean true if in night, boolean false if not.
    :return:
    """
    params = {
        "lat": MY_LAT,
        "lng": MY_LNG,
        "formatted": 0
    }
    ss_response = requests.get(url="https://api.sunrise-sunset.org/json", params=params)
    ss_response.raise_for_status()
    data = ss_response.json()
    sr_hr = int(data['results']['sunrise'].split("T")[1].split(":")[0])
    ss_hr = int(data['results']['sunset'].split("T")[1].split(":")[0])
    now_hr = datetime.now().hour
    return sr_hr <= now_hr <= ss_hr


def send_email():
    """
    If the ISS is within 5 degrees of MY_LAT,MY_LNG and it is night outside, send an email alert to go outside and look up.
    Email is sent using the smtplib.SMTP() function.
    :return:
    """
    with smtplib.SMTP("smtp.gmail.com", 587) as connection:
        connection.starttls()
        connection.login(user=MY_EMAIL, password=MY_EMAIL_PASSWORD)
        connection.sendmail(
            from_addr=MY_EMAIL,
            to_addrs=MY_EMAIL,
            msg=f"Subject:ISS Overhead!\n\nLook Up! It is dark and the International Space Station is overhead!"
        )

# Set while loop to check if the ISS is within range and it is dark outside every 60 seconds
# If it is within range, send an email notification.
while True:
    time.sleep(60)
    if iss_within_range() and is_dark():
        send_email()