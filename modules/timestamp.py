### Dates ###

# https://docs.python.org/es/3/library/datetime.html

from datetime import datetime
#from datetime import time
#from datetime import date
#from datetime import timedelta

def timestamp() -> str:
    ahora = datetime.now()
    ahora_hora = f"{ahora.hour}h{ahora.minute}m{ahora.second}s"
    ahora_fecha = f"{ahora.day}-{ahora.month}-{ahora.year}"
    return str(f"{ahora_fecha} {ahora_hora}")

#print(ahora_hora)
#print(ahora_fecha)
#print(timestamp)
