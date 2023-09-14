import os
import json
import requests

access_token = os.getenv('SPLUNK_ACCESS_TOKEN')
realm = os.getenv('SPLUNK_REALM')
fsx_share_path = os.getenv('FSX_SHARE_PATH')
network_share_path = rf"\\{fsx_share_path}"
file_name = os.getenv('FSX_FILE_NAME')
file_path = os.path.join(network_share_path, file_name)

def CREATE_FILE(file_path):
    try:
        with open(file_path, "w") as file:
            file.write("This is a test file.")
    except IOError as e:
        print(f"An error occurred while creating the file: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def TEST_FILE(file_path, file_name):
    if os.path.exists(file_path):
        print(f"File '{file_name}' was successfully created on the network share.")
        return f"1"
    else:
        print(f"Failed to create the file '{file_name}' on the network share.")
        return f"2"

def O11Y_CREATE_SUCCESS(create_result_message):
    endpoint = 'https://ingest.' + realm + '.signalfx.com/v2/datapoint'
    headers = {
        'Content-Type': 'application/json',
        'X-SF-Token': access_token
    }

    metric_data = {
        "gauge": [
            {
                "metric": "fsx_write_result",
                "value": create_result_message,
                "dimensions": {
                    "region": "us-west",
                    "environment": "production",
                    "datacenter": "dc-1"
                }
            }
        ]
    }
    
    try:
        # Send the metric data to Splunk Observability
        response = requests.post(endpoint, data=json.dumps(metric_data), headers=headers)
        
        # Check the response
        if response.status_code == 200:
            print("Metric 'fsx_write_result' sent successfully!")
        else:
            print(f"Failed to send metric 'fsx_write_result'. Status code: {response.status_code}")
            print(response.text)

    except Exception as e:
        print(f"An error occurred: {str(e)}")


def DELETE_FILE(file_path, file_name):
    try:
        os.remove(file_path)
        print(f"File '{file_name}' was successfully deleted from the network share.")
        return f"1"
    except FileNotFoundError:
        print(f"The file '{file_name}' does not exist on the network share.")
        return f"2"
    except Exception as e:
        print(f"An error occurred while deleting the file: {str(e)}")
        return f"3"


def O11Y_DELETE_SUCCESS(delete_result_message):
    endpoint = 'https://ingest.' + realm + '.signalfx.com/v2/datapoint'
    headers = {
        'Content-Type': 'application/json',
        'X-SF-Token': access_token
    }

    metric_data = {
        "gauge": [
            {
                "metric": "fsx_write_result",
                "value": create_result_message,
                "dimensions": {
                    "region": "us-west",
                    "environment": "production",
                    "datacenter": "dc-1"
                }
            }
        ]
    }
    
    try:
        # Send the metric data to Splunk Observability
        response = requests.post(endpoint, data=json.dumps(metric_data), headers=headers)
        
        # Check the response
        if response.status_code == 200:
            print("Metric 'fsx_delete_result' sent successfully!")
        else:
            print(f"Failed to send metric 'fsx_delete_result'. Status code: {response.status_code}")
            print(response.text)

    except Exception as e:
        print(f"An error occurred: {str(e)}")


CREATE_FILE(file_path)

# pause to enable testing
input("Press enter to continue")

create_result_message=TEST_FILE(file_path, file_name)
O11Y_CREATE_SUCCESS(create_result_message)

# pause to enable testing
input("Press enter to continue")

delete_result_message=DELETE_FILE(file_path, file_name)
O11Y_DELETE_SUCCESS(delete_result_message)
