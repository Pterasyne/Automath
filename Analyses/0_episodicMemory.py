import pandas as pd
NumberOfParticipants = 26 #insert your number of participants here, for our studies there were 26

episodic = pd.DataFrame(columns =["participant_code", "T1", "T2", "T3", "T4", "T5", "Delayed recall", "Recognition", 
                              "False T1", "False T2", "False T3", "False T4", "False T5", "False Delayed recall", "False Recognition",
                              "Repeat T1", "Repeat T2", "Repeat T3", "Repeat T4", "Repeat T5", "Repeat Delayed recall"])

for i in range(1, NumberOfParticipants + 1):
    t1_to_t5 = pd.read_excel(f"pre-tests/REY_{i:02}.xlsx", "Phase 1-5") #first sheet aka immediate recall (5 times)
    t6 = pd.read_excel(f"pre-tests/REY_{i:02}.xlsx", "Rappel différé") #second one aka delayed recall
    t7 = pd.read_excel(f"pre-tests/REY_{i:02}.xlsx", "Reconnaissance") #last one aka recognition

    participant_code = i
    trial1 = int(t1_to_t5.iat[16, 2])
    falseTrial1 = 15 - (t1_to_t5.iloc[:, 3] == False).sum()
    repeatTrial1 = 15 - (t1_to_t5.iloc[:, 4] == False).sum()
    trial2 = int(t1_to_t5.iat[16, 5])
    falseTrial2 = 15 - (t1_to_t5.iloc[:, 6] == False).sum()
    repeatTrial2 = 15 - (t1_to_t5.iloc[:, 7] == False).sum()
    trial3 = int(t1_to_t5.iat[16, 8])
    falseTrial3 = 15 - (t1_to_t5.iloc[:, 9] == False).sum()
    repeatTrial3 = 15 - (t1_to_t5.iloc[:, 10] == False).sum()
    trial4 = int(t1_to_t5.iat[16, 11])
    falseTrial4 = 15 - (t1_to_t5.iloc[:, 12] == False).sum()
    repeatTrial4 = 15 - (t1_to_t5.iloc[:, 13] == False).sum()
    trial5 = int(t1_to_t5.iat[16, 14])
    falseTrial5 = 15 - (t1_to_t5.iloc[:, 15] == False).sum()
    repeatTrial5 = 15 - (t1_to_t5.iloc[:, 16] == False).sum()
    delayed = int(t6.iat[16, 2])
    falseDelayed = 15 - (t6.iloc[:, 3] == False).sum()
    repeatDelayed = 15 - (t6.iloc[:, 4] == False).sum()
    recognition = int(t7.iat[0, 17][:-3])
    falseRecognition = int(t7.iat[1, 17][:-3])
    
    episodic = pd.concat([episodic, pd.DataFrame({"participant_code" : [participant_code], 
                        "T1" : [trial1], "T2" : [trial2], "T3" : [trial3], "T4" : [trial4], "T5" : [trial5], 
                        "Delayed recall" : [delayed], "Recognition" : [recognition], 
                        "False T1" : [falseTrial1], "False T2" : [falseTrial2], "False T3" : [falseTrial3], "False T4" : [falseTrial4], "False T5" : [falseTrial5], 
                        "False Delayed recall" : [falseDelayed], "False Recognition" : [falseRecognition],
                        "Repeat T1" : [repeatTrial1], "Repeat T2" : [repeatTrial2], "Repeat T3" : [repeatTrial3], "Repeat T4" : [repeatTrial4], "Repeat T5" : [repeatTrial5], 
                        "Repeat Delayed recall" : [repeatDelayed]})], ignore_index = True)

episodic.to_csv("episodicMemory.csv", index = False)