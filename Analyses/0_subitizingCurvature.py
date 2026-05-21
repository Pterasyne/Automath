import pandas as pd
from math import e
from scipy.optimize import curve_fit, minimize_scalar
NumberOfParticipants = 26 #insert your number of participants here, for our studies there were 26
    
curvatureDf = pd.DataFrame(columns =["participant_code", "ISR"]) #ISR for Individual Subitizing Range, here only by the curvature method on RT

df = pd.read_csv("subitizing_clean_experiment.csv")
df.drop(df[df["correct_response"] != True].index, inplace = True) 

for i in range(1, NumberOfParticipants + 1): #more details in the "2_individualSubitizingRange.py" code
    current_df = df.drop(df[df["participant_code"] != i].index)
    clean_df = current_df.groupby("expected", as_index = False)["rt_child"].mean()

    numerosity = clean_df["expected"].tolist()
    reactivity = ((clean_df["rt_child"] - min(clean_df["rt_child"])) / (max(clean_df["rt_child"]) - min(clean_df["rt_child"]))).tolist()

    parametersSigmoid, ignore = curve_fit(lambda x, c1, c2: 1/(1+e**(-c1*(x-c2))), numerosity, reactivity)

    c1 = parametersSigmoid[0]
    c2 = parametersSigmoid[1]

    def derivative(x):  
        return (c1*(e**(-c1*(x-c2))))/((1+e**(-c1*(x-c2)))**2)
    
    def second_derivative(x):
        return ((c1**2)*(e**(-c1*(x-c2)))*((e**(-c1*(x-c2)))-1))/((1+e**(-c1*(x-c2)))**3)
    
    def curvature(x):
        return second_derivative(x)/((1+(derivative(x)**2))**(3/2))
    
    def additive_inverse_curvature(x):
        return - curvature(x)
    max_curvature = minimize_scalar(additive_inverse_curvature, bounds=(0, c2))

    curvaturesRT = max_curvature.x
    temp = pd.DataFrame({"participant_code" : [i], "ISR" : [curvaturesRT]})
    curvatureDf = pd.concat([curvatureDf, temp], ignore_index = True)

curvatureDf.to_csv("subitizingCurvature.csv", index = False)