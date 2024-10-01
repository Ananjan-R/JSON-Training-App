import training_func as tr

#Data from trainings.json is loaded
training_data = tr.json_load('resources/trainings.json')  

#Number of completions for each training is counted
training_counts = tr.completed_training_count(training_data)

tr.json_save(training_counts, 'results/output1.json')  

#Message notifying completion of save
print("Training completion counts saved to output1.json")

#*******************************************************************************************************

#Fiscal year period that is required is specified
start_fiscal = '07/01/2023'
end_fiscal = '06/30/2024'

#Trainings that are required are specified
trainings_list = ["Electrical Safety for Labs", "X-Ray Safety", "Laboratory Safety Training"]

#Retrieves the list of people that have completed the trainings within the given fiscal year
fiscal_year_trainings = tr.filter_people_by_fiscalyear_and_training(training_data, trainings_list, start_fiscal, end_fiscal)

#Saving the filtered results as a JSON file
tr.json_save(fiscal_year_trainings, 'results/output2.json')

#Message notifying completion of save
print("Filtered training completions saved to output2.json")

#*******************************************************************************************************
#Find expired or soon to expired data using 1st of October 2023 as the current date
date = "10/01/2023"
expiring_training_results = tr.expired_or_soon_to_expire(json_data=training_data, date_ref=date, status= None)

#Save the expiry results as a JSON file
tr.json_save(expiring_training_results, 'results/output3.json')

#Message notifying completion of save
print("Filtered expired or soon to expire training data saved to output3.json")

