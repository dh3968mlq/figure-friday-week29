import globals
from datetime import datetime

def calc_table(division, season, date):
    "Calculate table at specified date"
    df = globals.gdata["aprs"]
    df = df[(df["division"]==division) & (df["season"]==season) & 
                (df["date"]<=datetime.strptime(date, "%Y-%m-%d").date())]
    df = df.rename(columns={"team_name":"team", "win":"won","loss":"lost", "draw":"drawn",
                            "goals_for":"for", "goals_against":"against", "goal_difference":"GD"})
    df["played"] = 1
    dfsum = df[[col["field"] for col in globals.gdata["columndefs"]]].groupby("team").sum().reset_index()
    dfsum = dfsum.sort_values(["points","GD", "for", "team"], ascending=[False, False, False, True])
    return dfsum
