# Define environment variables
$access_token = $env:SPLUNK_ACCESS_TOKEN
$realm = 'eu0'
$network_share_path = '\\fs-0b060f4317a02b1fa.rxtest.local\share'
$file_name = "testfile.txt"
$file_path = Join-Path -Path $network_share_path -ChildPath $file_name

# Function to create a file
Function Create-File($file_path) {
    Try {
        Set-Content -Path $file_path -Value "This is a test file."
    }
    Catch [System.IO.IOException] {
        Write-Host "An error occurred while creating the file: $_"
    }
    Catch {
        Write-Host "An unexpected error occurred: $_"
    }
}

# Function to test if the file exists
Function Test-File($file_path, $file_name) {
    If (Test-Path -Path $file_path) {
        Write-Host "File '$file_name' was successfully created on the network share."
        Return "1"
    }
    Else {
        Write-Host "Failed to create the file '$file_name' on the network share."
        Return "2"
    }
}

# Function to send create success metric
Function O11Y-Create-Success($create_result_message) {
    $endpoint = "https://ingest.$realm.signalfx.com/v2/datapoint"
    $headers = @{
        'Content-Type' = 'application/json'
        'X-SF-Token'   = $access_token
    }

    $metric_data = @{
        "gauge" = @(
            @{
                "metric" = "fsx_write_result"
                "value"  = $create_result_message
            }
        )
    }

    Try {
        # Send the metric data to Splunk Observability
        $response = Invoke-RestMethod -Uri $endpoint -Method Post -Headers $headers -Body ($metric_data | ConvertTo-Json)

        # Check the response
        If ($response.StatusCode -eq 200) {
            Write-Host "Metric sent successfully!"
        }
        Else {
            Write-Host "Failed to send metric. Status code: $($response.StatusCode)"
            Write-Host $response.Content
        }
    }
    Catch {
        Write-Host "An error occurred: $_"
    }
}

# Function to delete a file
Function Delete-File($file_path, $file_name) {
    Try {
        Remove-Item -Path $file_path -ErrorAction Stop
        Write-Host "File '$file_name' was successfully deleted from the network share."
        Return "1"
    }
    Catch [System.IO.FileNotFoundException] {
        Write-Host "The file '$file_name' does not exist on the network share."
        Return "2"
    }
    Catch {
        Write-Host "An error occurred while deleting the file: $_"
        Return "3"
    }
}

# Function to send delete success metric
Function O11Y-Delete-Success($delete_result_message) {
    $endpoint = "https://ingest.$realm.signalfx.com/v2/datapoint"
    $headers = @{
        'Content-Type' = 'application/json'
        'X-SF-Token'   = $access_token
    }

    $metric_data = @{
        "gauge" = @(
            @{
                "metric" = "fsx_delete_result"
                "value"  = $delete_result_message
            }
        )
    }

    Try {
        # Send the metric data to Splunk Observability
        $response = Invoke-RestMethod -Uri $endpoint -Method Post -Headers $headers -Body ($metric_data | ConvertTo-Json)

        # Check the response
        If ($response.StatusCode -eq 200) {
            Write-Host "Metric sent successfully!"
        }
        Else {
            Write-Host "Failed to send metric. Status code: $($response.StatusCode)"
            Write-Host $response.Content
        }
    }
    Catch {
        Write-Host "An error occurred: $_"
    }
}

# Create the file
Create-File -file_path $file_path

# Pause to enable testing
Read-Host "Press enter to continue"

# Test the file creation and send metrics
$create_result_message = Test-File -file_path $file_path -file_name $file_name
O11Y-Create-Success -create_result_message $create_result_message

# Pause to enable testing
Read-Host "Press enter to continue"

# Delete the file
$delete_result_message = Delete-File -file_path $file_path -file_name $file_name
O11Y-Delete-Success -delete_result_message $delete_result_message
