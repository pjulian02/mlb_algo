"""
@AUTHOR:: Philip Julian
@CREATED_DATE: 5 May 2023
@PURPOSE: Contains all of the commonly used variables for the program
@TODO: None
"""
import mysql.connector
from datetime import datetime, timedelta

"""MYSQL Variables"""
CONFIG = {
    "host": "3.129.8.223",
    "user": "philip",
    "password": "W@rD@!$3@g13",
    "database": "mlb_algo",
}
CONNECTION = mysql.connector.connect(
    **CONFIG
)  # Tests connection to the mysql server running on AWS
CURSOR = CONNECTION.cursor()


"""URL List Here"""
FANGRAPHS_HITTING_URL = "https://www.fangraphs.com/leaders.aspx?pos=all&stats=bat&lg=all&qual=0&type=c,13,50,38,52,211&season=2023&month=3&season1=2023&ind=0&team=0,ts&rost=0&age=0&filter=&players=0&startdate=2023-01-01&enddate=2023-12-31"
MLB_HITTING_URL = "https://www.mlb.com/stats/team?timeframe=-29"
FANGRAPHS_BASIC_HITTING_URL_FI = f"https://www.fangraphs.com/leaders/splits-leaderboards?splitArr=44&splitArrPitch=&position=B&autoPt=false&splitTeams=false&type=c,13,61,292,291,304&startDate={(datetime.now() - timedelta(days=30)).strftime('%Y-%-m-%-d')}&endDate={(datetime.now() - timedelta(days=1)).strftime('%Y-%-m-%-d')}&players=&filter=&groupBy=season&wxTemperature=&wxPressure=&wxAirDensity=&wxElevation=&wxWindSpeed=&sort=1,1&statType=team&statgroup=1"
FANGRAPHS_ADVANCED_HITTING_URL_FI = f"https://www.fangraphs.com/leaders/splits-leaderboards?splitArr=44&splitArrPitch=&position=B&autoPt=false&splitTeams=false&type=c,13,61,292,291,304&startDate={(datetime.now() - timedelta(days=30)).strftime('%Y-%-m-%-d')}&endDate={(datetime.now() - timedelta(days=1)).strftime('%Y-%-m-%-d')}&players=&filter=&groupBy=season&wxTemperature=&wxPressure=&wxAirDensity=&wxElevation=&wxWindSpeed=&sort=1,1&statType=team&statgroup=2"
FANGRAPHS_BATTED_HITTING_URL_FI = f"https://www.fangraphs.com/leaders/splits-leaderboards?splitArr=44&splitArrPitch=&position=B&autoPt=false&splitTeams=false&type=c,13,61,292,291,304&startDate={(datetime.now() - timedelta(days=30)).strftime('%Y-%-m-%-d')}&endDate={(datetime.now() - timedelta(days=1)).strftime('%Y-%-m-%-d')}&players=&filter=&groupBy=season&wxTemperature=&wxPressure=&wxAirDensity=&wxElevation=&wxWindSpeed=&sort=1,1&statType=team&statgroup=3"

FANGRAPHS_STARTING_URL = "https://www.fangraphs.com/leaders.aspx?pos=all&stats=sta&lg=all&qual=0&type=c,36,38,42,109,122,117&season=2023&month=3&season1=2023&ind=0&team=0&rost=0&age=0&filter=&players=0&page=1_1000"

FANGRAPHS_RELIEF_URL = "https://www.fangraphs.com/leaders.aspx?pos=all&stats=rel&lg=all&qual=0&type=c,36,38,42,109,122,117&season=2023&month=3&season1=2023&ind=0&team=0,ts&rost=0&age=0&filter=&players=0&startdate=&enddate="

# betting_url = "https://www.lines.com/betting/mlb/odds/book-24"
# mlb_hitting_nrfiyrfi = "https://www.mlb.com/stats/team?split=i01"

#TESTING