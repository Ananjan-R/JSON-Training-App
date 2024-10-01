import json
import datetime

#Function to load JSON file
def json_load(file_name):
   with open(file_name, 'r') as file:
      data = file.read()
      json_data = json.loads(data)
   return json_data

#Function to save output as a JSON file
def json_save(output1, file_name):
   with open(file_name, 'w') as f:
      json.dump(output1, f)

#Function to count the number of completions of each training 
def completed_training_count(json_data):
   #Dictionary to store count of completed trainings
   training_count={}

   for person in json_data:
      #Dictionary to store the most recent training completion if completed more than once
      most_recent_completion = {}

      for training in person['completions']:
         training_name = training['name']
         completed_date = datetime.datetime.strptime(training['timestamp'], '%m/%d/%Y')

         #Add to dictionary if only completion of training or the most recent occurence of same training
         if training_name not in most_recent_completion or completed_date > most_recent_completion[training_name]:
            most_recent_completion[training_name] = completed_date 

      #Training count is updated based on the most recent completion
      for training_name in most_recent_completion:
         training_count[training_name] = training_count.get(training_name, 0) + 1
            
   return training_count

#Function to check if training has been completed in given fiscal year and list them
def fiscal_year_trainings (completed_date, start_fiscal, end_fiscal):
   
   #Convert date into datetime objects to be able to compare
   completed_date = datetime.datetime.strptime(completed_date, '%m/%d/%Y')
   start_fiscal = datetime.datetime.strptime(start_fiscal, '%m/%d/%Y')
   end_fiscal = datetime.datetime.strptime(end_fiscal, '%m/%d/%Y')

   #Return trainings only completed within the fiscal year
   if start_fiscal <= completed_date <= end_fiscal:
      return True
   else:
      return False   
   
#Function to filter people that have completed a given training within the period of a given fiscal year 
def filter_people_by_fiscalyear_and_training (json_data, trainings_list, start_fiscal, end_fiscal):
   #Dictionary to store the trainings with people who have completed them within a given fiscal year
   filtered_results = {training: [] for training in trainings_list}

   #Iterate through the training completion data for each person
   for person in json_data:
      most_recent_completion = {}

      #Search for most recent completion date
      for completion in person['completions']:
         training_name = completion['name']
         completed_date = completion['timestamp']

         #Checking if the training has been completed by the person within the given fiscal year
         if training_name in trainings_list and fiscal_year_trainings(completed_date, start_fiscal, end_fiscal):
                #If it's the first occurence of this training for this person, or it's a more recent completion
            if (training_name not in most_recent_completion or 
                    completed_date > most_recent_completion[training_name]['timestamp']):
               most_recent_completion[training_name] = {'timestamp': completed_date, 'name': person['name']}

        #Add person to the result with their most recent completion for each training
      for training_name, details in most_recent_completion.items():
         if details['name'] not in filtered_results[training_name]:
            filtered_results[training_name].append(details['name'])

   return filtered_results

#Function to check if the training has expired or expires soon
def expiry_check (training_expiry, date_ref):
   expiry_date = datetime.datetime.strptime(training_expiry, '%m/%d/%Y')
   reference_date = datetime.datetime.strptime(date_ref, '%m/%d/%Y')
   next_month = reference_date + datetime.timedelta(days=30)
   
   if expiry_date < reference_date:
      return "Expired"
   
   elif reference_date <= expiry_date <= next_month:
      return "Expires soon"
   
   

#Function to find all people who have expired trainings or will expire soon
def expired_or_soon_to_expire (json_data, date_ref, status):
   expiring_training_people = []
   reference_date = datetime.datetime.strptime(date_ref, '%m/%d/%Y')

   #Iterate through the training completion data for each person
   for person in json_data:
      name = person['name']
      expiring_trainings = []

      most_recent_completion = {}

      #Check all training completions of a person to find most recent completion
      for training in person['completions']:
         training_name = training['name']
         expires = training['expires']
         if expires:
            #Find the expiry date
            expires_date = datetime.datetime.strptime(expires, '%m/%d/%Y')
            # Update the most recent expiry date for training
            if training_name not in most_recent_completion or expires_date > most_recent_completion[training_name]:
               #recent_date = most_recent_completion[training_name]
               most_recent_completion[training_name] = expires_date
               
            
      #Compares the most recent expiry date with current date and adds to list if true
      for training_name, expires in most_recent_completion.items():
            expiry_status = expiry_check(expires.strftime('%m/%d/%Y'), date_ref)   
            if expiry_status and (expiry_status == status or status == None):
               expiring_trainings.append({
                  'training_name': training_name,
                  'training_expiry': expires.strftime('%m/%d/%Y'),
                  'expiry_status': expiry_status
               })

      #Add person to the list if expired or soon to expire trainings are found
      if expiring_trainings:
         expiring_training_people.append({
            'name': name,
            'expiring_trainings': expiring_trainings
         })
   
   return expiring_training_people