import requests
from requests.auth import HTTPBasicAuth
import os
import json

# Set the URL and credentials
base_url = "https://ca1.p6.oraclecloud.com/metrolinx/cloudapi/restapi"
username = "armank"
password = "Barin1234/"

# Set the headers
headers = {
    "Accept": "application/json",
    "Version": "2"
}

# Get the directory where this script is located
save_directory = os.path.dirname(os.path.abspath(__file__))

# Function to get application roles
def get_application_roles():
    roles_url = f"{base_url}/roles"
    response = requests.get(roles_url, auth=HTTPBasicAuth(username, password), headers=headers, verify=False)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to retrieve roles. Status code: {response.status_code}")
        print(response.text)
        return None

# Function to get users
def get_users():
    users_url = f"{base_url}/user"
    response = requests.get(users_url, auth=HTTPBasicAuth(username, password), headers=headers, verify=False)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to retrieve users. Status code: {response.status_code}")
        print(response.text)
        return None

# Retrieve all roles
roles_data = get_application_roles()
if roles_data:
    # Updated role mapping based on the actual roles found in your user data
    role_mapping = {
        "BI Publisher": {
            "BICpglevel3Authors", "BICpglevel3Consumers", "BICpglevel3Superusers",
            "BIDevAuthors", "BIDevConsumers", "BIDevSuperusers",
            "BIProductionAuthors", "BIProductionConsumers", "BIProductionSuperusers",
            "BIStageAuthors", "BIStageConsumers", "BIStageSuperusers",
            "BITestAuthors", "BITestConsumers", "BITestSuperusers",
            "BITrainAuthors", "BITrainConsumers", "BITrainSuperusers"
        },
        "Primavera Analytics": {
            "PrimaveraAnalyticsDev", "PrimaveraAnalyticsProduction", "PrimaveraAnalyticsStage",
            "PrimaveraAnalyticsTest", "PrimaveraAnalyticsTrain"
        },
        "Primavera Data Services": {
            "PrimaveraDataServicesCpglevel3", "PrimaveraDataServicesDev",
            "PrimaveraDataServicesProduction", "PrimaveraDataServicesStage",
            "PrimaveraDataServicesTest"
        },
        "Primavera Gateway": {
            "PrimaveraGatewayCpglevel3Admin", "PrimaveraGatewayCpglevel3AdminNoData",
            "PrimaveraGatewayCpglevel3Developer", "PrimaveraGatewayCpglevel3User",
            "PrimaveraGatewayCpglevel3UserNoData", "PrimaveraGatewayDevAdmin",
            "PrimaveraGatewayDevAdminNoData", "PrimaveraGatewayDevDeveloper",
            "PrimaveraGatewayDevUser", "PrimaveraGatewayDevUserNoData",
            "PrimaveraGatewayProductionAdmin", "PrimaveraGatewayProductionAdminNoData",
            "PrimaveraGatewayProductionDeveloper", "PrimaveraGatewayProductionUser",
            "PrimaveraGatewayProductionUserNoData", "PrimaveraGatewayStageAdmin",
            "PrimaveraGatewayStageAdminNoData", "PrimaveraGatewayStageDeveloper",
            "PrimaveraGatewayStageUser", "PrimaveraGatewayStageUserNoData",
            "PrimaveraGatewayTestAdmin", "PrimaveraGatewayTestAdminNoData",
            "PrimaveraGatewayTestDeveloper", "PrimaveraGatewayTestUser",
            "PrimaveraGatewayTestUserNoData", "PrimaveraGatewayTrainAdmin",
            "PrimaveraGatewayTrainAdminNoData", "PrimaveraGatewayTrainDeveloper",
            "PrimaveraGatewayTrainUser", "PrimaveraGatewayTrainUserNoData"
        },
        "Primavera P6": {
            "PrimaveraP6Cpglevel3", "PrimaveraP6Dev", "PrimaveraP6Production",
            "PrimaveraP6Stage", "PrimaveraP6Test", "PrimaveraP6Train"
        },
        "Primavera Unifier": {
            "PrimaveraUnifierCpglevel3", "PrimaveraUnifierDev", "PrimaveraUnifierProduction",
            "PrimaveraUnifierStage", "PrimaveraUnifierTest", "PrimaveraUnifierTrain",
            "PrimaveraVirtualDesktopUser"
        },
        "Cloud Administrator": {"PrimaveraCloudAdmin"},
        "Communication Administrator": {"PrimaveraCommunicationAdmin"}
    }

    # Initialize a dictionary to hold users by application
    app_data = {app: [] for app in role_mapping.keys()}

    # Retrieve all users
    users_data = get_users()
    if users_data:
        print(f"Number of users retrieved: {len(users_data)}")

        # Filter and categorize only active users based on their roles
        for user in users_data:
            if user.get("status") == "Active":  # Filter for active users
                user_roles = {role.get("name") for role in user.get("roles", [])}
                user_info = {
                    "loginId": user.get("loginId"),
                    "emailAddress": user.get("emailAddress"),
                    "firstName": user.get("firstName"),
                    "lastName": user.get("lastName"),
                    "roles": list(user_roles),
                    "status": user.get("status"),
                    "createdDate": user.get("createdDate"),
                    "updatedDate": user.get("updatedDate")
                }
                for app_name, roles in role_mapping.items():
                    if roles & user_roles:
                        app_data[app_name].append(user_info)

        # Save data to JSON
        json_file_path = os.path.join(save_directory, "active_users_by_application.json")
        with open(json_file_path, "w") as json_file:
            json.dump(app_data, json_file, indent=4)
        
        print(f"Data saved to {json_file_path}")

else:
    print("Failed to retrieve roles or users.")
