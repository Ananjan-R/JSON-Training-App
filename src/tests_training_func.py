import pytest
from training_func import (
    completed_training_count, 
    filter_people_by_fiscalyear_and_training, 
    expired_or_soon_to_expire
)

#Sample data to be used in test cases
@pytest.fixture
def test_data():
    return [
        {"name": "Harry Amass", 
         "completions": [
             {"name": "Electrical Safety for Labs", "timestamp": "08/01/2022", "expires": "08/01/2023"},
             {"name": "X-Ray Safety", "timestamp": "06/30/2022", "expires": "06/30/2023"},
             {"name": "Laboratory Safety Training", "timestamp": "09/28/2022", "expires": "10/28/2023"}
         ]
        },
        {"name": "Ethan Wheatley",
         "completions": [
             {"name": "X-Ray Safety", "timestamp": "09/15/2023", "expires": "09/15/2024"},
             {"name": "X-Ray Safety", "timestamp": "08/01/2022", "expires": "08/01/2023"},
             {"name": "Laboratory Safety Training", "timestamp": "07/01/2023", "expires": "07/01/2024"}
         ]
        },
        {"name": "Toby Collyer", 
         "completions": [
             {"name": "Laboratory Safety Training", "timestamp": "08/01/2021", "expires": "08/01/2022"},
             {"name": "Electrical Safety for Labs", "timestamp": "08/01/2023", "expires": "08/01/2024"}
         ]
        }
    ]

#Test Case 1: Counting completed trainings
def test_completed_training_count(test_data):
    result = completed_training_count (test_data)
    expected_output = {
        "Electrical Safety for Labs" : 2,
        "X-Ray Safety" : 2,
        "Laboratory Safety Training" : 3
    }
    assert result == expected_output

#Test Case 2: Check if fiscal year filter works 
def test_fiscalyear_filter(test_data):
    fiscal_year_2024_start = "07/01/2023"
    fiscal_year_2024_end = "06/30/2024"
    result = filter_people_by_fiscalyear_and_training(
        test_data, 
        ["Electrical Safety for Labs", "X-Ray Safety", "Laboratory Safety Training"], 
        fiscal_year_2024_start, 
        fiscal_year_2024_end
    )
    expected_output = {
        "Electrical Safety for Labs": ["Toby Collyer"],
        "X-Ray Safety": ["Ethan Wheatley"],
        "Laboratory Safety Training": ["Ethan Wheatley"]
    }
    print("Result:", result)
    print("Expected:", expected_output)
    assert result == expected_output

#Test Case 3: Check for expired trainings
def test_expired_training_check(test_data):
    result = expired_or_soon_to_expire(test_data, "10/01/2023", "Expired")
    expected_output = [
        {"name": "Harry Amass",
         "expiring_trainings": [
             {"training_name": "Electrical Safety for Labs", "training_expiry": "08/01/2023", "expiry_status": "Expired"},
             {"training_name": "X-Ray Safety", "training_expiry": "06/30/2023", "expiry_status": "Expired"}
         ]
        },
        {"name": "Toby Collyer",
         "expiring_trainings": [
             {"training_name": "Laboratory Safety Training", "training_expiry": "08/01/2022", "expiry_status": "Expired"}
         ]
        }
    ]
    print("Result:", result)
    print("Expected:", expected_output)
    assert result == expected_output

#Test Case 4: Check for trainings that expire soon
def test_expire_soon_check(test_data):
    result = expired_or_soon_to_expire(test_data, "10/01/2023", "Expires soon")
    expected_output = [
        {"name": "Harry Amass",
         "expiring_trainings": [
             {"training_name": "Laboratory Safety Training", "training_expiry": "10/28/2023", "expiry_status": "Expires soon"}
         ]
        }
    ]
    assert result == expected_output


#Test Case 5: Check whether most recent completion for the same training is taken
def test_most_recent_completion(test_data):
    fiscal_year_2024_start = "07/01/2023"
    fiscal_year_2024_end = "06/30/2024"
    result = filter_people_by_fiscalyear_and_training(
        test_data, 
        ["X-Ray Safety"], 
        fiscal_year_2024_start, 
        fiscal_year_2024_end
    )
    expected_output = {"X-Ray Safety": ["Ethan Wheatley"]}
    assert result == expected_output

#Test Case 6: Check whether data on fiscal year boundaries are taken
def test_fiscal_year_boundary(test_data):
    fiscal_year_2024_start = "07/01/2023"
    fiscal_year_2024_end = "06/30/2024"
    result = filter_people_by_fiscalyear_and_training(
        test_data, 
        ["Laboratory Safety Training"], 
        fiscal_year_2024_start, 
        fiscal_year_2024_end
    )
    expected_output = {"Laboratory Safety Training": ["Ethan Wheatley"]}
    assert result == expected_output