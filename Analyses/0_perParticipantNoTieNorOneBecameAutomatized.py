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

small = ("2.0 + 3.0","2.0 + 4.0","3.0 + 2.0","3.0 + 4.0","4.0 + 2.0","4.0 + 3.0", 
         "2 + 3","2 + 4","3 + 2","3 + 4","4 + 2","4 + 3")

preVerification = pd.read_csv("pre_arithmetic_final.csv")
preVerification = preVerification[(preVerification["num1"]!=1)&(preVerification["num2"]!=1)]
preVerification = preVerification[preVerification["num1"]!=preVerification["num2"]]

postVerification = pd.read_csv("post_arithmetic_final.csv")
postVerification = postVerification[(postVerification["num1"]!=1)&(postVerification["num2"]!=1)]
postVerification = postVerification[postVerification["num1"]!=postVerification["num2"]]

tabProduction = pd.read_csv("production_final.csv")
tabProduction = tabProduction[tabProduction["answer"]!=10]
tabProduction = tabProduction[(tabProduction["num1"]!=1)&(tabProduction["num2"]!=1)]
tabProduction = tabProduction[tabProduction["num1"]!=tabProduction["num2"]]

preSubStrat = pd.read_csv("pre_subtraction_strat_complete.csv")
preSubStrat = preSubStrat[(preSubStrat["num1"]!=1)&(preSubStrat["num2"]!=1)]
preSubStrat = preSubStrat[preSubStrat["num1"]!=preSubStrat["num2"]]
preAddStrat = pd.read_csv("pre_addition_strat_complete.csv")
preAddStrat = preAddStrat[(preAddStrat["num1"]!=1)&(preAddStrat["num2"]!=1)]
preAddStrat = preAddStrat[preAddStrat["num1"]!=preAddStrat["num2"]]
postSubStrat = pd.read_csv("post_subtraction_strat_complete.csv")
postSubStrat = postSubStrat[(postSubStrat["num1"]!=1)&(postSubStrat["num2"]!=1)]
postSubStrat = postSubStrat[postSubStrat["num1"]!=postSubStrat["num2"]]
postAddStrat = pd.read_csv("post_addition_strat_complete.csv")
postAddStrat = postAddStrat[(postAddStrat["num1"]!=1)&(postAddStrat["num2"]!=1)]
postAddStrat = postAddStrat[postAddStrat["num1"]!=postAddStrat["num2"]]

preVerification = preVerification.rename(columns={"RT_true": "pre_RT_true",
                                    "RT_false_plus1": "pre_RT_false_plus1",
                                    "RT_false_minus1": "pre_RT_false_minus1"}) #Or change preprocessing (but I prefer it for OpportunisticStopping calculations)
smallpreVerification = preVerification[preVerification["problem"].isin(small)].copy()
smallpreVerification = smallpreVerification.groupby("participant_code")[["pre_RT_true", "pre_RT_false_plus1", "pre_RT_false_minus1"]].mean().reset_index()
smallpreVerification = smallpreVerification.add_prefix("small")
smallpreVerification = smallpreVerification.rename(columns={"smallparticipant_code": "participant_code"})
bigpreVerification = preVerification[~(preVerification["problem"].isin(small))].copy()
bigpreVerification = bigpreVerification.groupby("participant_code")[["pre_RT_true", "pre_RT_false_plus1", "pre_RT_false_minus1"]].mean().reset_index()
bigpreVerification = bigpreVerification.add_prefix("big")
bigpreVerification = bigpreVerification.rename(columns={"bigparticipant_code": "participant_code"})
preVerification = preVerification.groupby("participant_code")[["pre_RT_true", "pre_RT_false_plus1", "pre_RT_false_minus1"]].mean().reset_index()


postVerification = postVerification.rename(columns={"RT_true": "post_RT_true",
                                    "RT_false_plus1": "post_RT_false_plus1",
                                    "RT_false_minus1": "post_RT_false_minus1"}) 
smallpostVerification = postVerification[postVerification["problem"].isin(small)].copy()
smallpostVerification = smallpostVerification.groupby("participant_code")[["post_RT_true", "post_RT_false_plus1", "post_RT_false_minus1"]].mean().reset_index()
smallpostVerification = smallpostVerification.add_prefix("small")
smallpostVerification = smallpostVerification.rename(columns={"smallparticipant_code": "participant_code"})
bigpostVerification = postVerification[~(postVerification["problem"].isin(small))].copy()
bigpostVerification = bigpostVerification.groupby("participant_code")[["post_RT_true", "post_RT_false_plus1", "post_RT_false_minus1"]].mean().reset_index()
bigpostVerification = bigpostVerification.add_prefix("big")
bigpostVerification = bigpostVerification.rename(columns={"bigparticipant_code": "participant_code"})
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

preTab.to_csv("pre_production_final_BecAuto_NoTieNorOne.csv", index=False) #Just to save time and do not also have to do it in R
postTab.to_csv("post_production_final_BecAuto_NoTieNorOne.csv", index=False)
q1Tab.to_csv("q1_production_final_BecAuto_NoTieNorOne.csv", index=False)
q2Tab.to_csv("q2_production_final_BecAuto_NoTieNorOne.csv", index=False)
q3Tab.to_csv("q3_production_final_BecAuto_NoTieNorOne.csv", index=False)
q4Tab.to_csv("q4_production_final_BecAuto_NoTieNorOne.csv", index=False)

session0mod6 = tab[(tab["seance"]%6==0) & (tab["becameAutomatized"]==1)]
session0mod6.to_csv("session0mod6_production_final_BecAuto_NoTieNorOne.csv", index=False)
session0mod6 = session0mod6.groupby(["participant_code", "problem"])[["reaction_time"]].mean().reset_index()
smallsession0mod6 = session0mod6[session0mod6["problem"].isin(small)].copy()
smallsession0mod6 = smallsession0mod6.groupby("participant_code")[["reaction_time"]].mean().reset_index()
smallsession0mod6 = smallsession0mod6.rename(columns={"reaction_time": "smallsession0mod6_tab_RT"})
bigsession0mod6 = session0mod6[~(session0mod6["problem"].isin(small))].copy() #~ as the logical "not"
bigsession0mod6 = bigsession0mod6.groupby("participant_code")[["reaction_time"]].mean().reset_index()
bigsession0mod6 = bigsession0mod6.rename(columns={"reaction_time": "bigsession0mod6_tab_RT"})
session0mod6 = session0mod6.groupby("participant_code")[["reaction_time"]].mean().reset_index()
session0mod6 = session0mod6.rename(columns={"reaction_time": "sess0mod6_tab_RT"})

session1mod6 = tab[(tab["seance"]%6==1) & (tab["becameAutomatized"]==1)]
session1mod6.to_csv("session1mod6_production_final_BecAuto_NoTieNorOne.csv", index=False)
session1mod6 = session1mod6.groupby(["participant_code", "problem"])[["reaction_time"]].mean().reset_index()
smallsession1mod6 = session1mod6[session1mod6["problem"].isin(small)].copy()
smallsession1mod6 = smallsession1mod6.groupby("participant_code")[["reaction_time"]].mean().reset_index()
smallsession1mod6 = smallsession1mod6.rename(columns={"reaction_time": "smallsession1mod6_tab_RT"})
bigsession1mod6 = session1mod6[~(session1mod6["problem"].isin(small))].copy() #~ as the logical "not"
bigsession1mod6 = bigsession1mod6.groupby("participant_code")[["reaction_time"]].mean().reset_index()
bigsession1mod6 = bigsession1mod6.rename(columns={"reaction_time": "bigsession1mod6_tab_RT"})
session1mod6 = session1mod6.groupby("participant_code")[["reaction_time"]].mean().reset_index()
session1mod6 = session1mod6.rename(columns={"reaction_time": "sess1mod6_tab_RT"})

session2mod6 = tab[(tab["seance"]%6==2) & (tab["becameAutomatized"]==1)]
session2mod6.to_csv("session2mod6_production_final_BecAuto_NoTieNorOne.csv", index=False)
session2mod6 = session2mod6.groupby(["participant_code", "problem"])[["reaction_time"]].mean().reset_index()
smallsession2mod6 = session2mod6[session2mod6["problem"].isin(small)].copy()
smallsession2mod6 = smallsession2mod6.groupby("participant_code")[["reaction_time"]].mean().reset_index()
smallsession2mod6 = smallsession2mod6.rename(columns={"reaction_time": "smallsession2mod6_tab_RT"})
bigsession2mod6 = session2mod6[~(session2mod6["problem"].isin(small))].copy() #~ as the logical "not"
bigsession2mod6 = bigsession2mod6.groupby("participant_code")[["reaction_time"]].mean().reset_index()
bigsession2mod6 = bigsession2mod6.rename(columns={"reaction_time": "bigsession2mod6_tab_RT"})
session2mod6 = session2mod6.groupby("participant_code")[["reaction_time"]].mean().reset_index()
session2mod6 = session2mod6.rename(columns={"reaction_time": "sess2mod6_tab_RT"})

session3mod6 = tab[(tab["seance"]%6==3) & (tab["becameAutomatized"]==1)]
session3mod6.to_csv("session3mod6_production_final_BecAuto_NoTieNorOne.csv", index=False)
session3mod6 = session3mod6.groupby(["participant_code", "problem"])[["reaction_time"]].mean().reset_index()
smallsession3mod6 = session3mod6[session3mod6["problem"].isin(small)].copy()
smallsession3mod6 = smallsession3mod6.groupby("participant_code")[["reaction_time"]].mean().reset_index()
smallsession3mod6 = smallsession3mod6.rename(columns={"reaction_time": "smallsession3mod6_tab_RT"})
bigsession3mod6 = session3mod6[~(session3mod6["problem"].isin(small))].copy() #~ as the logical "not"
bigsession3mod6 = bigsession3mod6.groupby("participant_code")[["reaction_time"]].mean().reset_index()
bigsession3mod6 = bigsession3mod6.rename(columns={"reaction_time": "bigsession3mod6_tab_RT"})
session3mod6 = session3mod6.groupby("participant_code")[["reaction_time"]].mean().reset_index()
session3mod6 = session3mod6.rename(columns={"reaction_time": "sess3mod6_tab_RT"})

session4mod6 = tab[(tab["seance"]%6==4) & (tab["becameAutomatized"]==1)]
session4mod6.to_csv("session4mod6_production_final_BecAuto_NoTieNorOne.csv", index=False)
session4mod6 = session4mod6.groupby(["participant_code", "problem"])[["reaction_time"]].mean().reset_index()
smallsession4mod6 = session4mod6[session4mod6["problem"].isin(small)].copy()
smallsession4mod6 = smallsession4mod6.groupby("participant_code")[["reaction_time"]].mean().reset_index()
smallsession4mod6 = smallsession4mod6.rename(columns={"reaction_time": "smallsession4mod6_tab_RT"})
bigsession4mod6 = session4mod6[~(session4mod6["problem"].isin(small))].copy() #~ as the logical "not"
bigsession4mod6 = bigsession4mod6.groupby("participant_code")[["reaction_time"]].mean().reset_index()
bigsession4mod6 = bigsession4mod6.rename(columns={"reaction_time": "bigsession4mod6_tab_RT"})
session4mod6 = session4mod6.groupby("participant_code")[["reaction_time"]].mean().reset_index()
session4mod6 = session4mod6.rename(columns={"reaction_time": "sess4mod6_tab_RT"})

session5mod6 = tab[(tab["seance"]%6==5) & (tab["becameAutomatized"]==1)]
session5mod6.to_csv("session5mod6_production_final_BecAuto_NoTieNorOne.csv", index=False)
session5mod6 = session5mod6.groupby(["participant_code", "problem"])[["reaction_time"]].mean().reset_index()
smallsession5mod6 = session5mod6[session5mod6["problem"].isin(small)].copy()
smallsession5mod6 = smallsession5mod6.groupby("participant_code")[["reaction_time"]].mean().reset_index()
smallsession5mod6 = smallsession5mod6.rename(columns={"reaction_time": "smallsession5mod6_tab_RT"})
bigsession5mod6 = session5mod6[~(session5mod6["problem"].isin(small))].copy() #~ as the logical "not"
bigsession5mod6 = bigsession5mod6.groupby("participant_code")[["reaction_time"]].mean().reset_index()
bigsession5mod6 = bigsession5mod6.rename(columns={"reaction_time": "bigsession5mod6_tab_RT"})
session5mod6 = session5mod6.groupby("participant_code")[["reaction_time"]].mean().reset_index()
session5mod6 = session5mod6.rename(columns={"reaction_time": "sess5mod6_tab_RT"})

session0to2mod6 = tab[(tab["seance"]%6<3) & (tab["becameAutomatized"]==1)]
session0to2mod6.to_csv("session0to2mod6_production_final_BecAuto_NoTieNorOne.csv", index=False)
session0to2mod6 = session0to2mod6.groupby(["participant_code", "problem"])[["reaction_time"]].mean().reset_index()
smallsession0to2mod6 = session0to2mod6[session0to2mod6["problem"].isin(small)].copy()
smallsession0to2mod6 = smallsession0to2mod6.groupby("participant_code")[["reaction_time"]].mean().reset_index()
smallsession0to2mod6 = smallsession0to2mod6.rename(columns={"reaction_time": "smallsession0to2mod6_tab_RT"})
bigsession0to2mod6 = session0to2mod6[~(session0to2mod6["problem"].isin(small))].copy() #~ as the logical "not"
bigsession0to2mod6 = bigsession0to2mod6.groupby("participant_code")[["reaction_time"]].mean().reset_index()
bigsession0to2mod6 = bigsession0to2mod6.rename(columns={"reaction_time": "bigsession0to2mod6_tab_RT"})
session0to2mod6 = session0to2mod6.groupby("participant_code")[["reaction_time"]].mean().reset_index()
session0to2mod6 = session0to2mod6.rename(columns={"reaction_time": "sess0to2mod6_tab_RT"})

session3to5mod6 = tab[(tab["seance"]%6>=3) & (tab["becameAutomatized"]==1)]
session3to5mod6.to_csv("session3to5mod6_production_final_BecAuto_NoTieNorOne.csv", index=False)
session3to5mod6 = session3to5mod6.groupby(["participant_code", "problem"])[["reaction_time"]].mean().reset_index()
smallsession3to5mod6 = session3to5mod6[session3to5mod6["problem"].isin(small)].copy()
smallsession3to5mod6 = smallsession3to5mod6.groupby("participant_code")[["reaction_time"]].mean().reset_index()
smallsession3to5mod6 = smallsession3to5mod6.rename(columns={"reaction_time": "smallsession3to5mod6_tab_RT"})
bigsession3to5mod6 = session3to5mod6[~(session3to5mod6["problem"].isin(small))].copy() #~ as the logical "not"
bigsession3to5mod6 = bigsession3to5mod6.groupby("participant_code")[["reaction_time"]].mean().reset_index()
bigsession3to5mod6 = bigsession3to5mod6.rename(columns={"reaction_time": "bigsession3to5mod6_tab_RT"})
session3to5mod6 = session3to5mod6.groupby("participant_code")[["reaction_time"]].mean().reset_index()
session3to5mod6 = session3to5mod6.rename(columns={"reaction_time": "sess3to5mod6_tab_RT"})

session0to1mod6 = tab[(tab["seance"]%6<2) & (tab["becameAutomatized"]==1)]
session0to1mod6.to_csv("session0to1mod6_production_final_BecAuto_NoTieNorOne.csv", index=False)
session0to1mod6 = session0to1mod6.groupby(["participant_code", "problem"])[["reaction_time"]].mean().reset_index()
smallsession0to1mod6 = session0to1mod6[session0to1mod6["problem"].isin(small)].copy()
smallsession0to1mod6 = smallsession0to1mod6.groupby("participant_code")[["reaction_time"]].mean().reset_index()
smallsession0to1mod6 = smallsession0to1mod6.rename(columns={"reaction_time": "smallsession0to1mod6_tab_RT"})
bigsession0to1mod6 = session0to1mod6[~(session0to1mod6["problem"].isin(small))].copy() #~ as the logical "not"
bigsession0to1mod6 = bigsession0to1mod6.groupby("participant_code")[["reaction_time"]].mean().reset_index()
bigsession0to1mod6 = bigsession0to1mod6.rename(columns={"reaction_time": "bigsession0to1mod6_tab_RT"})
session0to1mod6 = session0to1mod6.groupby("participant_code")[["reaction_time"]].mean().reset_index()
session0to1mod6 = session0to1mod6.rename(columns={"reaction_time": "sess0to1mod6_tab_RT"})

session2to3mod6 = tab[((tab["seance"]%6==2) | (tab["seance"]%6==3)) & (tab["becameAutomatized"]==1)]
session2to3mod6.to_csv("session2to3mod6_production_final_BecAuto_NoTieNorOne.csv", index=False)
session2to3mod6 = session2to3mod6.groupby(["participant_code", "problem"])[["reaction_time"]].mean().reset_index()
smallsession2to3mod6 = session2to3mod6[session2to3mod6["problem"].isin(small)].copy()
smallsession2to3mod6 = smallsession2to3mod6.groupby("participant_code")[["reaction_time"]].mean().reset_index()
smallsession2to3mod6 = smallsession2to3mod6.rename(columns={"reaction_time": "smallsession2to3mod6_tab_RT"})
bigsession2to3mod6 = session2to3mod6[~(session2to3mod6["problem"].isin(small))].copy() #~ as the logical "not"
bigsession2to3mod6 = bigsession2to3mod6.groupby("participant_code")[["reaction_time"]].mean().reset_index()
bigsession2to3mod6 = bigsession2to3mod6.rename(columns={"reaction_time": "bigsession2to3mod6_tab_RT"})
session2to3mod6 = session2to3mod6.groupby("participant_code")[["reaction_time"]].mean().reset_index()
session2to3mod6 = session2to3mod6.rename(columns={"reaction_time": "sess2to3mod6_tab_RT"})

session4to5mod6 = tab[(tab["seance"]%6>3) & (tab["becameAutomatized"]==1)]
session4to5mod6.to_csv("session4to5mod6_production_final_BecAuto_NoTieNorOne.csv", index=False)
session4to5mod6 = session4to5mod6.groupby(["participant_code", "problem"])[["reaction_time"]].mean().reset_index()
smallsession4to5mod6 = session4to5mod6[session4to5mod6["problem"].isin(small)].copy()
smallsession4to5mod6 = smallsession4to5mod6.groupby("participant_code")[["reaction_time"]].mean().reset_index()
smallsession4to5mod6 = smallsession4to5mod6.rename(columns={"reaction_time": "smallsession4to5mod6_tab_RT"})
bigsession4to5mod6 = session4to5mod6[~(session4to5mod6["problem"].isin(small))].copy() #~ as the logical "not"
bigsession4to5mod6 = bigsession4to5mod6.groupby("participant_code")[["reaction_time"]].mean().reset_index()
bigsession4to5mod6 = bigsession4to5mod6.rename(columns={"reaction_time": "bigsession4to5mod6_tab_RT"})
session4to5mod6 = session4to5mod6.groupby("participant_code")[["reaction_time"]].mean().reset_index()
session4to5mod6 = session4to5mod6.rename(columns={"reaction_time": "sess4to5mod6_tab_RT"})

tab = tab.groupby(["participant_code", "problem"])[["reaction_time"]].mean().reset_index()
smalltab = tab[tab["problem"].isin(small)].copy()
smalltab = smalltab.groupby("participant_code")[["reaction_time"]].mean().reset_index()
smalltab = smalltab.rename(columns={"reaction_time": "small_tab_RT"})
bigtab = tab[~(tab["problem"].isin(small))].copy() #~ as the logical "not"
bigtab = bigtab.groupby("participant_code")[["reaction_time"]].mean().reset_index()
bigtab = bigtab.rename(columns={"reaction_time": "big_tab_RT"})
tab = tab.groupby("participant_code")[["reaction_time"]].mean().reset_index()
tab = tab.rename(columns={"reaction_time": "tab_RT"})

preTab = preTab.groupby(["participant_code", "problem"])[["reaction_time"]].mean().reset_index()
smallpreTab = preTab[preTab["problem"].isin(small)].copy()
smallpreTab = smallpreTab.groupby("participant_code")[["reaction_time"]].mean().reset_index()
smallpreTab = smallpreTab.rename(columns={"reaction_time": "small_preTab_RT"})
bigpreTab = preTab[~(preTab["problem"].isin(small))].copy() #~ as the logical "not"
bigpreTab = bigpreTab.groupby("participant_code")[["reaction_time"]].mean().reset_index()
bigpreTab = bigpreTab.rename(columns={"reaction_time": "big_preTab_RT"})
preTab = preTab.groupby("participant_code")[["reaction_time"]].mean().reset_index()
preTab = preTab.rename(columns={"reaction_time": "pre_tab_RT"})

postTab = postTab.groupby(["participant_code", "problem"])[["reaction_time"]].mean().reset_index()
smallpostTab = postTab[postTab["problem"].isin(small)].copy()
smallpostTab = smallpostTab.groupby("participant_code")[["reaction_time"]].mean().reset_index()
smallpostTab = smallpostTab.rename(columns={"reaction_time": "small_postTab_RT"})
bigpostTab = postTab[~(postTab["problem"].isin(small))].copy() #~ as the logical "not"
bigpostTab = bigpostTab.groupby("participant_code")[["reaction_time"]].mean().reset_index()
bigpostTab = bigpostTab.rename(columns={"reaction_time": "big_postTab_RT"})
postTab = postTab.groupby("participant_code")[["reaction_time"]].mean().reset_index()
postTab = postTab.rename(columns={"reaction_time": "post_tab_RT"})

q1Tab = q1Tab.groupby(["participant_code", "problem"])[["reaction_time"]].mean().reset_index()
smallq1Tab = q1Tab[q1Tab["problem"].isin(small)].copy()
smallq1Tab = smallq1Tab.groupby("participant_code")[["reaction_time"]].mean().reset_index()
smallq1Tab = smallq1Tab.rename(columns={"reaction_time": "small_q1Tab_RT"})
bigq1Tab = q1Tab[~(q1Tab["problem"].isin(small))].copy() #~ as the logical "not"
bigq1Tab = bigq1Tab.groupby("participant_code")[["reaction_time"]].mean().reset_index()
bigq1Tab = bigq1Tab.rename(columns={"reaction_time": "big_q1Tab_RT"})
q1Tab = q1Tab.groupby("participant_code")[["reaction_time"]].mean().reset_index()
q1Tab = q1Tab.rename(columns={"reaction_time": "q1_tab_RT"})

q2Tab = q2Tab.groupby(["participant_code", "problem"])[["reaction_time"]].mean().reset_index()
smallq2Tab = q2Tab[q2Tab["problem"].isin(small)].copy()
smallq2Tab = smallq2Tab.groupby("participant_code")[["reaction_time"]].mean().reset_index()
smallq2Tab = smallq2Tab.rename(columns={"reaction_time": "small_q2Tab_RT"})
bigq2Tab = q2Tab[~(q2Tab["problem"].isin(small))].copy() #~ as the logical "not"
bigq2Tab = bigq2Tab.groupby("participant_code")[["reaction_time"]].mean().reset_index()
bigq2Tab = bigq2Tab.rename(columns={"reaction_time": "big_q2Tab_RT"})
q2Tab = q2Tab.groupby("participant_code")[["reaction_time"]].mean().reset_index()
q2Tab = q2Tab.rename(columns={"reaction_time": "q2_tab_RT"})

q3Tab = q3Tab.groupby(["participant_code", "problem"])[["reaction_time"]].mean().reset_index()
smallq3Tab = q3Tab[q3Tab["problem"].isin(small)].copy()
smallq3Tab = smallq3Tab.groupby("participant_code")[["reaction_time"]].mean().reset_index()
smallq3Tab = smallq3Tab.rename(columns={"reaction_time": "small_q3Tab_RT"})
bigq3Tab = q3Tab[~(q3Tab["problem"].isin(small))].copy() #~ as the logical "not"
bigq3Tab = bigq3Tab.groupby("participant_code")[["reaction_time"]].mean().reset_index()
bigq3Tab = bigq3Tab.rename(columns={"reaction_time": "big_q3Tab_RT"})
q3Tab = q3Tab.groupby("participant_code")[["reaction_time"]].mean().reset_index()
q3Tab = q3Tab.rename(columns={"reaction_time": "q3_tab_RT"})

q4Tab = q4Tab.groupby(["participant_code", "problem"])[["reaction_time"]].mean().reset_index()
smallq4Tab = q4Tab[q4Tab["problem"].isin(small)].copy()
smallq4Tab = smallq4Tab.groupby("participant_code")[["reaction_time"]].mean().reset_index()
smallq4Tab = smallq4Tab.rename(columns={"reaction_time": "small_q4Tab_RT"})
bigq4Tab = q4Tab[~(q4Tab["problem"].isin(small))].copy() #~ as the logical "not"
bigq4Tab = bigq4Tab.groupby("participant_code")[["reaction_time"]].mean().reset_index()
bigq4Tab = bigq4Tab.rename(columns={"reaction_time": "big_q4Tab_RT"})
q4Tab = q4Tab.groupby("participant_code")[["reaction_time"]].mean().reset_index()
q4Tab = q4Tab.rename(columns={"reaction_time": "q4_tab_RT"})

smallpreSubStrat = preSubStrat[(preSubStrat["num1"] <= 4) & (preSubStrat["num2"] <= 4)].copy()
smallpreSubStrat = smallpreSubStrat.groupby("participant_code")[["PRE match", 
               "PRE count back from A", "PRE count up to A",
               "PRE direct retrieval", "PRE derived facts","PRE other unknown",
               "PRE modeling by separating B from A",
               "PRE modeling by adding up from B to reach A",
               "PRE modeling by pairing A and B one_to_one",
               "preAutomatized"]].mean().reset_index()
smallpreSubStrat["preAutomatizedOnMatch"] = smallpreSubStrat["preAutomatized"]/smallpreSubStrat["PRE match"]
smallpreSubStrat = smallpreSubStrat.add_prefix("smallsub")
smallpreSubStrat = smallpreSubStrat.rename(columns={"smallsubparticipant_code": "participant_code"})

bigpreSubStrat = preSubStrat[((preSubStrat["num1"] > 4) | (preSubStrat["num2"] > 4))].copy()
bigpreSubStrat = bigpreSubStrat.groupby("participant_code")[["PRE match", 
               "PRE count back from A", "PRE count up to A",
               "PRE direct retrieval", "PRE derived facts","PRE other unknown",
               "PRE modeling by separating B from A",
               "PRE modeling by adding up from B to reach A",
               "PRE modeling by pairing A and B one_to_one",
               "preAutomatized"]].mean().reset_index()
bigpreSubStrat["preAutomatizedOnMatch"] = bigpreSubStrat["preAutomatized"]/bigpreSubStrat["PRE match"]
bigpreSubStrat = bigpreSubStrat.add_prefix("bigsub")
bigpreSubStrat = bigpreSubStrat.rename(columns={"bigsubparticipant_code": "participant_code"})

smallpreAddStrat = preAddStrat[(preAddStrat["num1"] <= 4) & (preAddStrat["num2"] <= 4)].copy()
smallpreAddStrat = smallpreAddStrat.groupby("participant_code")[["PRE match", 
               "PRE count all", "PRE count on from the first addend",
               "PRE count on from the larger addend","PRE direct retrieval",
               "PRE derived facts","PRE other unknown","PRE direct modeling",
               "preAutomatized"]].mean().reset_index()
smallpreAddStrat["preAutomatizedOnMatch"] = smallpreAddStrat["preAutomatized"]/smallpreAddStrat["PRE match"]
smallpreAddStrat = smallpreAddStrat.add_prefix("smalladd")
smallpreAddStrat = smallpreAddStrat.rename(columns={"smalladdparticipant_code": "participant_code"})

bigpreAddStrat = preAddStrat[((preAddStrat["num1"] > 4) | (preAddStrat["num2"] > 4))].copy()
bigpreAddStrat = bigpreAddStrat.groupby("participant_code")[["PRE match", 
               "PRE count all", "PRE count on from the first addend",
               "PRE count on from the larger addend","PRE direct retrieval",
               "PRE derived facts","PRE other unknown","PRE direct modeling",
               "preAutomatized"]].mean().reset_index()
bigpreAddStrat["preAutomatizedOnMatch"] = bigpreAddStrat["preAutomatized"]/bigpreAddStrat["PRE match"]
bigpreAddStrat = bigpreAddStrat.add_prefix("bigadd")
bigpreAddStrat = bigpreAddStrat.rename(columns={"bigaddparticipant_code": "participant_code"})

smallpostSubStrat = postSubStrat[(postSubStrat["num1"] <= 4) & (postSubStrat["num2"] <= 4)].copy()
smallpostSubStrat = smallpostSubStrat.groupby("participant_code")[["POST match", 
               "POST count back from A", "POST count up to A",
               "POST direct retrieval", "POST derived facts","POST other unknown",
               "POST modeling by separating B from A",
               "POST modeling by adding up from B to reach A",
               "POST modeling by pairing A and B one_to_one",
               "postAutomatized"]].mean().reset_index()
smallpostSubStrat["postAutomatizedOnMatch"] = smallpostSubStrat["postAutomatized"]/smallpostSubStrat["POST match"]
smallpostSubStrat = smallpostSubStrat.add_prefix("smallsub")
smallpostSubStrat = smallpostSubStrat.rename(columns={"smallsubparticipant_code": "participant_code"})

bigpostSubStrat = postSubStrat[((postSubStrat["num1"] > 4) | (postSubStrat["num2"] > 4))].copy()
bigpostSubStrat = bigpostSubStrat.groupby("participant_code")[["POST match", 
               "POST count back from A", "POST count up to A",
               "POST direct retrieval", "POST derived facts","POST other unknown",
               "POST modeling by separating B from A",
               "POST modeling by adding up from B to reach A",
               "POST modeling by pairing A and B one_to_one",
               "postAutomatized"]].mean().reset_index()
bigpostSubStrat["postAutomatizedOnMatch"] = bigpostSubStrat["postAutomatized"]/bigpostSubStrat["POST match"]
bigpostSubStrat = bigpostSubStrat.add_prefix("bigsub")
bigpostSubStrat = bigpostSubStrat.rename(columns={"bigsubparticipant_code": "participant_code"})

smallpostAddStrat = postAddStrat[(postAddStrat["num1"] <= 4) & (postAddStrat["num2"] <= 4)].copy()
smallpostAddStrat = smallpostAddStrat.groupby("participant_code")[["POST match", 
               "POST count all", "POST count on from the first addend",
               "POST count on from the larger addend","POST direct retrieval",
               "POST derived facts","POST other unknown","POST direct modeling",
               "postAutomatized"]].mean().reset_index()
smallpostAddStrat["postAutomatizedOnMatch"] = smallpostAddStrat["postAutomatized"]/smallpostAddStrat["POST match"]
smallpostAddStrat = smallpostAddStrat.add_prefix("smalladd")
smallpostAddStrat = smallpostAddStrat.rename(columns={"smalladdparticipant_code": "participant_code"})

bigpostAddStrat = postAddStrat[((postAddStrat["num1"] > 4) | (postAddStrat["num2"] > 4))].copy()
bigpostAddStrat = bigpostAddStrat.groupby("participant_code")[["POST match", 
               "POST count all", "POST count on from the first addend",
               "POST count on from the larger addend","POST direct retrieval",
               "POST derived facts","POST other unknown","POST direct modeling",
               "postAutomatized"]].mean().reset_index()
bigpostAddStrat["postAutomatizedOnMatch"] = bigpostAddStrat["postAutomatized"]/bigpostAddStrat["POST match"]
bigpostAddStrat = bigpostAddStrat.add_prefix("bigadd")
bigpostAddStrat = bigpostAddStrat.rename(columns={"bigaddparticipant_code": "participant_code"})

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
         smallpreVerification, smallpostVerification, 
         bigpreVerification, bigpostVerification, 
         session0mod6, session1mod6, session2mod6, session3mod6, session4mod6, session5mod6,
         smallsession0mod6, smallsession1mod6, smallsession2mod6, smallsession3mod6, smallsession4mod6, smallsession5mod6,
         bigsession0mod6, bigsession1mod6, bigsession2mod6, bigsession3mod6, bigsession4mod6, bigsession5mod6,
         session0to2mod6, session3to5mod6, session0to1mod6, session2to3mod6, session4to5mod6,
         smallsession0to2mod6, smallsession3to5mod6, smallsession0to1mod6, smallsession2to3mod6, smallsession4to5mod6,
         bigsession0to2mod6, bigsession3to5mod6, bigsession0to1mod6, bigsession2to3mod6, bigsession4to5mod6,
         tab, preTab, postTab, q1Tab, q2Tab, q3Tab, q4Tab, 
         smalltab, smallpreTab, smallpostTab, smallq1Tab, smallq2Tab, smallq3Tab, smallq4Tab, 
         bigtab, bigpreTab, bigpostTab, bigq1Tab, bigq2Tab, bigq3Tab, bigq4Tab, 
         preSubStrat, preAddStrat, postSubStrat, postAddStrat,
         smallpreSubStrat, bigpreSubStrat, smallpreAddStrat, bigpreAddStrat,
         smallpostSubStrat, bigpostSubStrat, smallpostAddStrat, bigpostAddStrat,
         subitizingRT, subitizingACC]

for df in allDf:
    final = final.merge(df, on="participant_code", how="left")

for file in files:
    temp = pd.read_csv(file)
    final = final.merge(temp, on="participant_code", how="left")

final = final.dropna(axis=1, how="all")

final.to_csv("perParticipant_BecAuto_NoTieNorOne.csv", index=False)

final_complete = final.dropna(how="any").reset_index(drop=True)

final_complete.to_csv("perParticipantWithoutNA_BecAuto_NoTieNorOne.csv", index=False)
