import pprint
import sqlite3

from . import sqlite_parser
from . import decoder


class Sqlite3Utils:
    debug = False
    
    # Table information
    table_name = ""
    
    # Sqlite3
    con = None
    cur = None
    
    def __init__(self,
                 path: str,
                 table_name: str,
                 parse_json: bool = True,
                 debug: bool = False):
        self.table_name = table_name
        self.parse_json = parse_json
        # Not used anymore, just keeping for backwards compatibility
        self.debug = debug

        self.con = sqlite3.connect(path)
        self.cur = self.con.cursor()

    def check_table_exists(self):
        """Check if a table exists on sqlite3"""
        table = self.table_name
        double_apostrophe = table.replace('\'', '\'\'')
        query = "SELECT name " \
                    "\tFROM sqlite_master" \
                        "\t\tWHERE type='table'" \
                        f"\t\tAND name='{double_apostrophe}'"
        result = self.cur.execute(query)
        result = result.fetchone()
    
        condition = result is not None and result[0] == self.table_name
        if condition:
            return True
        else:
            return False

    def delete_every_row(self):
        """Delete every row in the given table"""
        query = "DELETE FROM {0}".format(self.table_name)
        self.cur.execute(query)

    def get_columns_list(self):
        """Get the columns name, useful for checking if a key exists or not"""
        self.cur.execute(f"PRAGMA table_info({self.table_name})")
        descriptive_columns_list = self.cur.fetchall()

        # It looks like this
        # [(0, 'value', 'TEXT', 0, None, 0), (1, 'key', 'TEXT', 0, None, 0)]
        columns_name = []
        for item in descriptive_columns_list:
            columns_name.append(item[1])

        return columns_name

    def print_every_row(self):
        """Print every row"""
        self.cur.execute("SELECT * FROM {0}".format(self.table_name))
        print("EVERY ROW:")
    
        rows = self.cur.fetchall()
    
        i = 0
        for row in rows:
            print(" - ROW {0}: ".format(i), row)
            i += 1

    # Actions
    def create_table(self, data):
        """Create a table if it doesn't exist"""
        keywords = sqlite_parser.parse_sql(data)
        query = f"CREATE TABLE {self.table_name}({keywords})"

        # Create the table
        try:
            self.cur.execute(query)
        except Exception as ex:
            pass

    def add_new_fields(self, data: dict):
        """Add the new fields

        prev_data: Parsed table row to dictionary, in which, this function is going to
        insert the new rows"""
        # Get keys
        # prev_keys = prev_data.keys()
        # data_keys = self.parse_sql(data)
        new_keys = []
        
        for i, key in new_keys:
            # 1 Column name
            # 2 Var type
            var_type = sqlite_parser.parse_sql_data_type(data[key])
            
            if var_type == "null":
                var_type = "text"
            
            query = f"ALTER TABLE {self.table_name}\n" \
                    f"\tADD COLUMN {new_keys[i]} {var_type};"

            self.cur.execute(query)

    def get(self, unique_key_name: str, unique_key_val, decode_json: bool = False):
        """Get data from the database

        It defaults false, because almost 80% of this project uses it like that"""
        # Parse unique_key_val
        parsed_val = sqlite_parser.convert_to_sql_value(unique_key_val, debug=self.debug)
    
        # Get previous data
        prev_data_query = f"SELECT * FROM {self.table_name} " \
                          f"WHERE {unique_key_name + '=' + parsed_val};"
        self.cur.execute(prev_data_query)
        prev_data = self.cur.fetchall()

        # This may throw an error
        previous_data = sqlite_parser.convert_to_python_dict(
            prev_data,
            self.cur.description,
            debug=self.debug)

        # Decode json recursively
        if decode_json or self.parse_json:
            previous_data = decoder.decode_json_recursively(previous_data)
    
        return previous_data

    def run_query(self, query: str, decode_json: bool = False):
        """SQL get with multiple WHERE clauses example:
        SELECT * FROM repository_settings
            WHERE user='FelixRiddle'
        INTERSECT
            SELECT * FROM repository_settings
                WHERE name='test'
		This way you can add many conditions as you see fit, intersect will
		exclude those that don't meet the conditions.
		"""
        try:
            self.cur.execute(query)

            prev_data = self.cur.fetchall()
        except Exception as ex:
            raise Exception(ex)

        desc = self.cur.description
        previous_data = sqlite_parser.convert_to_python_dict(
            prev_data,
            desc,
            debug=self.debug)

        # Decode json
        if self.parse_json or decode_json:
            previous_data = decoder.decode_recursively_list_or_dict(previous_data)

        # In case is another kind of query, commit
        self.con.commit()
        return previous_data

    def get_all(self):
        """Get all rows"""
        query = f"SELECT * FROM {self.table_name}"
        self.cur.execute(query)
        data = self.cur.fetchall()
        
        # First time use, throws an error
        previous_data = None
        try:
            desc = self.cur.description
            previous_data = sqlite_parser.convert_to_python_dict(
                data,
                desc,
                debug=self.debug,
            )
        except Exception as ex:
            pass
        
        return previous_data

    def fetch_one_random(self):
        """Fetch a single random item"""
        self.cur.execute(
            f"""SELECT * FROM {self.table_name}\n
            \tORDER BY RANDOM()
            \t\tLIMIT 1;""")
        data = sqlite_parser.convert_to_python_dict(
            self.cur.fetchall(),
            self.cur.description,
            debug=self.debug)

        # Decode json
        if self.parse_json:
            data = decoder.decode_recursively_list_or_dict(data)
        return data

    def add_missing_columns(self, data: dict):
        """If the data object has keys that don't exist on the table
        this function adds those keys as columns"""
        # Columns list
        columns_list = self.get_columns_list()

        # Make a list out of data keys, because data.keys returns a different class
        data_columns = list(data.keys())
        for key in data_columns:
            # if not key in table_columns:
            if key not in columns_list:
                value_type = sqlite_parser.parse_sql_data_type(data[key], null_as_text=True)
                # query = "ALTER TABLE {0} ADD COLUMN {1} {2};".format(self.table_name, key, value_type)
                query = f"ALTER TABLE {self.table_name}\n" \
                        f"\tADD COLUMN {key} {value_type};"

                self.cur.execute(query)
        return True

    def add_new_columns(self, data):
        """Alias for add_missing_columns"""
        return self.add_missing_columns(data)

    def get_filtered(self, filterA: dict):
        """Get data filtered by key-value pairs in the filter parameter"""
        first_key = list(filterA.keys())[0]
        get_previous_data_query = f"""SELECT * FROM {self.table_name}
                WHERE {first_key}='{filterA[first_key]}'"""

        # Add every key in the dictionary
        i = 0
        for key, value in filterA.items():
            # Skip the first, because it was added before
            if not i == 0:
                get_previous_data_query += f"""
                    INTERSECT
                        SELECT * FROM {self.table_name}
                            WHERE {key}='{value}'"""

            i += 1

        # Get data
        data = self.run_query(get_previous_data_query)

        # Check if parse_json is enabled
        if self.parse_json:
            data = decoder.decode_json_recursively(data)

        return data

    def update_filtered(self, data: dict, filterA: dict):
        """Update data where the data in filterA matches"""
        comma_separated_keywords = sqlite_parser.parse_sql(data, mode="commaSeparatedKeys")
        comma_separated_values = sqlite_parser.parse_sql(data, mode="commaSeparatedValues")

        first_key = list(filterA.keys())[0]

        # Reference/s:
        # https://stackoverflow.com/questions/8645773/sql-query-with-multiple-where-statements
        # Start the where clause with the unique_key_name
        where_clause = f"WHERE {first_key}=" \
                       f"{sqlite_parser.convert_to_sql_value(filterA[first_key], debug=self.debug)}"

        iteration = 1
        # Get the length items in the dictionary
        amount_of_dict_keys = len(list(filterA.keys()))
        if amount_of_dict_keys > 1:
            # Start the where clause with the unique_key_name
            where_clause = f"WHERE {first_key}=" \
                           f"{sqlite_parser.convert_to_sql_value(filterA[first_key], debug=self.debug)}" \
                           f" and"

            # Iterate through every key and value
            for key, value in filterA.items():
                # print("Iteration: ", iteration)
                if not iteration == 1:
                    # While iteration is less than the amount of keys adds a comma at the end
                    # print(f"Is iteration less than keys?: {iteration < amount_of_dict_keys}")
                    if iteration < amount_of_dict_keys:
                        where_clause += f" {key}=" \
                                        f"{sqlite_parser.convert_to_sql_value(value, debug=self.debug)}" \
                                        f" and"
                    else:
                        # Otherwise add a parenthesis
                        where_clause += f" {key}=" \
                                        f"{sqlite_parser.convert_to_sql_value(value, debug=self.debug)}"
                iteration += 1

        update_query = f"UPDATE {self.table_name} \n" \
                       f"\tSET ({comma_separated_keywords})=\n" \
                       f"\t\t({comma_separated_values}) \n" \
                       f"\t\t\t{where_clause};"

        self.cur.execute(update_query)
        self.con.commit()

    def insert_replace(self,
                       data: dict,
                       unique_key_name: str = "",
                       unique_key_val=None,
                       intersect_dict=None):
        """Insert or replace data in sqlite3

        Intersect dict should be a dictionary with key-value pairs that further filter the
        results of the query to obtain the requested data.
        Note: This function doesn't delete previous data from the same row

        This was the first version of the function which has been completely replaced by
        version 2, now this function just implements the v2 internally."""
        filterA = {
            unique_key_name: unique_key_val
        }

        # If it's a dict, add the data to the filter
        if isinstance(intersect_dict, dict):
            filterA = {
                **filterA,
                **intersect_dict
            }

        # Just use the version 2 to do the dirty work
        return self.insert_replace_v2(
            data,
            filterA)

    def insert_replace_v2(self, data: dict, filterA: dict):
        """Insert or replace version 2

        Note: This function doesn't delete previous data from the same row"""
        # Create the table if it doesn't exist
        self.create_table(data)

        # Get previous data
        previous_data: dict = {}
        try:
            # Get data
            previous_data = self.get_filtered(filterA)
        except Exception as ex:
            # Previous data doesn't exist
            pass

        # Add new columns
        self.add_missing_columns(data)

        # Insert or update(upsert) functionality
        new_data = data
        if isinstance(new_data, dict):
            new_data = {**previous_data, **data}

        # Check if it exists in the database already or not
        if len(previous_data.keys()) <= 0:
            # It doesn't exist, then create it
            comma_separated_keywords = sqlite_parser.parse_sql(
                new_data, mode="commaSeparatedKeys")
            comma_separated_values = sqlite_parser.parse_sql(
                new_data, mode="commaSeparatedValues")

            update_query = f"INSERT INTO {self.table_name} ({comma_separated_keywords})\n" \
                           f"\tVALUES({comma_separated_values});"

            self.cur.execute(update_query)

            self.con.commit()
        else:
            return self.update_filtered(data, filterA)

    def upsert(self, data: dict, filterA: dict):
        """Alias for insert_replace_v2"""
        return self.insert_replace_v2(data, filterA)
