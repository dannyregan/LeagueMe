def ensure_connection(connection):
    if not connection.is_connected():
        connection.reconnect()
    return connection
