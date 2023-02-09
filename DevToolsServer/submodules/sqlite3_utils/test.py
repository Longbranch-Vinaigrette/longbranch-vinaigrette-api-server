from __init__ import Sqlite3Utils

repository_settings = \
    Sqlite3Utils(
        "/home/felix/.devgui/database/dev_gui.db",
        "repository_settings")
data = repository_settings.run_query(
"""
SELECT * FROM repository_settings
	WHERE user='FelixRiddle'
INTERSECT
	SELECT * FROM repository_settings
		WHERE name='test6'
""")
print("Data obtained: ", data)
print("Its type: ", type(data))
