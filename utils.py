#!/bin/env python
# coding=utf-8

from datetime import date
from datetime import timedelta


class DateB(object):

    def __init__(self):
        self._date = date.today()

    def to_string(self):
        return self._date

    def moins_jours(self, jours):
        self._date = self._date - timedelta(days=jours)