import pandas as pd
import numpy as np
import plotly.express as px
import plotly.figure_factory as ff

def medal_tally(df):

    medal_tally = df.drop_duplicates(subset = ["Team", "NOC", "Games", "Year", "City", "Sport", "Event", "Medal"])
    medal_tally = medal_tally.groupby("region").sum()[["Gold", "Silver", "Bronze"]].sort_values("Gold", ascending = False).reset_index()
    medal_tally['total'] = medal_tally['Gold'] + medal_tally['Silver'] + df['Bronze']

    return medal_tally

def country_year_list(df):
    years = list(df['Year'].unique())
    years.sort()
    years.insert(0, "Overall")

    countries = np.unique(df['region'].dropna().values).tolist() # Get the countires in sorted order by removing all the NaN values.
    countries.insert(0, "Overall")

    return years, countries

def fetch_medal_tally(df, year, country):
    flag = 0
    medal_df = df.drop_duplicates(subset = ["Team", "NOC", "Games", "Year", "City", "Sport", "Event", "Medal"])

    if year == "Overall" and country == "Overall":
        temp_df = medal_df

    if year == "Overall" and country != "Overall":
        flag = 1
        temp_df = medal_df[medal_df["region"] == country]

    if year != "Overall" and country == "Overall":    
        temp_df = medal_df[medal_df['Year'] == int(year)]

    if year != "Overall" and country != "Overall":
        temp_df = medal_df[(medal_df['Year'] == year) & (medal_df['region'] == country)]
    
    if flag == 1:
        x = temp_df.groupby("Year").sum()[["Gold", "Silver", "Bronze"]].sort_values("Year", ascending = False).reset_index()
    else:
        x = temp_df.groupby("region").sum()[["Gold", "Silver", "Bronze"]].sort_values("Gold", ascending = False).reset_index()
    x["Total"] = x["Gold"] + x["Silver"] + x["Bronze"]

    return x

def data_over_time(df, col):
    
    data_over_time = df.drop_duplicates(["Year", col])["Year"].value_counts().reset_index().sort_values("Year")
    data_over_time.rename(columns = {"Year" : "Edition", "count" : col}, inplace = True)

    return data_over_time

def most_successful(df, sport): # Check which athlete is popular in a particular sport
    temp_df = df.dropna(subset = ["Medal"]) # Beacuse there are many players who didn't won any medal

    if sport != "Overall":
        temp_df = temp_df[temp_df["Sport"] == sport]

    return temp_df["Name"].value_counts()

def yearwise_medal_tally(df, country):
    temp_df = df.dropna(subset = ["Medal"])
    temp_df.dropna(subset = ["Team", "NOC", "Games", "Year", "City", "Sport", "Event", "Medal"], inplace = True)
    new_df = temp_df[temp_df["region"] == country]
    final_df = new_df.groupby("Year").count()["Medal"].reset_index()

    return final_df

def country_event_heatmap(df, country):
    temp_df = df.dropna(subset = ["Medal"])
    temp_df.dropna(subset = ["Team", "NOC", "Games", "Year", "City", "Sport", "Event", "Medal"], inplace = True)
    new_df = temp_df[temp_df["region"] == country]
    return new_df.pivot_table(index = "Sport", columns = "Year", values = "Medal", aggfunc = "count").fillna(0).astype(int)

def wieght_v_height(df, sport):
    athlete_df = df.drop_duplicates(subset = ["Name", "region"])
    
    athlete_df["Medal"].fillna("No Medal", inplace = True)
    temp_df = athlete_df[athlete_df["Sport"] == sport]
    return temp_df

def men_vs_women(df):

    athlete_df = df.drop_duplicates(subset = ["Name", "region"])
    gender_dummies = pd.get_dummies(athlete_df["Sex"]).astype(int)
    athlete_df_temp = pd.concat([athlete_df, gender_dummies], axis = 1).drop(columns = ["Sex"], axis = 1)
    men = athlete_df_temp[athlete_df_temp["M"] == 1].groupby("Year").count()["Name"].reset_index()
    women = athlete_df_temp[athlete_df_temp["F"] == 1].groupby("Year").count()["Name"].reset_index()
    final = men.merge(women, on = "Year", how = "left")
    final.fillna(0, inplace = True)
    final["Name_y"] = final["Name_y"].astype(int)
    final.rename(columns = {"Name_x" : "Male", "Name_y" : "Female"}, inplace = True)
    return final



