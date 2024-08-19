import requests
from requests.auth import HTTPBasicAuth
import json
import csv

# -------------------------
# Variable Declarations
# -------------------------
jira_instance_url = "https://your-jira-instance.com"
username = "your-username"
api_token = "your-api-token"

# File path to CSV with field names (one field name per line)
csv_file_path = "fields_to_create.csv"

# Screen and tab information
screen_name = "Your Screen Name"
tab_name = "Your Tab Name"

# Authentication
auth = HTTPBasicAuth(username, api_token)

# Headers
headers = {
    "Accept": "application/json",
    "Content-Type": "application/json"
}

# -------------------------
# Helper Functions
# -------------------------

# Step 1: Create a Multi-line Text Field using REST API
def create_multiline_text_field(field_name, field_description):
    url = f"{jira_instance_url}/rest/api/2/field"
    payload = {
        "name": field_name,
        "description": field_description,
        "type": "com.atlassian.jira.plugin.system.customfieldtypes:textarea",
        "searcherKey": "com.atlassian.jira.plugin.system.customfieldtypes:textsearcher"
    }
    response = requests.post(url, data=json.dumps(payload), headers=headers, auth=auth)
    
    if response.status_code == 201:
        new_field_id = response.json()['id']
        print(f"Created field '{field_name}' with ID: {new_field_id}")
        return new_field_id
    elif response.status_code == 200:  # Recognizing 200 status code as success
        new_field_id = response.json()['id']
        print(f"Field '{field_name}' already exists with ID: {new_field_id}")
        return new_field_id
    else:
        print(f"Failed to create field: {response.status_code} {response.text}")
        raise Exception(f"Error: {response.status_code} {response.text}")

# Step 2: Get Screen ID by Screen Name
def get_screen_id():
    url = f"{jira_instance_url}/rest/api/2/screens"
    response = requests.get(url, headers=headers, auth=auth)
    
    if response.status_code == 200:
        screens = response.json()
        for screen in screens:
            if screen['name'] == screen_name:
                print(f"Found screen '{screen_name}' with ID: {screen['id']}")
                return screen['id']
        raise Exception(f"Screen '{screen_name}' not found.")
    else:
        print(f"Failed to retrieve screens: {response.status_code} {response.text}")
        raise Exception(f"Error: {response.status_code} {response.text}")

# Step 3: Get Tab ID by Tab Name
def get_tab_id(screen_id):
    url = f"{jira_instance_url}/rest/api/2/screens/{screen_id}/tabs"
    response = requests.get(url, headers=headers, auth=auth)
    
    if response.status_code == 200:
        tabs = response.json()
        for tab in tabs:
            if tab['name'] == tab_name:
                print(f"Found tab '{tab_name}' with ID: {tab['id']}")
                return tab['id']
        raise Exception(f"Tab '{tab_name}' not found on screen ID: {screen_id}.")
    else:
        print(f"Failed to retrieve tabs: {response.status_code} {response.text}")
        raise Exception(f"Error: {response.status_code} {response.text}")

# Step 4: Add Field to Screen and Tab
def add_field_to_screen_and_tab(field_id, screen_id, tab_id):
    url = f"{jira_instance_url}/rest/api/2/screens/{screen_id}/tabs/{tab_id}/fields"
    payload = {
        "fieldId": field_id
    }
    response = requests.post(url, data=json.dumps(payload), headers=headers, auth=auth)
    
    if response.status_code == 204 or response.status_code == 200:  # Recognize both 204 and 200 as success
        print(f"Added field with ID: {field_id} to screen ID: {screen_id} on tab ID: {tab_id}")
    else:
        print(f"Failed to add field to screen: {response.status_code} {response.text}")
        raise Exception(f"Error: {response.status_code} {response.text}")

# Step 5: Read CSV and Create Fields
def process_csv_and_create_fields():
    try:
        # Get screen and tab IDs
        screen_id = get_screen_id()
        tab_id = get_tab_id(screen_id)
        
        # Read CSV and process field names
        with open(csv_file_path, mode='r') as file:
            reader = csv.reader(file)
            for row in reader:
                field_name = row[0]
                field_description = f"{field_name} - Multi-line text field created via API"
                
                # Step 1: Create the custom field
                field_id = create_multiline_text_field(field_name, field_description)
                
                # Step 4: Add the field to the screen and tab
                add_field_to_screen_and_tab(field_id, screen_id, tab_id)
        
        print("Process completed successfully.")
    
    except Exception as e:
        print(f"An error occurred: {e}")

# -------------------------
# Main Execution
# -------------------------
if __name__ == "__main__":
    process_csv_and_create_fields()
