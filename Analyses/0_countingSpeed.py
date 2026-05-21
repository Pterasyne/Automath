import pandas as pd
NumberOfParticipants = 26 #insert your number of participants here, for our studies there were 26
    
speedDf = pd.DataFrame(columns =["participant_code", "countingSpeed"])

for i in range(1, NumberOfParticipants + 1):
    df = pd.read_csv(f"post-tests/chrono_{i:02}.csv").iloc[0]
    speed = df["meanSixBest"]
    temp = pd.DataFrame({"participant_code" : [i], "countingSpeed" : [speed]})
    speedDf = pd.concat([speedDf, temp], ignore_index = True)

speedDf.to_csv("countingSpeed.csv", index = False)
