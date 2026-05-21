import pandas as pd
NumberOfParticipants = 26 #insert your number of participants here, for our studies there were 26
    
spanDf = pd.DataFrame(columns =["participant_code", "letterSpan"])

for i in range(1, NumberOfParticipants + 1):
    df = pd.read_excel(f"post-tests/Letter_{i:02}.xlsx") 
    span = df[df["Correct"] == True]["Span"].max()
    temp = pd.DataFrame({"participant_code" : [i], "letterSpan" : [span]})
    spanDf = pd.concat([spanDf, temp], ignore_index = True)

spanDf.to_csv("letterSpan.csv", index = False)