#!/usr/bin/python
# coding: utf-8

import logging, time
import logging.handlers
import os

class Logger(object):    

    def __init__(self, name):    
        # the path to store log files
        self.path = "./logs/" 
        if not os.path.exists(self.path):
            os.makedirs(self.path)
        self.filename = self.path + 'ipaddress.log'    
        self.name = name
        self.logger = logging.getLogger(self.name)    
        # the output level of log for console
        self.logger.setLevel(logging.INFO)    
        # the format of log for console
        self.console = logging.StreamHandler()    
        self.console.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(name)s[line:%(lineno)d] - %(message)s'))    
        # generate log file everyday, and the log files will be keep 10 days
        self.logfile = logging.handlers.TimedRotatingFileHandler(self.filename, 'D', 1, 10)
        # the format of log for file
        self.logfile.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s -   %(name)s[line:%(lineno)d] - %(message)s'))
        self.logger.addHandler(self.logfile)
        self.logger.addHandler(self.console) 
    def debug(self,message):
        self.logger.debug(message)

    def info(self,message):
        self.logger.info(message)

    def warn(self,message):
        self.logger.warn(message)

    def error(self,message):
        self.logger.error(message)

    def crit(self,message):
        self.logger.critical(message)

if __name__ =='__main__':
    logyyx = Logger("test")
    logyyx.debug('a debug log')
    logyyx.info('a info log')
    logyyx.war('a warning log')
    logyyx.error('a error log')
    logyyx.cri('a critical log')
