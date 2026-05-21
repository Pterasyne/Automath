import pandas as pd
import os.path
NumberOfParticipants = 26 #insert your number of participants here, for our studies there were 26

#Init
temp = pd.DataFrame(columns =["participant_code", "seance", "num1", "num2", "correct", "reaction_time", "answer", "date_fr"])


for i in range(1, NumberOfParticipants + 1):
    df = pd.read_csv(f"tab/seances{i:02}.csv") #format of your participant code (leading 0 if single digit here)
    df["participant_code"] = i
    df.rename({"result" : "correct", "n1" : "num1", "n2": "num2"}, axis = 1, inplace = True)
    temp = pd.concat([temp.astype(df.dtypes), df], ignore_index = True)

if os.path.isfile("demographics_arithmetic.csv"): #per participant
    temp_d = pd.read_csv("demographics_arithmetic.csv")
    temp = pd.merge_ordered(temp_d, temp, on = "participant_code")
    
temp.to_csv("production_clean.csv", index = False)