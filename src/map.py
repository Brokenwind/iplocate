#!/usr/bin/python
# coding: utf-8

__author__ = "Brokenwind"

import numpy
import re
import sys
import os
import urllib2
import json
from IPy import IP
from tables import Tables
from decimal import *
from log import Logger

# set global charset
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)

class BaiduMap:
    def __init__(self):
        self._logger = Logger(__file__)
        self.headers = {}
        self.headers["User-Agent"]="Mozilla/5.0 (X11; Linux x86_64; rv:45.0) Gecko/20100101 Firefox/45.0"

    def access(self,url):
        """get Json object from specified url
        """
        try:
            req = urllib2.Request(url,headers=self.headers)
            response = urllib2.urlopen(req)
            return json.loads(response.read())
        except Exception,e:
            self._logger.error("error occured when get geo data")
            return None

    def ipLocation(self,ip,ak):
        url = "http://api.map.baidu.com/location/ip?ip="+ip+"&ak="+ak+"&coor=bd09ll "
        data = self.access(url)
        if not data:
           return None
        if "status" in data.keys():
            state = data["status"]
            if state == 0:
                return data
            elif state == 1:
                self._logger.warn("did not got the address of ip: "+ip)
                return None
            elif state > 1:
                self._logger.error("can not still access the service. status code: "+str(state))
                #os._exit(0)
                return None

    def getAllIpAddress(self):
        table = Tables()
        table.createTable("ipAddress")
        iplines = []
        try:
            ipfile = open("chinaiplist.txt")
            iplines = ipfile.readlines()
        except Exception,e:
            self._logger.error("error occured when open file")
            return None
        
        # get iprecord from file
        linenum = 0
        ipindex = 0
        iprecord = open("iprecord.txt","a+")
        content = iprecord.readlines()
        if len(content) != 0:
            line = content[len(content)-1]
            strs = line.split(" ")
            linenum = int(strs[0])
            ipindex = int(strs[1])

        for i in range(linenum,len(iplines)):
            ips = IP(iplines[i])
            if ips:
                for j in range(ipindex,len(ips)):
                    ip = ips[j]
                    data = search.ipLocation(str(ip),"sh0wDYRg1LnB5OYTefZcuHu3zwuoFeOy")
                    if data:
                        try:
                            if "address" in data.keys() and  "content" in data.keys():
                                detail = data["content"]["address_detail"]
                                point = data["content"]["point"]
                                params = (str(ip),data["address"],detail["province"],detail["city"],detail["district"],detail["street"],detail["street_number"],point["x"],point["y"])
                                table.insertTable("ipAddress",params)
                                iprecord.write(str(i)+" "+str(j)+"\n")
                            else:
                                self._logger.warn("did not get result of ip:"+ip)
                        except Exception,e:
                            self._logger.error("error occured when extract information from json object")
                            continue
            else:
                self._logger.warn("no ip got from ip segment: "+iplines[i])

if __name__ == "__main__":
    search = BaiduMap()
    search.getAllIpAddress()

