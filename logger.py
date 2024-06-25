import csv
import os
import datetime

path = './logs/'
header = ['Time', 'Channel_A', 'Channel_B', 'Channel_C']

def log_action(action):
    """
    Logs the given action to a file.

    Parameters:
    - action (str): The action to be logged.

    Returns:
    None
    """
    directory = create_folder()
    file_path = os.path.join(directory, 'actions.txt')
    with open(file_path, 'a') as file:
        current_time = datetime.datetime.now().strftime("%H:%M:%S")
        file.write(f"[{current_time}] - {action}\n")

def log_values(values, max_size_mb=15):
    """
    Logs the given values to a file.

    Parameters:
    - values (list): The values to be logged.
    - max_size_mb (int): The maximum size of the log file in MB.

    Returns:
    None
    """
    directory = create_folder()
    if check_csv_file_size(directory, max_size_mb):
        file_path = add_csv_file(directory)
    else:
        latest_file = get_latest_csv_file(directory)
        file_path = os.path.join(directory, latest_file)
    
    write_values(file_path, values)

def create_folder():
    """
    Creates a folder with the current date as the name.

    Returns:
        str: The path of the created folder.
    """
    today = datetime.date.today()
    folder_name = today.strftime("%Y-%m-%d")
    folder_path = os.path.join(path, folder_name)
    
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    
    return folder_path

def add_csv_file(directory):
    """
    Creates a new CSV file in the specified directory with a unique name.
    
    Args:
        directory (str): The directory where the CSV file should be created.
        
    Returns:
        str: The path of the newly created CSV file.
    """
    file_name = "1"
    file_path = os.path.join(directory, file_name + ".csv")
    count = 1
    
    while os.path.exists(file_path):
        count += 1
        file_name = str(count)
        file_path = os.path.join(directory, file_name + ".csv")
    
    with open(file_path, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(header)
        
    return file_path

def write_values(file_path, values):
    """
    Appends a row of values to a CSV file.

    Args:
        file_path (str): The path to the CSV file.
        values (list): The list of values to be written as a row.

    Returns:
        None
    """
    with open(file_path, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(values)

def check_csv_file_size(directory, max_size_mb):
    """
    Check if the size of the latest CSV file in the given directory exceeds the maximum size.

    Args:
        directory (str): The directory path to check for files.
        max_size_mb (float): The maximum file size in megabytes.

    Returns:
        bool: True if the size of the latest file is greater than the maximum size, False otherwise.
    """
    if directory is None:
        return True
    if not os.listdir(directory):
        return True
    
    latest_file = get_latest_csv_file(directory)
    if latest_file is None:
        return True
    file_path = os.path.join(directory, latest_file)
    file_size_mb = os.path.getsize(file_path) / (1024 * 1024)  # Convert to MB
    
    return file_size_mb > max_size_mb

def get_latest_csv_file(directory):
    """
    Returns the name of the latest CSV file in the specified directory.

    Args:
        directory (str): The directory path.

    Returns:
        str: The name of the latest file in the directory, or None if the directory is empty.
    """
    files = os.listdir(directory)
    if not files:
        return None
    latest_file = None
    latest_time = 0

    for file in files:
        if file.endswith('.csv'):
            file_path = os.path.join(directory, file)
            file_time = os.path.getctime(file_path)
            if file_time > latest_time:
                latest_file = file
                latest_time = file_time

    return latest_file
# © AIMA DEVELOPPEMENT 2024