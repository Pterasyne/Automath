import pandas as pd
from math import e #Euler's number (not constant btw) for logistic-sigmoid function
from scipy.optimize import curve_fit, minimize_scalar
from scipy import stats
import pwlf

NumberOfParticipants = 26 #Insert your number of participants here, for our studies there were 26
NumberOfStd = 1 #3 in the paper of Starkey and McCandliss
df = pd.read_csv("subitizing_clean_experiment.csv")

probabilistics = []
inflectionsRT = []
intersectionsRT = []
curvaturesRT = []
bilinearsRT = []
inflectionsAcc = []
intersectionsAcc = []
curvaturesAcc = []
bilinearsAcc = []

copyOfDf = df.copy()
df.drop(df[df["correct_response"] != True].index, inplace = True) 


for i in range(1, NumberOfParticipants + 1): 
# -> Probabilistic method (labels are introduced for potential easier vizualization):
    exp = df[df["participant_code"] == i]
    isr = 2
    exp["label"] = "black"
    exp["threshold"] = 0
    exp = exp.astype({"threshold": float})
    for j in range(2, 8):
        tempDfForStd = exp[exp["expected"] <= j]
        tempDfForMedian = exp[exp["expected"] == j]
        tempStd = tempDfForStd["rt_child"].std()
        tempMedian = tempDfForMedian["rt_child"].median()
        exp.loc[(exp["rt_child"] > float(tempMedian+NumberOfStd*tempStd)) & (exp["expected"] == j+1), "label"] = "red"
        exp.loc[exp["expected"] == j+1, "threshold"] = tempMedian+NumberOfStd*tempStd
        tempIsr = exp[exp["expected"] == j+1].value_counts("label").get("black", 0)
        if tempIsr >= 5:
            isr += tempIsr*0.1
        else:
            exp.loc[exp["expected"] > j+1, "label"] = "red"
            isr += tempIsr*0.1
            break
    probabilistics.append(isr)

#We now follow Leibovich-Raveh pipeline here, as in calculating mean RT per problem on correct trials and then min-max normalizing
    current_df = df.drop(df[df["participant_code"] != i].index)
    clean_df = current_df.groupby("expected", as_index = False)["rt_child"].mean()

    numerosity = clean_df["expected"].tolist()
    reactivity = ((clean_df["rt_child"] - min(clean_df["rt_child"])) / (max(clean_df["rt_child"]) - min(clean_df["rt_child"]))).tolist()

# -> Inflection method (and general sigmoid fitting):
    parametersSigmoid, ignore = curve_fit(lambda x, c1, c2: 1/(1+e**(-c1*(x-c2))), numerosity, reactivity)

    c1 = parametersSigmoid[0]
    c2 = parametersSigmoid[1]

    inflectionsRT.append(c2)

# -> Leibovich-Raveh intersection method
    baseline = 1/(1+e**(-c1*(0-c2))) #subitizing line in their paper, aka sigmoid crosses the y_axis

    def sigmoid(x):
        return 1/(1+e**(-c1*(x-c2)))

    def derivative(x):  #for the art of calculus, but could be replaced by np.gradient
        return (c1*(e**(-c1*(x-c2))))/((1+e**(-c1*(x-c2)))**2)
    
    intersection = (baseline - sigmoid(c2))/derivative(c2) + c2 # as tangent = sigmoid(c2) + derivative(c2)*(x-c2)
    intersectionsRT.append(intersection)

# -> Curvature method
    def second_derivative(x):
        return ((c1**2)*(e**(-c1*(x-c2)))*((e**(-c1*(x-c2)))-1))/((1+e**(-c1*(x-c2)))**3)
    
    def curvature(x):
        return second_derivative(x)/((1+(derivative(x)**2))**(3/2))
    
    def additive_inverse_curvature(x): #as there is no maximize_scale in scipy, we minmiize the opposite
        return - curvature(x)
    max_curvature = minimize_scalar(additive_inverse_curvature, bounds=(0, c2))
    curvaturesRT.append(max_curvature.x)

# -> Bilinear (piecewise regression) method via pwlf library
    bilinear = pwlf.PiecewiseLinFit(numerosity, reactivity)
    breakpoints = bilinear.fit(2)
    breakpoint = breakpoints[1]
    bilinearsRT.append(breakpoint)

for i in range(1, NumberOfParticipants + 1): 
#Exactly the same but with accuracy (we could have use a loop and we have no excuses)
    current_df = copyOfDf.drop(copyOfDf[copyOfDf["participant_code"] != i].index)
    current_df["correct_response"] = current_df["correct_response"].astype(str).str.lower().map({"true":1, "false":0})
    clean_df = current_df.groupby("expected", as_index = False)["correct_response"].mean()
    numerosity = clean_df["expected"].tolist()
    inaccuracy = (1 - clean_df["correct_response"]).tolist()

# -> Inflection method (and general sigmoid fitting), adding p0 = [1.0, 5.0] to help convergence (only 2 participants else), as done by Leibovich-Raveh:
    try :   
        parametersSigmoid, ignore = curve_fit(lambda x, c1, c2: 1/(1+e**(-c1*(x-c2))), numerosity, inaccuracy, p0 = [1.0, 5.0])
    except RuntimeError:
        parametersSigmoid, ignore = None, None

    if parametersSigmoid is not None:    
        c1 = parametersSigmoid[0]
        c2 = parametersSigmoid[1]

        inflectionsAcc.append(c2)

# -> Leibovich-Raveh intersection method
        baseline = 1/(1+e**(-c1*(0-c2))) #subitizing line in their paper, aka sigmoid crosses the y_axis

        def sigmoid(x):
            return 1/(1+e**(-c1*(x-c2)))

        def derivative(x):  #for the art of calculus, but could be replaced by np.gradient
            return (c1*(e**(-c1*(x-c2))))/((1+e**(-c1*(x-c2)))**2)
        
        intersection = (baseline - sigmoid(c2))/derivative(c2) + c2 # as tangent = sigmoid(c2) + derivative(c2)*(x-c2)
        intersectionsAcc.append(intersection)

# -> Curvature method
        def second_derivative(x):
            return ((c1**2)*(e**(-c1*(x-c2)))*((e**(-c1*(x-c2)))-1))/((1+e**(-c1*(x-c2)))**3)
        
        def curvature(x):
            return second_derivative(x)/((1+(derivative(x)**2))**(3/2))
        
        def additive_inverse_curvature(x): #as there is no maximize_scale in scipy, we minmiize the opposite
            return - curvature(x)
        max_curvature = minimize_scalar(additive_inverse_curvature)
        curvaturesAcc.append(max_curvature.x)

# -> Bilinear (piecewise regression) method via pwlf library / we do not calculate if it's the only accuracy ISR
        bilinear = pwlf.PiecewiseLinFit(numerosity, inaccuracy)
        breakpoints = bilinear.fit(2)
        breakpoint = breakpoints[1]
        bilinearsAcc.append(breakpoint)

print(stats.pearsonr(intersectionsRT, curvaturesRT))
print(stats.pearsonr(inflectionsRT, intersectionsRT))
print(stats.pearsonr(inflectionsRT, curvaturesRT))
print(stats.pearsonr(bilinearsRT, inflectionsRT))
print(stats.pearsonr(bilinearsRT, intersectionsRT))
print(stats.pearsonr(bilinearsRT, curvaturesRT))
print(stats.pearsonr(probabilistics, bilinearsRT))
print(stats.pearsonr(probabilistics, inflectionsRT))
print(stats.pearsonr(probabilistics, intersectionsRT))
print(stats.pearsonr(probabilistics, curvaturesRT))

print(stats.pearsonr(intersectionsAcc, curvaturesAcc))
print(stats.pearsonr(inflectionsAcc, intersectionsAcc))
print(stats.pearsonr(inflectionsAcc, curvaturesAcc))
print(stats.pearsonr(bilinearsAcc, inflectionsAcc))
print(stats.pearsonr(bilinearsAcc, intersectionsAcc))
print(stats.pearsonr(bilinearsAcc, curvaturesAcc))
