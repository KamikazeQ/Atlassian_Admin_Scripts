import csv
from jira import JIRA

# Credentials and JIRA Cloud site URLs
jira_cloud_credentials = {
    'username': 'cloud-email@example.com',  # Replace with your JIRA Cloud username
    'token': 'cloudAPIToken'                # Replace with your JIRA Cloud API token
}
jira_cloud_urls = [
    'https://site1.atlassian.net',
    'https://site2.atlassian.net',
    'https://site3.atlassian.net',
    'https://site4.atlassian.net'
]

# Credentials for JIRA Server
jira_server_url = 'https://jiraserver.example.com'  # Replace with your JIRA Server URL
jira_server_username = 'server-username'            # Replace with your JIRA Server username
jira_server_password = 'serverPassword'             # Replace with your JIRA Server password

def get_jira_projects(jira_url, auth):
    """ Connect to JIRA and retrieve all projects. """
    jira = JIRA(server=jira_url, basic_auth=auth)
    projects = jira.projects()
    return [(project.key, project.name, jira_url) for project in projects]

def write_csv(filename, data, header):
    """ Write data to a CSV file. """
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(header)
        writer.writerows(data)

def find_duplicates(filename):
    """ Find duplicate projects based on project key. """
    projects = {}
    with open(filename, newline='') as file:
        reader = csv.reader(file)
        header = next(reader)  # Skip the header row
        for row in reader:
            key = row[0]
            if key in projects:
                projects[key].append(row)
            else:
                projects[key] = [row]

    # Filter out keys that do not have duplicates
    duplicates = [proj for proj_list in projects.values() if len(proj_list) > 1 for proj in proj_list]
    return duplicates

def main():
    all_projects = []

    # Collect projects from all JIRA Cloud sites
    for url in jira_cloud_urls:
        all_projects.extend(get_jira_projects(url, (jira_cloud_credentials['username'], jira_cloud_credentials['token'])))

    # Collect projects from JIRA Server
    all_projects.extend(get_jira_projects(jira_server_url, (jira_server_username, jira_server_password)))

    # Sort all projects by project key
    all_projects_sorted = sorted(all_projects, key=lambda x: x[0])

    # Write to the main CSV
    main_csv_file = 'jira_projects.csv'
    header = ['Project Key', 'Project Name', 'JIRA URL']
    write_csv(main_csv_file, all_projects_sorted, header)
    print("Main CSV file has been created and sorted by project key.")

    # Identify duplicates and write to another CSV if any
    duplicates = find_duplicates(main_csv_file)
    if duplicates:
        duplicates_csv_file = 'duplicate_projects.csv'
        write_csv(duplicates_csv_file, duplicates, header)
        print(f"Duplicate projects CSV file '{duplicates_csv_file}' has been created.")
    else:
        print("No duplicate projects found.")

if __name__ == "__main__":
    main()
