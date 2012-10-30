__author__ = 'stone'
#coding=UTF-8
import DbModule
import traceback
from logHelper import getLogger

class orderInfoObj:
    def compareOrderInfo(self,inOrderInfo):
        try:
            logger = getLogger()
            logger.debug("start compareOrderInfo")
            ret = True

            #exists contact,same name,same phone? 现在电话加密,所以不能比较.
            #ret &= DbModule.NotExitsContact(inOrderInfo)

            #if (ret == False):
            #    return ret

            #exists orderid?
            ret &= DbModule.NotExitsOrderid(inOrderInfo["orderId"])

            if (ret == False):
                return ret

            #exists productid?
            ret &= DbModule.IsExitsProductid(inOrderInfo["orderDet"])

            if (ret == False):
                return ret

            #valid crusr?
            ret &= DbModule.IsValidCrusr(inOrderInfo["crusr"])
            if (ret == False):
                return ret

            #valid order status?
            ret &= DbModule.IsValidOrderStatus(inOrderInfo["orderStatus"])
            if (ret == False):
                return ret

            #valid contact address
            ret &= DbModule.IsValidContactAddress(inOrderInfo)
            if (ret == False):
                return ret

        except :
            logger.error("exception occur, see the traceback.log")
            #异常写入日志文件.
            f = open('traceback.txt','a')
            traceback.print_exc()
            traceback.print_exc(file = f)
            f.flush()
            f.close()
            ret = False
        else:
            pass
        finally:
            return ret

    def saveOrderInfo(self,inOrderInfo):
        try:
            logger = getLogger()
            logger.debug("start saveOrderInfo")
            ret = True
            ret &= self.compareOrderInfo(inOrderInfo)

            #all condition is ok
            if(ret):
                ret = DbModule.saveData2Db(inOrderInfo)

                if (ret):
                    ret = DbModule.saveData2DbSqlite("GWImp"+inOrderInfo["orderId"])
        except :
            logger.error("exception occur, see the traceback.log")
            #异常写入日志文件.
            f = open('traceback.txt','a')
            traceback.print_exc()
            traceback.print_exc(file = f)
            f.flush()
            f.close()
        else:
            pass
        finally:
            pass
            return ret

