# International Space Station (ISS) Overhead Notification Application

## **[100 Days of Code: The Complete Python Pro Bootcamp for 2023](https://www.udemy.com/course/100-days-of-code/)**

By Dr. Angela Yu

*Day 33 of 100:* API Endpoints and API Parameters

## Project Specs

Create an application that monitors the position of the International Space Station (ISS) via an API in relation to a users current latitude and longitude.

If the ISS within range to be seen by the naked eye and it is dark outside, send an email notification to go outside and look up.

This application is written with Python 3.11.

![The International Space Station Above the Earth](https://github-readme.s3.us-west-1.amazonaws.com/ISSOverheadApp.png)

### Main Features
This application tracks the current position of the International Space Station using [Open Notify's Open APIs from Space](http://open-notify.org/) data. 

In addition, using the [Sunset/Sunrise API](https://sunrise-sunset.org/), the application checks to see if it is currently night time at the user's current location to determine if the ISS can be seen by the naked eye.  

## Usage & Requirements

This project uses six libraries:
- requests
- smtplib
- time
- datetime
- dotenv
- os

### Workflow
We start by creating a while loop that delays for 60 seconds so that we can continually monitor time and locations. Within this loop we check if the location of the ISS is within 5º of the user's location and whether or not it is dark enough to see it. If both check return true, we then send an email notification:

```
while True:
    time.sleep(60)
    if iss_within_range() and is_dark():
        send_email()
```

Within each loop, we first check to see if the location of the International Space Station (ISS) is within range of the user's location by making an request API call to [Open Notify's Open APIs from Space](http://open-notify.org/) API:

```
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
```

If the ISS is within 5º of the user's location, the function returns true. If not, it returns false and the loop continues.

If the `iss_within_range()` function returns `true`, the application then checks the current time at the user's location to determine if the sky is dark enough to see the ISS with the naked eye. This is accomplished by calling the [Sunset/Sunrise API](https://sunrise-sunset.org/) and entering the user's LAT and LNG coordinates, and then comparing the user's current time against the scheduled sunset and sunrise times: 

```angular2html
def is_dark():
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
```

If it is currently dark at the user's location, the function returns true. If not, it returns false.

If the ISS is within range AND it is dark enough outside to see it, the application then sends an email notification using the `smtplib.SMTP()` function:

```angular2html
def send_email():
    with smtplib.SMTP("smtp.gmail.com", 587) as connection:
        connection.starttls()
        connection.login(user=MY_EMAIL, password=MY_EMAIL_PASSWORD)
        connection.sendmail(
            from_addr=MY_EMAIL,
            to_addrs=MY_EMAIL,
            msg=f"Subject:ISS Overhead!\n\nLook Up! It is dark and the International Space Station is overhead!"
        )
```

# Getting Started

All of the commands below should be typed into the Python terminal of your IDE (I use PyCharm for my Python Development).

First, clone the repository from Github and switch to the new directory:

    $ git clone git@github.com:shelbyblanton/iss-overhead-app.git
    
Then open the project in PyCharm.

## Set .ENV Variables

This application utilizes an `.env` file to store the following sensitive access variables:
- `MY_LAT`
- `MY_LNG`
- `MY_EMAIL`
- `MY_EMAIL_PASSWORD`

You can create this file either by typing ```touch .env``` into the PyCharm terminal, or by right-clicking on the app directory and creating a new file.

Either way, once the file is created open it and copy/paste add the following code:
```angular2html
MY_LAT=<< MY LOCATION LATITUDE >>
MY_LNG=<< MY LOCATION LONGITUDE >>
MY_EMAIL=<< MY EMAIL ADDRESS >>
MY_EMAIL_PASSWORD=<< MY EMAIL PASSWORD >>
```

### LAT/LNG Coordinates

To determine your LAT and LNG coordinates, visit [latlng.net](https://www.latlong.net/) and enter your city name and click the `Find` button. The website will then display your LAT/LNG coordinates:

![Finding your LAT/LNG coordinates at latlng.net](https://github-readme.s3.us-west-1.amazonaws.com/ISSOverHeadApp-latlng.png)

Copy your `Latitude` coordinate and replace the `<< MY LOCATION LATITUDE >>` text in the `.env` file with your latitude coordinate.

Do the same for the `Latitude` coordinate, replacing the `<< MY LOCATION LATITUDE >>` text.

Be sure that the arrows `<<` and `>>` are removed.

### Email Notifications

Next, within the `.env` file replace the `<< MY EMAIL ADDRESS >>` with an email address that you want the notification sent to.

Then replace the `<< MY EMAIL PASSWORD >>` with that email's password. The reason we store this data in an `.env` file is to protect it.

## Install Libraries and Packages
    
In the `main.py` file, click on the word `requests` in the import statement at the top of the page. Then click on the red exclamation point and click `Install package requests` to load the library:

![Install the requests package in PyCharm](https://github-readme.s3.us-west-1.amazonaws.com/package-install-requests.png)

Then do the same for the `dotenv` import by clicking on the `Install package dotenv` option:

![Install the dotenv package in PyCharm](https://github-readme.s3.us-west-1.amazonaws.com/package-install-dotenv.png)

**Setup is complete!** 

Click Run in PyCharm to see the app in action.


# Author & Credits

Programmed by **[M. Shelby Blanton](https://www.linkedin.com/in/shelbyblanton/)** under the instructional guidance of **[Dr. Angela Yu](https://www.udemy.com/user/4b4368a3-b5c8-4529-aa65-2056ec31f37e/)** via **[Udemy.com](udemy.com)**.
