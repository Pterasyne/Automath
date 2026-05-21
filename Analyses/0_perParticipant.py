import pandas as pd
numberOfParticipants = 26 

files = ["episodicMemory.csv",
         "kCowan.csv",
         "letterSpan.csv",
         "countingSpeed.csv",
         "subitizingCurvature.csv"]

subitizing = pd.read_csv("subitizing_clean_experiment.csv")
subitizingRT = subitizing[subitizing["correct_response"] == True].groupby("participant_code")[["rt_child"]].mean().reset_index() 
subitizingRT = subitizingRT.rename(columns={"rt_child": "RTSubitizing"})
subitizingACC = subitizing.groupby("participant_code")[["correct_response"]].mean().reset_index()
subitizingACC = subitizingACC.rename(columns={"correct_response": "accuracySubitizing"})


preVerification = pd.read_csv("pre_arithmetic_final.csv")

postVerification = pd.read_csv("post_arithmetic_final.csv")

tabProduction = pd.read_csv("production_final.csv")
tabProduction = tabProduction[tabProduction["answer"]!=10]

preSubStrat = pd.read_csv("pre_subtraction_strat_complete.csv")

preAddStrat = pd.read_csv("pre_addition_strat_complete.csv")

postSubStrat = pd.read_csv("post_subtraction_strat_complete.csv")

postAddStrat = pd.read_csv("post_addition_strat_complete.csv")


preVerification = preVerification.rename(columns={"RT_true": "pre_RT_true",
                                    "RT_false_plus1": "pre_RT_false_plus1",
                                    "RT_false_minus1": "pre_RT_false_minus1"}) #Or change preprocessing (but I prefer it for OpportunisticStopping calculations)
preVerification = preVerification.groupby("participant_code")[["pre_RT_true", "pre_RT_false_plus1", "pre_RT_false_minus1"]].mean().reset_index()


postVerification = postVerification.rename(columns={"RT_true": "post_RT_true",
                                    "RT_false_plus1": "post_RT_false_plus1",
                                    "RT_false_minus1": "post_RT_false_minus1"}) 
postVerification = postVerification.groupby("participant_code")[["post_RT_true", "post_RT_false_plus1", "post_RT_false_minus1"]].mean().reset_index()



tabProduction["date_fr"] = pd.to_datetime(tabProduction["date_fr"], format = "mixed")

tab = pd.DataFrame(columns=["participant_code","reaction_time"])
preTab = pd.DataFrame(columns=["participant_code","reaction_time"])
postTab = pd.DataFrame(columns=["participant_code","reaction_time"])
q1Tab = pd.DataFrame(columns=["participant_code","reaction_time"])
q2Tab = pd.DataFrame(columns=["participant_code","reaction_time"])
q3Tab = pd.DataFrame(columns=["participant_code","reaction_time"])
q4Tab = pd.DataFrame(columns=["participant_code","reaction_time"])


for i in tabProduction["participant_code"].unique(): #not all participants after filtering
    tempTab = tabProduction[tabProduction["participant_code"] == i].copy()
    medianDate = tempTab["date_fr"].median()
    tempPreTab = tempTab[tempTab["date_fr"] < medianDate]
    tempPostTab = tempTab[tempTab["date_fr"] >= medianDate]

    q1Date = tempPreTab["date_fr"].median()
    tempQ1Tab = tempPreTab[tempPreTab["date_fr"] < q1Date]
    tempQ2Tab = tempPreTab[tempPreTab["date_fr"] >= q1Date]

    q3Date = tempPostTab["date_fr"].median()
    tempQ3Tab = tempPostTab[tempPostTab["date_fr"] < q3Date]
    tempQ4Tab = tempPostTab[tempPostTab["date_fr"] >= q3Date]

    tab = pd.concat([tab, tempTab], ignore_index=True)
    preTab = pd.concat([preTab, tempPreTab], ignore_index=True)
    postTab = pd.concat([postTab, tempPostTab], ignore_index=True)
    q1Tab = pd.concat([q1Tab, tempQ1Tab], ignore_index=True)
    q2Tab = pd.concat([q2Tab, tempQ2Tab], ignore_index=True)
    q3Tab = pd.concat([q3Tab, tempQ3Tab], ignore_index=True)
    q4Tab = pd.concat([q4Tab, tempQ4Tab], ignore_index=True)

preTab.to_csv("pre_production_final.csv", index=False) #Just to save time and do not also have to do it in R
postTab.to_csv("post_production_final.csv", index=False)
q1Tab.to_csv("q1_production_final.csv", index=False)
q2Tab.to_csv("q2_production_final.csv", index=False)
q3Tab.to_csv("q3_production_final.csv", index=False)
q4Tab.to_csv("q4_production_final.csv", index=False)

session0mod6 = tab[(tab["seance"]%6==0)]
session0mod6.to_csv("session0mod6_production_final.csv", index=False)
session0mod6 = session0mod6.groupby(["participant_code", "problem"])[["reaction_time"]].mean().reset_index()

session0mod6 = session0mod6.groupby("participant_code")[["reaction_time"]].mean().reset_index()
session0mod6 = session0mod6.rename(columns={"reaction_time": "sess0mod6_tab_RT"})

session1mod6 = tab[(tab["seance"]%6==1)]
session1mod6.to_csv("session1mod6_production_final.csv", index=False)
session1mod6 = session1mod6.groupby(["participant_code", "problem"])[["reaction_time"]].mean().reset_index()

session1mod6 = session1mod6.groupby("participant_code")[["reaction_time"]].mean().reset_index()
session1mod6 = session1mod6.rename(columns={"reaction_time": "sess1mod6_tab_RT"})

session2mod6 = tab[(tab["seance"]%6==2)]
session2mod6.to_csv("session2mod6_production_final.csv", index=False)
session2mod6 = session2mod6.groupby(["participant_code", "problem"])[["reaction_time"]].mean().reset_index()

session2mod6 = session2mod6.groupby("participant_code")[["reaction_time"]].mean().reset_index()
session2mod6 = session2mod6.rename(columns={"reaction_time": "sess2mod6_tab_RT"})

session3mod6 = tab[(tab["seance"]%6==3)]
session3mod6.to_csv("session3mod6_production_final.csv", index=False)
session3mod6 = session3mod6.groupby(["participant_code", "problem"])[["reaction_time"]].mean().reset_index()

session3mod6 = session3mod6.groupby("participant_code")[["reaction_time"]].mean().reset_index()
session3mod6 = session3mod6.rename(columns={"reaction_time": "sess3mod6_tab_RT"})

session4mod6 = tab[(tab["seance"]%6==4)]
session4mod6.to_csv("session4mod6_production_final.csv", index=False)
session4mod6 = session4mod6.groupby(["participant_code", "problem"])[["reaction_time"]].mean().reset_index()

session4mod6 = session4mod6.groupby("participant_code")[["reaction_time"]].mean().reset_index()
session4mod6 = session4mod6.rename(columns={"reaction_time": "sess4mod6_tab_RT"})

session5mod6 = tab[(tab["seance"]%6==5)]
session5mod6.to_csv("session5mod6_production_final.csv", index=False)
session5mod6 = session5mod6.groupby(["participant_code", "problem"])[["reaction_time"]].mean().reset_index()

session5mod6 = session5mod6.groupby("participant_code")[["reaction_time"]].mean().reset_index()
session5mod6 = session5mod6.rename(columns={"reaction_time": "sess5mod6_tab_RT"})

session0to2mod6 = tab[(tab["seance"]%6<3)]
session0to2mod6.to_csv("session0to2mod6_production_final.csv", index=False)
session0to2mod6 = session0to2mod6.groupby(["participant_code", "problem"])[["reaction_time"]].mean().reset_index()

session0to2mod6 = session0to2mod6.groupby("participant_code")[["reaction_time"]].mean().reset_index()
session0to2mod6 = session0to2mod6.rename(columns={"reaction_time": "sess0to2mod6_tab_RT"})

session3to5mod6 = tab[(tab["seance"]%6>=3)]
session3to5mod6.to_csv("session3to5mod6_production_final.csv", index=False)
session3to5mod6 = session3to5mod6.groupby(["participant_code", "problem"])[["reaction_time"]].mean().reset_index()

session3to5mod6 = session3to5mod6.groupby("participant_code")[["reaction_time"]].mean().reset_index()
session3to5mod6 = session3to5mod6.rename(columns={"reaction_time": "sess3to5mod6_tab_RT"})

session0to1mod6 = tab[(tab["seance"]%6<2)]
session0to1mod6.to_csv("session0to1mod6_production_final.csv", index=False)
session0to1mod6 = session0to1mod6.groupby(["participant_code", "problem"])[["reaction_time"]].mean().reset_index()

session0to1mod6 = session0to1mod6.groupby("participant_code")[["reaction_time"]].mean().reset_index()
session0to1mod6 = session0to1mod6.rename(columns={"reaction_time": "sess0to1mod6_tab_RT"})

session2to3mod6 = tab[((tab["seance"]%6==2) | (tab["seance"]%6==3))]
session2to3mod6.to_csv("session2to3mod6_production_final.csv", index=False)
session2to3mod6 = session2to3mod6.groupby(["participant_code", "problem"])[["reaction_time"]].mean().reset_index()

session2to3mod6 = session2to3mod6.groupby("participant_code")[["reaction_time"]].mean().reset_index()
session2to3mod6 = session2to3mod6.rename(columns={"reaction_time": "sess2to3mod6_tab_RT"})

session4to5mod6 = tab[(tab["seance"]%6>3)]
session4to5mod6.to_csv("session4to5mod6_production_final.csv", index=False)
session4to5mod6 = session4to5mod6.groupby(["participant_code", "problem"])[["reaction_time"]].mean().reset_index()

session4to5mod6 = session4to5mod6.groupby("participant_code")[["reaction_time"]].mean().reset_index()
session4to5mod6 = session4to5mod6.rename(columns={"reaction_time": "sess4to5mod6_tab_RT"})

tab = tab.groupby(["participant_code", "problem"])[["reaction_time"]].mean().reset_index()

tab = tab.groupby("participant_code")[["reaction_time"]].mean().reset_index()
tab = tab.rename(columns={"reaction_time": "tab_RT"})

preTab = preTab.groupby(["participant_code", "problem"])[["reaction_time"]].mean().reset_index()

preTab = preTab.groupby("participant_code")[["reaction_time"]].mean().reset_index()
preTab = preTab.rename(columns={"reaction_time": "pre_tab_RT"})

postTab = postTab.groupby(["participant_code", "problem"])[["reaction_time"]].mean().reset_index()

postTab = postTab.groupby("participant_code")[["reaction_time"]].mean().reset_index()
postTab = postTab.rename(columns={"reaction_time": "post_tab_RT"})

q1Tab = q1Tab.groupby(["participant_code", "problem"])[["reaction_time"]].mean().reset_index()

q1Tab = q1Tab.groupby("participant_code")[["reaction_time"]].mean().reset_index()
q1Tab = q1Tab.rename(columns={"reaction_time": "q1_tab_RT"})

q2Tab = q2Tab.groupby(["participant_code", "problem"])[["reaction_time"]].mean().reset_index()

q2Tab = q2Tab.groupby("participant_code")[["reaction_time"]].mean().reset_index()
q2Tab = q2Tab.rename(columns={"reaction_time": "q2_tab_RT"})

q3Tab = q3Tab.groupby(["participant_code", "problem"])[["reaction_time"]].mean().reset_index()

q3Tab = q3Tab.groupby("participant_code")[["reaction_time"]].mean().reset_index()
q3Tab = q3Tab.rename(columns={"reaction_time": "q3_tab_RT"})

q4Tab = q4Tab.groupby(["participant_code", "problem"])[["reaction_time"]].mean().reset_index()

q4Tab = q4Tab.groupby("participant_code")[["reaction_time"]].mean().reset_index()
q4Tab = q4Tab.rename(columns={"reaction_time": "q4_tab_RT"})

preSubStrat = preSubStrat.groupby("participant_code")[["PRE match", 
                                                       "PRE count back from A", "PRE count up to A",
                                                       "PRE direct retrieval", "PRE derived facts","PRE other unknown",
                                                       "PRE modeling by separating B from A",
                                                       "PRE modeling by adding up from B to reach A",
                                                       "PRE modeling by pairing A and B one_to_one",
                                                       "preAutomatized"]].mean().reset_index()
preSubStrat["preAutomatizedOnMatch"] = preSubStrat["preAutomatized"]/preSubStrat["PRE match"]
preSubStrat = preSubStrat.add_prefix("sub")
preSubStrat = preSubStrat.rename(columns={"subparticipant_code": "participant_code"})

preAddStrat = preAddStrat.groupby("participant_code")[["PRE match", 
                                                       "PRE count all", "PRE count on from the first addend",
                                                       "PRE count on from the larger addend","PRE direct retrieval",
                                                       "PRE derived facts","PRE other unknown","PRE direct modeling",
                                                       "preAutomatized"]].mean().reset_index()
preAddStrat["preAutomatizedOnMatch"] = preAddStrat["preAutomatized"]/preAddStrat["PRE match"]
preAddStrat = preAddStrat.add_prefix("add")
preAddStrat = preAddStrat.rename(columns={"addparticipant_code": "participant_code"})

postSubStrat = postSubStrat.groupby("participant_code")[["POST match", 
                                                       "POST count back from A", "POST count up to A",
                                                       "POST direct retrieval", "POST derived facts","POST other unknown",
                                                       "POST modeling by separating B from A",
                                                       "POST modeling by adding up from B to reach A",
                                                       "POST modeling by pairing A and B one_to_one",
                                                       "postAutomatized"]].mean().reset_index()
postSubStrat["postAutomatizedOnMatch"] = postSubStrat["postAutomatized"]/postSubStrat["POST match"]
postSubStrat = postSubStrat.add_prefix("sub")
postSubStrat = postSubStrat.rename(columns={"subparticipant_code": "participant_code"})

postAddStrat = postAddStrat.groupby("participant_code")[["POST match", 
                                                       "POST count all", "POST count on from the first addend",
                                                       "POST count on from the larger addend","POST direct retrieval",
                                                       "POST derived facts","POST other unknown","POST direct modeling",
                                                       "postAutomatized"]].mean().reset_index()
postAddStrat["postAutomatizedOnMatch"] = postAddStrat["postAutomatized"]/postAddStrat["POST match"]
postAddStrat = postAddStrat.add_prefix("add")
postAddStrat = postAddStrat.rename(columns={"addparticipant_code": "participant_code"})

final = pd.read_csv("demographics_arithmetic.csv")

allDf = [preVerification, postVerification, 
 
         session0mod6, session1mod6, session2mod6, session3mod6, session4mod6, session5mod6,

         session0to2mod6, session3to5mod6, session0to1mod6, session2to3mod6, session4to5mod6,
         tab, preTab, postTab, q1Tab, q2Tab, q3Tab, q4Tab, 

         preSubStrat, preAddStrat, postSubStrat, postAddStrat,

         subitizingRT, subitizingACC]

for df in allDf:
    final = final.merge(df, on="participant_code", how="left")

for file in files:
    temp = pd.read_csv(file)
    final = final.merge(temp, on="participant_code", how="left")

final = final.dropna(axis=1, how="all")

final.to_csv("perParticipant.csv", index=False)

final_complete = final.dropna(how="any").reset_index(drop=True)

final_complete.to_csv("perParticipantWithoutNA.csv", index=False)
