#!/usr/bin/python
# codig:utf-8

from log import Logger
from mysql import MySQL
from bs4 import BeautifulSoup
import uuid
import sys

default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)

class Tables:
    """Create or Drop tables,delete data from tables
    """
    def __init__(self):
        self._logger = Logger(__file__)
        try:
            fsock = open("sqls.xml", "r")
        except IOError:
            self._logger.error("The file don't exist, Please double check!")
        self.sqls = BeautifulSoup(fsock.read())
        dbconfig = {'host':'127.0.0.1', 
                'port': 3306, 
                'user':'root', 
                'passwd':'123456', 
                'db':'scenic', 
                'charset':'utf8'}
        self.db = MySQL(dbconfig)

    def initDB(self):
        """create all tables
        """
        createSqls = self.sqls.find(id="createSql")
        for item in createSqls.select("item"):
            sql = item.string
            self._logger.info("create the table "+item.attrs["id"])
            self.db.execute(sql)
        # must reopen the cursor, or it will raise exception with error code 1024. What a fucking error
        self.db.reopenCursor()

    def createTable(self,name):
        """create a specified table
        """
        create = self.sqls.find(id="createSql").find(id=name).string
        if create:
            self._logger.info(" create table "+name)
            self.db.execute(create)
        else:
            self._logger.error("error occured when create table "+name)
        
    def dropAll(self):
        """drop all the tables
        """
        dropSqls= self.sqls.find(id="dropSql")
        for item in dropSqls.select("item"):
            sql = item.string
            self._logger.info("drop the table "+item.attrs["id"])
            self.db.execute(sql)

    def dropTable(self,name):
        """drop specified table
        """
        drop = self.sqls.find(id="dropSql").find(name)
        if drop:
            self._logger.info("drop the table "+name)
            self.db.execute(sql)
        else:
            self._logger.warn("Don't have the table "+name)

    def cleanAll(self):
        """delete data from all the tables,but not drop tables
        """
        cleanSqls= self.sqls.find(id="cleanSql")
        for item in cleanSqls.select("item"):
            sql = item.string
            self._logger.info("clean the table "+item.attrs["id"])
            self.db.execute(sql)

    def cleanTable(self,name):
        """clean the data of specified table
        """
        pass

    def insertTable(self,name,params):
        """insert values int to the specified table
        # Parameters:
        name: the name of the table
        params: the value insert into the tables. It can be tuple for inserting a row,or can be a list to insert serveral rows
        # Return:
        """
        insert = self.sqls.find(id="insertSql").find(id=name).string
        if insert:
            self._logger.info(" insert into table "+name)
            self.db.insert(insert,params)
        else:
            self._logger.error("did not find the table "+name+" when insert")

if __name__ == "__main__":
    tables = Tables()
    tables.dropAll()    
    tables.initDB()
