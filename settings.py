import os

class Settings:
    """
    A class that manages application settings.

    Attributes:
        file_path (str): The file path of the settings file.

    Methods:
        __init__(): Initializes the Settings object.
        create_settings_file(): Creates the settings file if it doesn't exist.
        write_to_settings_file(setting, value): Writes a setting and its value to the settings file.
        read_from_settings_file(setting): Reads the value of a setting from the settings file.
    """

    def __init__(self):
        self.file_path = "./utils/settings.conf"
        if not os.path.exists(self.file_path):
            self.create_settings_file()

    def create_settings_file(self):
        """
        Creates the settings file if it doesn't exist.
        """
        directory = os.path.dirname(self.file_path)
        if not os.path.exists(directory):
            os.makedirs(directory)
        
        if not os.path.exists(self.file_path):
            with open(self.file_path, "w") as file:
                pass
            return True
        return False

    def write_to_settings_file(self, setting, value):
        """
        Writes a setting and its value to the settings file.

        Args:
            setting (str): The name of the setting.
            value: The value of the setting.

        Returns:
            bool: True if the write operation is successful, False otherwise.
        """
        if os.path.exists(self.file_path):
            with open(self.file_path, "r+") as file:
                lines = file.readlines()
                file.seek(0)
                found = False
                for line in lines:
                    if line.startswith(f"{setting} = "):
                        file.write(f"{setting} = {value}\n")
                        found = True
                    else:
                        file.write(line)
                if not found:
                    file.write(f"{setting} = {value}\n")
                file.truncate()
            return True
        return False

    def read_from_settings_file(self, setting):
        """
        Reads the value of a setting from the settings file.

        Args:
            setting (str): The name of the setting.

        Returns:
            str or None: The value of the setting if found, None otherwise.
        """
        if os.path.exists(self.file_path):
            with open(self.file_path, "r") as file:
                for line in file:
                    s, value = line.strip().split(" = ")
                    if s == setting:
                        return value
        return None
    
    def does_setting_exist(self, setting):
        """
        Checks if a setting exists in the settings file.

        Args:
            setting (str): The name of the setting.

        Returns:
            bool: True if the setting exists, False otherwise.
        """
        if os.path.exists(self.file_path):
            with open(self.file_path, "r") as file:
                for line in file:
                    s, _ = line.strip().split(" = ")
                    if s == setting:
                        return True
        return False
# Développé par Noa Second