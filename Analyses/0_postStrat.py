import pandas as pd
NumberOfParticipants = 26 #insert your number of participants here, for our studies there were 26
    
temp = pd.DataFrame(columns =["participant_code", "Type", "Opérande 1", "Opérande 2", "Réponse enfant", "Match",
                               "0", "1", "2", "3", "4", "5", "6", "7", "8"])

for i in range(1, NumberOfParticipants + 1):
    df = pd.read_excel(f"post-tests/PostStrat_{i:02}.xlsx") #format of your participant code (leading 0 if single digit here)
    df.drop(["signe", "Résultat attendu", "9"], axis = 1, inplace = True)

    #Removing qualitative comments on the file
    columnsNames = df.columns.tolist() #Not by column names (e.g., "Unnamed: 17"), as the formatting changes across excel versions
    for j in range (len(temp.columns)-1, len(columnsNames)):
        df.drop([columnsNames[j]], axis = 1, inplace = True)  
    df.drop(df[(df["Type"] != "Addition") & (df["Type"] != "Soustraction")].index, inplace = True) #also to remove added general comments
    df["participant_code"] = i 
    temp = pd.concat([temp, df], ignore_index = True)

temp = temp.astype({"Match":bool, "0":bool, "1":bool, "2":bool, "3":bool, "4":bool, "5":bool, "6":bool, "7":bool, "8":bool})
temp.rename(columns = {"Opérande 1":"num1", "Opérande 2":"num2", #same name as arithmetic + in english
                       "Réponse enfant":"child_answer"}, inplace = True) 

#Dummy coding for automatization
temp["postAutomatized"] = 0
temp.loc[((temp["3"]==True) | (temp["4"]==True) | (temp["5"]==True)) #necessary parentheses as the logical "and" ("&") has the priority
         & temp["Match"] == True, "postAutomatized"] = 1 

#Addition part
addition = temp.drop(temp[temp["Type"] == "Soustraction"].index)
addition.drop(["Type", "7", "8"], axis = 1, inplace = True)
addAutoOnly = addition.drop(["Match", "0", "1", "2", "3", "4", "5", "6"], axis = 1)
addAutoOnly.to_csv("post_addition_strat_automatized.csv", index = False) #just the dummy code
addition.rename(columns = {"Match":"POST match", 
                           "0":"POST count all", 
                           "1":"POST count on from the first addend", 
                           "2":"POST count on from the larger addend",
                            "3":"POST direct retrieval", 
                            "4":"POST derived facts", 
                            "5":"POST other unknown",
                            "6":"POST direct modeling"}, inplace = True) #link with "guide de passation"
addition.to_csv("post_addition_strat_complete.csv", index = False) 

#Subtraction part
subtraction = temp.drop(temp[temp["Type"] == "Addition"].index)
subtraction.drop(["Type", "0"], axis = 1, inplace = True)
subAutoOnly = subtraction.drop(["1", "2", "3", "4", "5", "6", "7", "8"], axis = 1)
subAutoOnly.to_csv("post_subtraction_strat_automatized.csv", index = False) #just the dummy code
subtraction.rename(columns = {"Match":"POST match", 
                              "1":"POST count back from A", 
                              "2":"POST count up to A", 
                              "3":"POST direct retrieval", 
                              "4":"POST derived facts", 
                              "5":"POST other unknown",
                              "6":"POST modeling by separating B from A", 
                              "7":"POST modeling by adding up from B to reach A", 
                              "8":"POST modeling by pairing A and B one_to_one"}, inplace = True) #link with "guide de passation"
subtraction.to_csv("post_subtraction_strat_complete.csv", index = False)