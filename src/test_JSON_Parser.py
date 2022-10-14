# coding: utf8

import unittest
import time
import json
import random


class hsl20_4:
    LOGGING_NONE = 0

    def __init__(self):
        pass

    class BaseModule:
        debug_output_value = {}  # type: {int, any}
        debug_set_remanent = {}  # type: {int, any}
        debug_input_value = {}  # type: {int: any}

        def __init__(self, a, b):
            self.module_id = 0

        def _get_framework(self):
            f = hsl20_4.Framework()
            return f

        def _get_logger(self, a, b):
            return 0

        def _get_remanent(self, key):
            # type: (str) -> any
            return 0

        def _set_remanent(self, key, val):
            # type: (str, any) -> None
            self.debug_set_remanent = val

        def _set_output_value(self, pin, value):
            # type: (int, any) -> None
            self.debug_output_value[int(pin)] = value
            print (str(time.time()) + "\t# Out: pin " + str(pin) + " <- \t" + str(value))

        def _set_input_value(self, pin, value):
            # type: (int, any) -> None
            self.debug_input_value[int(pin)] = value
            print "# In: pin " + str(pin) + " -> \t" + str(value)

        def _get_input_value(self, pin):
            # type: (int) -> any
            if pin in self.debug_input_value:
                return self.debug_input_value[pin]
            else:
                return 0

        def _get_module_id(self):
            # type: () -> int
            if self.module_id == 0:
                self.module_id = random.randint(1, 1000)
            return self.module_id

    class Framework:
        def __init__(self):
            self.my_ip = "127.0.0.1"

        def _run_in_context_thread(self, a):
            pass

        def create_debug_section(self):
            d = hsl20_4.DebugHelper()
            return d

        def get_homeserver_private_ip(self):
            # type: () -> str
            return self.my_ip

        def get_instance_by_id(self, id):
            # type: (int) -> str
            return ""

    class DebugHelper:
        def __init__(self):
            pass

        def set_value(self, cap, text):
            print(str(time.time()) + "\tValue:\t'" + str(cap) + "': " + str(text))

        def add_message(self, msg):
            print(str(time.time()) + "\tMsg:  \t" + str(msg))


##!!!!##################################################################################################
#### Own written code can be placed above this commentblock . Do not change or delete commentblock! ####
########################################################################################################
##** Code created by generator - DO NOT CHANGE! **##

class JSON_Parser_11087_11087(hsl20_4.BaseModule):

    def __init__(self, homeserver_context):
        hsl20_4.BaseModule.__init__(self, homeserver_context, "hsl20_4_json")
        self.FRAMEWORK = self._get_framework()
        self.LOGGER = self._get_logger(hsl20_4.LOGGING_NONE, ())
        self.PIN_I_SJSON = 1
        self.PIN_I_SKEY = 2
        self.PIN_I_NIDX = 3
        self.PIN_O_SVALUE = 1
        self.PIN_O_FVALUE = 2

########################################################################################################
#### Own written code can be placed after this commentblock . Do not change or delete commentblock! ####
###################################################################################################!!!##

    def get_list_element(self, s_json, n_index):
        json_file = json.loads(s_json)

        if isinstance(json_file, list):
            if n_index < len(json_file):
                return json.dumps(json_file[n_index])

        return "{}"

    def get_value(self, s_json, s_key):
        json_file = json.loads(s_json)
        ret = ""
        if s_key in json_file:
            val = json_file[s_key]

            if (isinstance(val, dict)
                    or isinstance(val, list)):
                ret = json.dumps(val)
            else:
                ret = val
        else:
            self.DEBUG.add_message("Error: Key not found.")

        if isinstance(ret, str):
            ret = ret.encode("ascii", "xmlcharrefreplace")

        return ret

    def on_init(self):
        self.DEBUG = self.FRAMEWORK.create_debug_section()

    def on_input_value(self, index, value):
        s_json = self._get_input_value(self.PIN_I_SJSON)
        if s_json == str():
            self.DEBUG.add_message("No json data set.")
            return

        s_key = self._get_input_value(self.PIN_I_SKEY)
        n_idx = self._get_input_value(self.PIN_I_NIDX)

        if s_key == str() and n_idx < 0:
            self.DEBUG.add_message("No key of index set.")
            return

        val = ""

        self.DEBUG.set_value("Json", str(s_json))
        self.DEBUG.set_value("Index", str(n_idx))
        self.DEBUG.set_value("Key", str(s_key))

        if n_idx >= 0:
            self.DEBUG.add_message("Index requested")
            val = self.get_list_element(s_json, n_idx)
        else:
            self.DEBUG.add_message("Value requested")
            val = self.get_value(s_json, s_key)

        # handle unicode representation
        if isinstance(val, str):
            val = val.replace("u'", '"')
            val = val.replace("'", '"')
            val = val.replace(": False", ': false')
            val = val.replace(": True", ': true')
        else:
            self._set_output_value(self.PIN_O_FVALUE, float(val))

        self._set_output_value(self.PIN_O_SVALUE, str(val))


############################################

class JsonTests(unittest.TestCase):

    def setUp(self):
        self.dummy = JSON_Parser_11087_11087(0)
        self.dummy.on_init()

    def tearDown(self):
        pass

    def test_getValue_str(self):
        in_text = '{"siteCurrentPowerFlow":{"updateRefreshRate":3,"unit":"kW","connections":[{"from":"STORAGE",' \
                  '"to":"Load"},{"from":"GRID","to":"Load"}],"GRID":{"status":"Active","currentPower":0.01},' \
                  '"LOAD":{"status":"Active","currentPower":1.37},"PV":{"status":"Idle","currentPower":0.0},' \
                  '"STORAGE":{"status":"Discharging","currentPower":1.36,"chargeLevel":38,"critical":false}}} '

        ret = self.dummy.get_value(in_text, "siteCurrentPowerFlow")
        res = '{"LOAD": {"status": "Active", "currentPower": 1.37}, "PV": {"status": "Idle", "currentPower": 0.0}, ' \
              '"STORAGE": {"status": "Discharging", "critical": false, "chargeLevel": 38, "currentPower": 1.36}, ' \
              '"connections": [{"to": "Load", "from": "STORAGE"}, {"to": "Load", "from": "GRID"}], "GRID": {"status": ' \
              '"Active", "currentPower": 0.01}, "updateRefreshRate": 3, "unit": "kW"} '
        self.assertEqual(json.loads(ret), json.loads(res))

    def test_getValue_int(self):
        ret = '{"LOAD": {"status": "Active", "currentPower": 1.37}, "PV": {"status": "Idle", "currentPower": 0.0}, ' \
              '"STORAGE": {"status": "Discharging", "critical": false, "chargeLevel": 38, "currentPower": 1.36}, ' \
              '"connections": [{"to": "Load", "from": "STORAGE"}, {"to": "Load", "from": "GRID"}], "GRID": {"status": ' \
              '"Active", "currentPower": 0.01}, "updateRefreshRate": 3, "unit": "kW"} '
        ret = self.dummy.get_value(ret, "updateRefreshRate")
        self.assertEqual(ret, 3)

    def test_index(self):
        ret = '["LOAD", "Active", "PV"]'
        self.dummy.debug_input_value[self.dummy.PIN_I_SJSON] = ret
        self.dummy.debug_input_value[self.dummy.PIN_I_SKEY] = str()
        self.dummy.debug_input_value[self.dummy.PIN_I_NIDX] = 1

        self.dummy.on_input_value(self.dummy.PIN_I_NIDX, 1)

        ret = self.dummy.debug_output_value[self.dummy.PIN_O_SVALUE]
        self.assertEqual(ret, '"Active"')

    def test_key(self):
        ret = '{"LOAD": {"status": "Active", "currentPower": 1.37}, "PV": {"status": "Idle", "currentPower": 0.0}, ' \
              '"STORAGE": {"status": "Discharging", "critical": false, "chargeLevel": 38, "currentPower": 1.36}, ' \
              '"connections": [{"to": "Load", "from": "STORAGE"}, {"to": "Load", "from": "GRID"}], "GRID": {"status": ' \
              '"Active", "currentPower": 0.01}, "updateRefreshRate": 3, "unit": "kW"} '

        self.dummy.debug_input_value[self.dummy.PIN_I_SJSON] = ret
        self.dummy.debug_input_value[self.dummy.PIN_I_SKEY] = "updateRefreshRate"
        self.dummy.debug_input_value[self.dummy.PIN_I_NIDX] = -1

        self.dummy.on_input_value(self.dummy.PIN_I_NIDX, -1)

        ret = self.dummy.debug_output_value[self.dummy.PIN_O_SVALUE]
        self.assertEqual(ret, "3")

        ret = self.dummy.debug_output_value[self.dummy.PIN_O_FVALUE]
        self.assertEqual(ret, 3)

if __name__ == '__main__':
    unittest.main()