#!/usr/bin/env python
# -*- coding: utf-8 -*-

from config import *
from datetime import datetime
import uuid


class LogFile(object):
    def __init__(self):
        self._log = open(os.path.join(Statics().log, 'process_error_%s.log' % uuid.uuid4().__str__()), 'w')

    def log_write_row(self, *args):
        message = '%s | [%s] | %s\n' % (args[0], datetime.now().__str__(), args[1])
        self._log.write(message)

    def log_save(self):
        self._log.close()
