import json
import requests
import logging
import uuid
import datetime
import time
import asyncio
import websockets
import re
from enum import Enum
try:
    import thread
except ImportError:
    import _thread as thread
import time

from .thermostat import SensiThermostat

OAUTH_URL = "https://oauth.sensiapi.io/token?device={}"
START_WS_URL = "wss://rt.sensiapi.io/thermostat/?EIO=3&capabilities=display_humidity,operating_mode_settings,fan_mode_settings,indoor_equipment,outdoor_equipment,indoor_stages,outdoor_stages,continuous_backlight,degrees_fc,display_time,keypad_lockout,temp_offset,compressor_lockout,boost,heat_cycle_rate,heat_cycle_rate_steps,cool_cycle_rate,cool_cycle_rate_steps,aux_cycle_rate,aux_cycle_rate_steps,early_start,min_heat_setpoint,max_heat_setpoint,min_cool_setpoint,max_cool_setpoint,circulating_fan,humidity_control,humidity_offset,humidity_offset_lower_bound,humidity_offset_upper_bound,temp_offset_lower_bound,temp_offset_upper_bound&transport=websocket"

CLIENT_SECRET = "XBF?Z9U6;x3bUwe^FugbL=4ksvGjLnCQ"
CLIENT_ID = "android"

DEVICES = {}

OAUTH = {"Authorization": None}

_LOGGER = logging.getLogger(__name__)

THERMOSTATS = {}


class SensiApiInterface:

    def __init__(self, username, password):
        """Create a Sensi API interface."""
        self.username = username
        self.password = password
        self.device = uuid.uuid4()
        self._login_and_get_token()
        self.access_token = ""
        self.refresh_token = ""
        self.expires_at = datetime.datetime.now()

    def _login_and_get_token(self):
        _response = requests.post(OAUTH_URL.format(self.device), data={"username": self.username, "password": self.password, "client_id": CLIENT_ID, "client_secret": CLIENT_SECRET, "grant_type": "password"}, verify=False)
        if _response.status_code != 200:
            _LOGGER.error("Failed to log in")
        else:
            _response_json = _response.json()
            self.access_token = _response_json.get("access_token")
            OAUTH["Authorization"] = "Bearer " + self.access_token
            self.refresh_token = _response_json.get("refresh_token")
            #Expire it 30 minutes early
            self.expires_at = datetime.datetime.now() + datetime.timedelta(seconds=_response_json.get("expires_in") - 1800)
        print("access_token: " + self.access_token)
        print("refresh_token: " + self.refresh_token)

    async def _async_start_ws_connection(self):
        
        async with websockets.connect(START_WS_URL, extra_headers=OAUTH) as websocket:
            asyncio.ensure_future(self._run_keep_alive(websocket))
            while True:
                ws_response = await websocket.recv()
                #print(ws_response)
                prased_response = parse_ws_response(ws_response)
                if prased_response:
                    # response type and json body
                    route_response(self, prased_response[0], prased_response[1])
                else:
                    # Do nothing I guess...
                    pass

    async def _run_keep_alive(self, websocket):
        while True:
            await asyncio.sleep(30)
            await websocket.send('2')

    def start_ws_connection(self):
        """Get the data from the API."""
        asyncio.get_event_loop().run_until_complete(self._async_start_ws_connection())

def route_response(api_interface, response_type, response_json):
    if response_type == "42":
        if "state" in response_json:
            for device in response_json[1]:
                _id = device.get("icd_id")
                _device = DEVICES.get(_id)
                if _device:
                    _device.update_state(device)
                else:
                    DEVICES[_id] = SensiThermostat(api_interface, device)

def parse_ws_response(response):
        list_of_non_digits = re.findall(r'\D', response[:10])
        if list_of_non_digits:
            response_type = response[:response.find(list_of_non_digits[0])]
            start_of_json = response.find(list_of_non_digits[0])
            parsed_json = None
            try:
                parsed_json = json.loads(response[start_of_json:])
            except:
                parsed_json = None
            return response_type, parsed_json
        else:
            # regex failed
            return None
