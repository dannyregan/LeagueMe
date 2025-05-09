# A helper function to ensure connection is maintained with the database
# I wasn't sure why, but the database routinely lost connection when buttons were clicked
# This function prevents that from crashing the app
def ensure_connection(connection):
    if not connection.is_connected():
        connection.reconnect()
    return connection
