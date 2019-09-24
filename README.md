# pynilu
Python3 interface to api.nilu.no

```python
from pynilu.api import NiluApiInterface

nilu = NiluApiInterface(["Bankplassen"], ["Lillehammer"])

sensors = nilu.get_sensors()

for sensor in sensors:
    print(sensor.value())
```# pysensi
