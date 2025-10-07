import pandas as pd


def preprocess(athletes_df, region_df):

    # filtering for summer olympics

    athletes_df = athletes_df[athletes_df["Season"] == "Summer"]

    # merge with region_df
    athletes_df = athletes_df.merge(region_df, on = "NOC", how = "left")

    # dropping duplicates
    athletes_df.drop_duplicates(inplace = True)

    # One Hot Encoding medals
    df = pd.concat([athletes_df, pd.get_dummies(athletes_df["Medal"]).astype(int)], axis = 1)
    
    return df