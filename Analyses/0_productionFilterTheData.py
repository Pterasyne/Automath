import pandas as pd
import numpy as np
import os.path
import matplotlib.pyplot as plt
numberOfParticipants = 26 #insert your number of participants here, for our studies there were 26

df = pd.read_csv("production_clean.csv")

#Filtering on trials
df.drop(df[(df["num1"] + df["num2"]) >= 10].index, inplace = True) 
df["problem"] = df["num1"].astype(str) + " + " + df["num2"].astype(str) #adding a column to have an identifiying key for problem
df.drop(df[df["correct"] != "correct"].index, inplace = True) #also remove undef

#Filtering on participants
stdDf = df.groupby("participant_code", as_index = False)["reaction_time"].std()
meanDf = df.groupby("participant_code", as_index = False)["reaction_time"].mean()
correctDf = df.groupby("participant_code", as_index = False)["correct"].value_counts()
for i in range(1 , numberOfParticipants + 1):
    mean = meanDf.loc[meanDf['participant_code'] == i, 'reaction_time'].iloc[0]
    std = stdDf.loc[stdDf['participant_code'] == i, 'reaction_time'].iloc[0]
    numberCorrect = correctDf.loc[(correctDf['participant_code'] == i) & (correctDf["correct"] == "correct"), 'count'].iloc[0]
    totalTrials = correctDf.loc[correctDf['participant_code'] == i, 'count'].sum() #there are easier way but we keep the logic
    df.drop(df[(df["participant_code"] == i) & ((df["reaction_time"] > mean + 3*std) 
               | (df["reaction_time"] < mean - 3*std))].index, inplace = True) #remove extreme problems within a participant

#Adding pre-tests automatization information for R-analyses
if os.path.isfile("pre_addition_strat_automatized.csv"): 
    autoDf = pd.read_csv("pre_addition_strat_automatized.csv")
    autoDf.drop("child_answer", axis = 1 , inplace = True)
    df = pd.merge(df,autoDf, how = "outer")

#Adding post-tests automatization information for R-analyses
if os.path.isfile("post_addition_strat_automatized.csv"): 
    autoDf = pd.read_csv("post_addition_strat_automatized.csv")
    autoDf.drop("child_answer", axis = 1 , inplace = True)
    df = pd.merge(df,autoDf, how = "outer")

df["stillAutomatized"] = ((df["preAutomatized"] == 1) & (df["postAutomatized"] == 1)).astype(int)
df["stillNonAutomatized"] = ((df["preAutomatized"] == 0) & (df["postAutomatized"] == 0)).astype(int)
df["becameAutomatized"] = ((df["preAutomatized"] == 0) & (df["postAutomatized"] == 1)).astype(int)

df.to_csv("production_final.csv", index = False)
