__author__ = 'stone'
#coding=UTF-8
import DbModule
from logHelper import getLogger

class orderTransObj:
    def getTransInfo(self,inOrderId):
        logger = getLogger()
        logger.debug("start getTransInfo")
        return DbModule.getOrderTransInfo(inOrderId)
