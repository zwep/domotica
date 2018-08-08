# encoding: utf-8

"""
The Toon module impersonates the Eneco Toon mobile app, and implements
similar functionality.
Most part of the code is not written by me, but by:
Robert van der Meulen: https://github.com/rvdm
"""

import os
import re
import json
import sys
import uuid
import pprint
import requests
import time


class Toon:
    """ Log in to the Toon API, and do stuff. """
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.toonstate = None
        self.sessiondata = None
        self.debug = 0
        self.max_retries = 3
        self.retry_interval = 1
        self.required_datakeys = [ 'deviceStatusInfo', 'gasUsage', 'powerUsage', 'thermostatInfo' ]
        self.toon_url = "https://toonopafstand.eneco.nl/toonMobileBackendWeb/client"

    def login(self):
        """
        Log in to the toon API, and set up a session.

        First we open the login page, to get the agreement
        details.
        Agreement details and user details are stored in the
        sessiondata variable.

        :return:
        """

        formdata = {"username": self.username, "password": self.password}
        r = requests.get(os.path.join(self.toon_url, 'login'), params=formdata)
        self.sessiondata = r.json()

    def logout(self):
        """
        Log out of the API.
        This is needed, as toon keeps a maximum amount of display clients.
        Too many logins lead to 500 responses from the API.
        :return:
        """
        client_id = self.sessiondata["clientId"]
        client_checksum = self.sessiondata["clientIdChecksum"]
        formdata = {"clientId": client_id, "clientIdChecksum": client_checksum, "random": uuid.uuid4()}
        r = requests.get(os.path.join(self.toon_url, "auth/logout"), params=formdata)
        self.toonstate = None
        self.sessiondata = None

    def set_maxretries(self,max_retries):
        """
         Set maximum of retries (default: 3).
        :param max_retries:
        :return:
        """
        self.max_retries = max_retries

    def retrieve_toon_state(self):
        self.refresh_toon_state()
        client_id = self.sessiondata["clientId"]
        client_checksum = self.sessiondata["clientIdChecksum"]
        formdata = {"clientId": client_id, "clientIdChecksum": client_checksum, "random": uuid.uuid4()}

        self.toonstate = {}
        retries = 0
        while not all(x in self.toonstate for x in self.required_datakeys):
            retries += 1
            if retries > self.max_retries:
                raise Exception('Incomplete response')
            elif retries > 1:
                time.sleep(self.retry_interval)

        r = requests.get(os.path.join(self.toon_url, "auth/retrieveToonState"), params=formdata)

        if r.status_code == 200:
            self.toonstate = r.json()
            return
        else:
            self.logout()
            raise Exception("retrieve status: ", r.status_code)

    def refresh_toon_state(self):
        # refreshing the session helps with the keep-alive.

        # Now re-use the agreement details to do the actual
        # authentication. This establishes a session, and allows
        # state to be retrieved.
        # TODO: check for variable existence / throw exception on
        # failure
        client_id = self.sessiondata["clientId"]
        client_checksum = self.sessiondata["clientIdChecksum"]
        agreement_id = self.sessiondata["agreements"][0]["agreementId"]
        agreement_checksum = self.sessiondata["agreements"][0]["agreementIdChecksum"]

        formdata = {"clientId": client_id, "clientIdChecksum": client_checksum,
                    "agreementId": agreement_checksum, "agreementIdChecksum": agreement_checksum,
                    "random": uuid.uuid4()}

        r = requests.get(os.path.join(self.toon_url, "auth/start"), params=formdata)
        if r.status_code == 200:
            return
        else:
            self.logout()
            raise Exception("refresh status: ", r.status_code)

    def get_gas_usage(self):
        self.retrieve_toon_state()
        return self.toonstate["gasUsage"]

    def get_power_usage(self):
        self.retrieve_toon_state()
        return self.toonstate["powerUsage"]

    def get_thermostat_info(self):
        self.retrieve_toon_state()
        return self.toonstate["thermostatInfo"]

    def get_thermostat_states(self):
        self.retrieve_toon_state()
        return self.toonstate["thermostatStates"]

    def set_thermostat(self, temperature):
        targettemp = int(temperature*100)
        client_id = self.sessiondata["clientId"]
        client_checksum = self.sessiondata["clientIdChecksum"]
        formdata = {"clientId": client_id, "clientIdChecksum": client_checksum,
                    "random": uuid.uuid4(), "value": targettemp}

        r = requests.get(os.path.join(self.toon_url, "auth/setPoint"), params=formdata)

    def get_program_state(self):
        self.retrieve_toon_state()
        return self.toonstate["thermostatInfo"]["activeState"]

    def set_program_state(self, targetstate):
        client_id = self.sessiondata["clientId"]
        client_checksum = self.sessiondata["clientIdChecksum"]
        formdata = {"clientId": client_id, "clientIdChecksum": client_checksum,
                    "random": uuid.uuid4(), "state": 2,
                    "temperatureState": targetstate}

        r = requests.get(os.path.join(self.toon_url, "auth/schemeState"), params=formdata)

