import sqlite3

conn = sqlite3.connect("users.db")
c = conn.cursor()

# Code to ensure that there is always an Admin and Employee account on the server.
c.execute("INSERT INTO users VALUES ('username', 'password', 'role')")
conn.commit()

# Close the connection
conn.close()
