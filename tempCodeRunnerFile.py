class DBConnection:
  def __init__(self, user, password, host, port):
    self.password = password
    self.user = user
    self.host = host
    self.port = port
    self.config = {
    #   'user': self.user,
    #   'password': self.password,
    #   'host': self.host,
    #   'port': self.port,
        'user': 'root',
        'password': 'legends',
        'host': '127.0.0.1',
        'port': '3306',
        'database': 'league'
    }
    self.connection = None