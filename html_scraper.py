"""CONSTANTS"""
from constants import (
    CURSOR,
    CONNECTION,
    MLB_HITTING_URL,
    FANGRAPHS_HITTING_URL,
    FANGRAPHS_BASIC_HITTING_URL_FI,
    FANGRAPHS_ADVANCED_HITTING_URL_FI,
    FANGRAPHS_BATTED_HITTING_URL_FI,
    FANGRAPHS_RELIEF_URL,
    FANGRAPHS_STARTING_URL,
)

"""FILES"""
# from sql_writer import sql_writer as sw

"""LIBRARIES"""
import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression


class retrieve_mlb_data:
    def __init__(self) -> None:
        self.team_abbreviations = {
            "Diamondbacks": "ARI",
            "Braves": "ATL",
            "Orioles": "BAL",
            "Red Sox": "BOS",
            "Cubs": "CHC",
            "White Sox": "CHW",
            "Reds": "CIN",
            "Guardians": "CLE",
            "Rockies": "COL",
            "Tigers": "DET",
            "Astros": "HOU",
            "Royals": "KCR",
            "Angels": "LAA",
            "Dodgers": "LAD",
            "Marlins": "MIA",
            "Brewers": "MIL",
            "Twins": "MIN",
            "Mets": "NYM",
            "Yankees": "NYY",
            "Athletics": "OAK",
            "Phillies": "PHI",
            "Pirates": "PIT",
            "Padres": "SDP",
            "Mariners": "SEA",
            "Giants": "SFG",
            "Cardinals": "STL",
            "Rays": "TBR",
            "Rangers": "TEX",
            "Blue Jays": "TOR",
            "Nationals": "WSN",
            "Arizona Diamondbacks": "ARI",
            "Atlanta Braves": "ATL",
            "Baltimore Orioles": "BAL",
            "Boston Red Sox": "BOS",
            "Chicago Cubs": "CHC",
            "Chicago White Sox": "CHW",
            "Cincinnati Reds": "CIN",
            "Cleveland Guardians": "CLE",
            "Colorado Rockies": "COL",
            "Detroit Tigers": "DET",
            "Houston Astros": "HOU",
            "Kansas City Royals": "KCR",
            "Los Angeles Angels": "LAA",
            "Los Angeles Dodgers": "LAD",
            "Miami Marlins": "MIA",
            "Milwaukee Brewers": "MIL",
            "Minnesota Twins": "MIN",
            "New York Mets": "NYM",
            "New York Yankees": "NYY",
            "Oakland Athletics": "OAK",
            "Philadelphia Phillies": "PHI",
            "Pittsburgh Pirates": "PIT",
            "San Diego Padres": "SDP",
            "Seattle Mariners": "SEA",
            "San Francisco Giants": "SFG",
            "St. Louis Cardinals": "STL",
            "Tampa Bay Rays": "TBR",
            "Texas Rangers": "TEX",
            "Toronto Blue Jays": "TOR",
            "Washington Nationals": "WSN",
        }
        self.now = datetime.now()  # sets current time

    def scrape_necessary_hitting_data(self) -> None:
        fan_page = requests.get(FANGRAPHS_HITTING_URL)  # grabs fangraph website
        mlb_page = requests.get(MLB_HITTING_URL)  # grabs MLB website

        fan_soup = BeautifulSoup(
            fan_page.text, "html.parser"
        )  # parses said website using html
        mlb_soup = BeautifulSoup(
            mlb_page.text, "html.parser"
        )  # parses said website using html

        fan_table = fan_soup.find(
            "table", {"class": "rgMasterTable"}
        )  # finds main table
        mlb_table = mlb_soup.find("div", {"class": "table-wrapper-3-qU3HfQ"})

        headers = [
            _.text for _ in fan_table.find_all("th", {"class": "rgHeader"})
        ]  # grabs all column headers from tabele
        mydata = pd.DataFrame(columns=headers)  # creates dataframe with found headers

        for _ in fan_table.find_all("tr")[
            3:
        ]:  # loops through table of data and adds it to pandas dataframe
            row_data = _.find_all("td")
            row = [i.text for i in row_data]

            length = len(mydata)
            mydata.loc[length] = row

        self.delete_columns(
            ["#"], mydata
        )  # delete unnecessary columns from the dataframe

        data = []  # holder for found data on mlb website
        for row in mlb_table.find_all("tr")[1:]:
            cells = row.find_all("td")
            team = row.find("a").find("span").text
            games = cells[1].text
            runs = cells[3].text
            data.append([team, games, runs])

        df = pd.DataFrame(data, columns=["Team", "GP", "Runs"])
        df["Team"] = df["Team"].map(self.team_abbreviations)

        mydata = pd.merge(mydata, df, on="Team")

        # print(
        #     type((float(mydata.iloc[0][5][:-1])) / 100),
        #     (float(mydata.iloc[0][5][:-1])) / 100,
        # ), exit()

        for index, row in mydata.iterrows():
            # Query Statement to be sent to mysql server
            query = f"INSERT INTO hitting_data (team, rbi, wOBA, slg, wRC, hard_contact, rpg) VALUES ('{mydata.iloc[index][0]}',  '{mydata.iloc[index][1]}',  '{mydata.iloc[index][2]}', '{mydata.iloc[index][3]}',  '{mydata.iloc[index][4]}',  '{(float(mydata.iloc[index][5][:-1]) / 100)}',  '{round(int(mydata.iloc[index][7]) / int(mydata.iloc[index][6]),2)}')"
            CURSOR.execute(query)
            CONNECTION.commit()

    def scrape_necessary_first_inning_hitting_data(self) -> None:
        """
        Scrapes data from Fangraphs website and MLB website to populate table in MySQL database
            for first innning hitting data

        Args: None
        Returns: None

        Things to Do (TD):
        rbi, wOBA, slg, wRC, hard_hit -> fangraphs?
        gp -> mlb
        rpg -> normal calulations
        """
        fan_page = requests.get(FANGRAPHS_BASIC_HITTING_URL_FI)  # grabs fangraph website
        fan_soup = BeautifulSoup(fan_page.text, "html.parser")  # parses said website using html



        fan_table = fan_soup.find("div", {"class":"table-wrapper-outer"})  # finds main table
        print(fan_table),exit()
        
        headers = [_.text for _ in fan_table.find_all("th", {"class": "rgHeader"})]  # grabs all column headers from tabele
        mydata = pd.DataFrame(columns=headers)  # creates dataframe with found headers

        for _ in fan_table.find_all("tr")[3:]:  # loops through table of data and adds it to pandas dataframe
            row_data = _.find_all("td")
            row = [i.text for i in row_data]

            length = len(mydata)
            mydata.loc[length] = row

        self.delete_columns(
            [
                "#",
                "Season",
                "G",
                "PA",
                "AB",
                "H",
                "1B",
                "2B",
                "3B",
                "HR",
                "R",
                "BB",
                "IBB",
                "SO",
                "HBP",
                "SF",
                "SH",
                "GDP",
                "SB",
                "CS",
                "AVG",
            ],
            mydata,
        )  # delete unnecessary columns from the dataframe
        
        print(mydata)

    def calculate_xrpg(self) -> None:
        teams = pd.read_sql(
            "SELECT team FROM hitting_data ORDER BY team ASC", con=CONNECTION
        )

        hit_efficiency = pd.read_sql(
            "SELECT avg_ratio FROM hitting_data_view ORDER BY team ASC", con=CONNECTION
        )

        rpg = pd.read_sql(
            "SELECT rpg FROM hitting_data ORDER BY team ASC", con=CONNECTION
        )

        model = LinearRegression()
        model.fit(  # Train the model on correlation between RPG and Hitting Efficiency
            hit_efficiency, rpg
        )

        xrpg = model.predict(hit_efficiency)  # Predicts xRPG

        for index, val in enumerate(xrpg):
            # Query Statement to be sent to mysql server
            query = f"INSERT INTO team_xRPG (team, xRPG) VALUES ('{teams['team'][index]}',  '{val[0]}')"
            CURSOR.execute(query)
            CONNECTION.commit()

    def scrape_necessary_starting_pitching_data(self) -> None:
        """
        Scrapes data from Fangraphs website and populates table in MySQL database

        Args: None
        Returns: None
        """
        fan_page = requests.get(FANGRAPHS_STARTING_URL)  # grabs fangraph website

        fan_soup = BeautifulSoup(
            fan_page.text, "html.parser"
        )  # parses said website using html

        fan_table = fan_soup.find(
            "table", {"class": "rgMasterTable"}
        )  # finds main table

        headers = [
            _.text for _ in fan_table.find_all("th", {"class": "rgHeader"})
        ]  # grabs all column headers from tabele
        mydata = pd.DataFrame(columns=headers)  # creates dataframe with found headers

        for _ in fan_table.find_all("tr")[
            3:
        ]:  # loops through table of data and adds it to pandas dataframe
            row_data = _.find_all("td")
            row = [i.text for i in row_data]

            length = len(mydata)
            mydata.loc[length] = row

        self.delete_columns(
            ["#", "Team"], mydata
        )  # delete unnecessary columns from the dataframe

        # print(mydata)

        for index, row in mydata.iterrows():
            # Query Statement to be sent to mysql server
            query = f"INSERT INTO starting_pitcher_data (team, k9, kbb, whip, zcont_percent, siera, era_minus) VALUES ('{mydata.iloc[index][0]}',  '{mydata.iloc[index][1]}',  '{mydata.iloc[index][2]}', '{mydata.iloc[index][3]}',  '{mydata.iloc[index][4][:-1]}',  '{mydata.iloc[index][5]}', '{mydata.iloc[index][6]}')"
            CURSOR.execute(query)
            CONNECTION.commit()

    def scrape_necessary_first_inning_starting_pitching_data(self) -> None:
        pass

    def scrape_necessary_relief_pitching_data(self) -> None:
        """
        Scrapes data from Fangraphs website and populates table in MySQL database

        Args: None
        Returns: None
        """
        fan_page = requests.get(FANGRAPHS_RELIEF_URL)  # grabs fangraph website

        fan_soup = BeautifulSoup(
            fan_page.text, "html.parser"
        )  # parses said website using html

        fan_table = fan_soup.find(
            "table", {"class": "rgMasterTable"}
        )  # finds main table

        headers = [
            _.text for _ in fan_table.find_all("th", {"class": "rgHeader"})
        ]  # grabs all column headers from tabele
        mydata = pd.DataFrame(columns=headers)  # creates dataframe with found headers

        for _ in fan_table.find_all("tr")[
            3:
        ]:  # loops through table of data and adds it to pandas dataframe
            row_data = _.find_all("td")
            row = [i.text for i in row_data]

            length = len(mydata)
            mydata.loc[length] = row

        self.delete_columns(
            ["#"], mydata
        )  # delete unnecessary columns from the dataframe

        # print(mydata.iloc[0][4][:-1])

        for index, row in mydata.iterrows():
            # Query Statement to be sent to mysql server
            query = f"INSERT INTO relief_pitcher_data (team, k9, kbb, whip, zcont_percent, siera, era_minus) VALUES ('{mydata.iloc[index][0]}',  '{mydata.iloc[index][1]}',  '{mydata.iloc[index][2]}', '{mydata.iloc[index][3]}',  '{mydata.iloc[index][4][:-1]}',  '{mydata.iloc[index][5]}', '{mydata.iloc[index][6]}')"
            CURSOR.execute(query)
            CONNECTION.commit()

    def scrape_necessary_first_inning_relief_pitching_data(self) -> None:
        pass

    def delete_columns(self, del_cols: list, df: pd.DataFrame) -> None:
        """
        Deletes unnecessary columns from a pandas dataframe

        Args:
            del_cols (list): List of strings containing column names to delete
            df (pd.DataFrame): Pandas Dataframe that has columns to be deleted
        Returns: None
        """
        for _ in del_cols:
            del df[_]


a = retrieve_mlb_data()
# a.scrape_necessary_hitting_data()
# a.scrape_necessary_starting_pitching_data()
a.scrape_necessary_first_inning_hitting_data()
