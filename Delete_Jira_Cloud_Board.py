import requests

def delete_jira_board(base_url, email, api_token, board_id):
    # Endpoint for deleting the board
    board_url = f"{base_url}/rest/agile/1.0/board/{board_id}"
    
    # Basic Authentication Setup
    auth = (email, api_token)
    
    # Send DELETE request to remove the board
    response = requests.delete(board_url, auth=auth)
    
    # Debug output
    print(f"Request URL: {response.request.url}")
    print(f"Request Method: {response.request.method}")
    print(f"Status Code: {response.status_code}")
    
    # Check the response from the server
    if response.status_code == 204:
        print(f"Successfully deleted the board with ID: {board_id}.")
    elif response.status_code == 404:
        print("The specified board does not exist.")
    elif response.status_code == 403:
        print("Insufficient permissions to delete the board.")
    else:
        print(f"Failed to delete the board. Status Code: {response.status_code}. Error: {response.text}")

# Parameters (replace with your actual details)
base_url = "https://your-domain.atlassian.net"
email = "your-email@example.com"
api_token = "your-api-token"
board_id = 123  # Replace with the board ID you want to delete

delete_jira_board(base_url, email, api_token, board_id)
