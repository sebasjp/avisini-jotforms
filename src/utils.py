import os
import json
from datetime import datetime
from pytz import timezone


def saveJson(data: list, path_write: str):
    
  bogota_tz = timezone('America/Bogota')
  now_bogota = datetime.now(bogota_tz)
  now_str = now_bogota.strftime('%Y%m%d') # Format the datetime object

  with open(path_write.format(now_str=now_str), 'w') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)


def readJson(path_read: str):

  bogota_tz = timezone('America/Bogota')
  now_bogota = datetime.now(bogota_tz)
  now_str = now_bogota.strftime('%Y%m%d') # Format the datetime object

  with open(path_read.format(now_str=now_str), 'r') as f:
    data = json.load(f)

  return data