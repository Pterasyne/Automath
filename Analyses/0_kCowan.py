import pandas as pd
NumberOfParticipants = 26 #insert your number of participants here, for our studies there were 26
    
kDf = pd.DataFrame(columns =["participant_code", "cowan_k_size_4", "cowan_k_size_6", "cowan_k_size_8", "cowan_k_mean"])

for i in range(1, NumberOfParticipants + 1):
    df = pd.read_csv(f"post-tests/change_detection_{i:02}.csv").iloc[0] #first line is sufficient
    k4 = df["cowan_k_size_4"]
    k6 = df["cowan_k_size_6"]
    k8 = df["cowan_k_size_8"]
    kmean = df["cowan_k_mean"]   
    temp = pd.DataFrame({"participant_code" : [i], 
                         "cowan_k_size_4" : [k4], "cowan_k_size_6" : [k6], "cowan_k_size_8" : [k8],
                         "cowan_k_mean" : [kmean]})
    kDf = pd.concat([kDf, temp], ignore_index = True)

kDf.to_csv("kCowan.csv", index = False)