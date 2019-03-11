#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pyodbc

class DqConnection:
    def setCredentials(self, credentials):
        self._credentials = credentials