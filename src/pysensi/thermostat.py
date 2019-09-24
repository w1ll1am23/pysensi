import json

class SensiThermostat:

    def __init__(self, api_interface, state_json):
        self.api = api_interface
        self.state = state_json
        self._temperature = None
        self._humidity = None
        self._mode = None
        self._unit_type = None

    @property
    def id(self):
        return self.state.get("icd_id")

    @property
    def name(self):
        return self.state.get("registration").get("name")

    @property
    def cool_range(self):
        return self.state.get("capabilities").get("min_cool_setpoint"), self.state.get("capabilities").get("max_cool_setpoint")
    
    @property
    def heat_range(self):
        return self.state.get("capabilities").get("min_heat_setpoint"), self.state.get("capabilities").get("max_heat_setpoint")

    @property
    def modes(self):
        _modes = []
        for mode, enabled in self.state.get("capabilities").get("operating_mode_settings").items():
            if mode not in _modes and enabled == "yes":
                _modes.append(mode)
        return _modes

    @property
    def fan_modes(self):
        _modes = []
        for mode, enabled in self.state.get("capabilities").get("fan_mode_settings").items():
            if mode not in _modes and enabled == "yes":
                _modes.append(mode)
        return _modes

    @property
    def temperature(self):
        try:
            _temp_temperature = self.state.get("state").get("display_temp")
            if _temp_temperature:
                self._temperature = _temp_temperature
        except AttributeError:
            pass
        return self._temperature

    @property
    def humidity(self):
        try:
            _temp_humidity = self.state.get("state").get("humidity")
            if _temp_humidity:
                self._humidity = _temp_humidity
        except AttributeError:
            pass
        return self._humidity

    @property
    def mode(self):
        try:
            _temp_mode = self.state.get("state").get("current_operating_mode")
            if _temp_mode:
                self._mode = _temp_mode
        except AttributeError:
            pass
        return self._mode

    @property
    def unit_type(self):
        try:
            _temp_unit_type = self.state.get("state").get("display_scale")
            if _temp_unit_type:
                self._unit_type = _temp_unit_type
        except AttributeError:
            pass
        return self._unit_type
    

    def update_state(self, state_json):
        self.state = state_json
        print(json.dumps(self.state))
        print(self.name)
        print(self.id)
        print(str(self.unit_type))
        print(str(self.mode))
        print(str(self.cool_range))
        print(str(self.heat_range))
        print(str(self.modes))
        print(str(self.temperature))
        print(str(self.humidity))
    
