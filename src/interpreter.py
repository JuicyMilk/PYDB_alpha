import os
import re

import errors as err

class Interpreter:
    def __init__(self, db_file: str):
        self.db = db_file
        self.script_lines = []
        self.db_name = ''
        self.db_groups = []
        self.db_entries = []
    
    def check_db_file(self):
        """checks if provided DB path is valid"""
        if os.path.exists(self.db):
            if self.db.endswith('.pydb'):
                return True
            else:
                raise err.FileNotDB      # TODO use errors instead of return False
        else:
            raise err.DatabaseNotFound

    def get_script(self):
        """gets DB script line for line and stores it in self.db_script_lines"""
        self.check_db_file()
        self.script_lines.clear()

        lines = []

        with open(self.db) as db_reader:
            for line in db_reader.readlines():
                lines.append(line)
        lines = [line.replace('\n', '') for line in lines]

        # checks if DB_NAME occurres more than one time, raises error if it does
        db_name_occurrencies = 0
        for line in lines:
            if 'DB_NAME' in line:
                db_name_occurrencies += 1
                self.db_name = re.findall(r'DB_NAME\["(.*?)"\]', lines[0])[0]

            if db_name_occurrencies > 1:
                raise err.InterpretError

        if self.db_name == '':
            self.db_name = 'N/A'
            
        # stores script
        self.script_lines = lines

    def get_groups(self):
        """gets DB group names from self.script_lines and saves them in self.db_groups"""
        self.check_db_file()
        self.db_groups.clear()

        groups = []
        
        for line in self.script_lines:
            if re.findall(r'GROUP\[name="(.*?)"]', line):
                groups.append(re.findall(r'GROUP\[name="(.*?)"]', line)[0])
        
        for group in groups:
            self.db_groups.append(group)
        
        for group in self.db_groups:
            if self.db_groups.count(group) > 1:
                raise err.InterpretError
    
    def get_entries(self):
        self.check_db_file()
        self.db_entries.clear()

        entries = []

        for line in self.script_lines:
            if re.findall(r'ENTRY\[id="(.*?)", name="(.*?)"]'):
                entries.append(re.findall(r'ENTRY\[id="(.*?)", name="(.*?)"]')[0])
