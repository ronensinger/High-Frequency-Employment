import time

class Initiate:
  def __init__(self):
    self.first_time = time.time()
    self.last_time = time.time()
  
  def time(self):
    ping = round((time.time() - self.last_time) * 1000, 3)
    self.last_time = time.time()
    return ping
  
  def finished(self):
    ping = round((time.time() - self.first_time) * 1000, 3)
    return ping