#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json


class Credentials():
    def __init__(self):
        try:
            self.index = -1
            with open('credentials.json', encoding='UTF-8') as file:
                self.data = json.load(file)
                self.cred_len = len(self.data['credentials'])
        except Exception as e:
            print("Credentials JSON file could not be found!")
            raise e

    def next_credentials(self):
        self.index = (self.index + 1) % self.cred_len
        return self.data['credentials'][self.index]
