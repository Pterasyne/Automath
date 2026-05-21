import pandas as pd
NumberOfParticipants = 26 #insert your number of participants here, for our studies there were 26

#Init
temp_tra = pd.DataFrame(columns =["participant_code", "stimulus_file", "training_rt_child", "training_experimenter_response", "training_expected", "training_correct_response"])
temp_exp = pd.DataFrame(columns =["participant_code", "stimulus_file", "rt_child", "experimenter_response", "expected", "correct_response"])

for i in range(1, NumberOfParticipants + 1):
    df = pd.read_csv(f"pre-tests/subitizing_{i:02}.csv") #format of your participant code (leading 0 if single digit here)
    df.drop(["success", "timeout", "failed_images", "failed_audio", "failed_video", "failed_video", "trial_type", "trial_index", "plugin_version", "time_elapsed", 
             "rt", "response", "value", "stimulus", "training_rt_experimenter", "rt_experimenter"], axis = 1, inplace = True)
    df["stimulus_file"] = df["stimulus_file"].ffill() #forward fill from the last observed value (as it was not aligned with RT)

#For the training file
    df_tra = df.drop(["rt_child", "experimenter_response", "expected", "correct_response"], axis = 1)
    df_tra.dropna(inplace = True)
    temp_tra = pd.concat([temp_tra.astype(df_tra.dtypes), df_tra], ignore_index = True)

#For the experiment file
    df_exp = df.drop(["training_rt_child", "training_experimenter_response", "training_expected", "training_correct_response"], axis = 1)
    df_exp.dropna(inplace = True)
    temp_exp = pd.concat([temp_exp.astype(df_exp.dtypes), df_exp], ignore_index = True)

temp_tra.to_csv("subitizing_clean_training.csv", index = False)
temp_exp.to_csv("subitizing_clean_experiment.csv", index = False)