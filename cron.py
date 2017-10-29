from datetime import datetime
from threading import Timer
import os

x=datetime.today()
print(x)
y=x.replace(day=x.day, hour=8, minute=30, second=1)
delta_t=y-x

secs=delta_t.seconds+1

def run_algo():
  os.system('nohup python /root/HFT/assassin.py')

t = Timer(secs, run_algo)
t.start()