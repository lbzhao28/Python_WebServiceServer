__author__ = 'stone'
#coding=UTF-8
import web
import globalDefine
import traceback
from configData import getConfig
from logHelper import getLogger

def IsValidCrusr(inCrusr):
    ret = True
    try:
        logger = getLogger()
        logger.debug("start IsValidCrusr")

        if (inCrusr != 'taobao')&(inCrusr != 'guanwang'):
            ret = False
            globalDefine.globalOrderInfoErrorlog="crusr should be taobao or guanwang"

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


def IsValidOrderStatus(inOrderStatus):
    ret = True
    try:
        logger = getLogger()
        logger.debug("start IsValidOrderStatus")

        if (inOrderStatus != 'yifu')&(inOrderStatus != 'weifu'):
            ret = False
            globalDefine.globalOrderInfoErrorlog="orderstatus should be yifu or weifu"

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

def DbConnect():
    db = web.database(dbn=getConfig('db','dbname','str'),db=getConfig('db','dbservice','str'),user=getConfig('db','dbuser','str'),pw=getConfig('db','dbpwd','str'))
    return db

def DbSqliteConnect():
    db = web.database(dbn=getConfig('dbSqlite','dbname','str'),db=getConfig('dbSqlite','dbfile','str'))
    return db

def IsValidContactAddress(inOrderInfo):
    ret = True
    try:
        logger = getLogger()
        logger.debug("start IsValidContactAddress")

        dbI8 = DbConnect()

        #according the contact province,city,district to get the snapid.

        #get provinceid from dic_sys_province
        myvar = dict(chinese=inOrderInfo["contactProvince"])
        entries = dbI8.select('i8.dic_sys_province',myvar,what="provinceid",where="chinese=$chinese")
        localProvinceId = entries[0].PROVINCEID

        updateDict = {'orderProvinceId':localProvinceId}
        inOrderInfo.update(updateDict)

        logger.debug("localProvinceID is :"+localProvinceId )

        #get cityid from dic_sys_city
        myvar = dict(chinese=inOrderInfo["contactCity"])
        entries = dbI8.select('i8.dic_sys_city',myvar,what="cityid",where="chinese=$chinese")
        localCityId = entries[0].CITYID

        updateDict = {'orderCityId':localCityId}
        inOrderInfo.update(updateDict)

        logger.debug("localCityId is :"+localCityId )

        #get addressid from dic_sys_ems
        myvar = dict(name=inOrderInfo["contactDistrict"],provinceid=localProvinceId,city=localCityId)
        entries = dbI8.select('i8.dic_sys_ems',myvar,what="spellid",where="name=$name and provinceid=$provinceid and city=$city")
        localSpellId = entries[0].SPELLID
        logger.debug("localSpellId is :"+localSpellId )

        updateDict = {'orderSpellId':localSpellId}
        inOrderInfo.update(updateDict)

    except :
        logger.error("exception occur, see the traceback.log")
        #异常写入日志文件.
        f = open('traceback.txt','a')
        traceback.print_exc()
        traceback.print_exc(file = f)
        f.flush()
        f.close()
        ret = False
        globalDefine.globalOrderInfoErrorlog="contact province,contact city,contact district can not be finded in I8 system"
    else:
        pass
    finally:
        pass
        return ret

def NotExitsContact(inOrderInfo):
    ret = True
    try:
        logger = getLogger()
        logger.debug("start NotExitsContact")
        dbI8 = DbConnect()

        hasName = False
        hasPhone = False

        myvar = dict(name=inOrderInfo['contactName'])
        entries = dbI8.select('i8.con_contact',myvar,what='contactid',where="name=$name")

        #exits contact name .
        for val in entries:
            hasName = True

        myvar = dict(phone=inOrderInfo['contactMobilePhone'])
        entries = dbI8.select('i8.con_phone',myvar,what='contactid',where="phone=$phone")


        #exits contact phone .
        for val in entries:
            hasPhone = True

        if (hasName & hasPhone):
            globalDefine.globalOrderInfoErrorlog="same contact name and mobile phone existed"
            return ret
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

def NotExitsOrderid(inOrderid):
    ret = True
    try:
        logger = getLogger()
        logger.debug("start NotExitsOrderid")
        dbI8 = DbConnect()
        myvar = dict(orderid="GWImp"+inOrderid)
        #entries = dbI8.select('con_orderhist',myvar,where="orderid=$orderid",_test=True)
        entries = dbI8.select('i8.con_orderhist',myvar,where="orderid=$orderid")

        #exits order id.
        for val in entries:
            ret = False
            globalDefine.globalOrderInfoErrorlog="orderid existed"
            return ret
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

def IsExitsProductid(inOrderDet):
    ret = False
    try:
        logger = getLogger()
        logger.debug("start IsExitsProductid")
        dbI8 = DbConnect()

        for localOrderDet in inOrderDet:
            myvar = dict(prodid=localOrderDet["orderProductId"])
            entries = dbI8.select('i8.dic_sys_product',myvar,where="prodid=$prodid")

            ret = False
            #exits order id.
            for val in entries:
                ret = True

            if (ret == False):
                globalDefine.globalOrderInfoErrorlog = "prodid not existed"
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

def getOrderTransInfo(inOrderid):
    try:
        logger = getLogger()
        logger.debug("start getOrderTransInfo")
        mailid = ""
        companytitle = ""
        dbI8 = DbConnect()
        myvar = dict(orderid="GWImp"+inOrderid)
        entries = dbI8.select('i8.con_orderhist',myvar,what='mailid',where="orderid=$orderid")

        globalDefine.globalOrderTransErrorlog = "mailid does not existed"
        for val in entries:
            mailid = val.MAILID
            #TODO:confirm this judge.
            if (mailid != None):
                #get companytitile
                entries = dbI8.query('select cp.name from i8.con_orderhist o,i8.dic_sys_company cp where o.entityid is not null and o.entityid = cp.companyid and o.orderid = $inOrderid ',vars={'inOrderid':"GWImp"+inOrderid})
                for val in entries:
                    companytitle = val.NAME
                    globalDefine.globalOrderTransErrorlog = "got mailid and companytitile"
                    return {'mailid':mailid,'companytitle':companytitle}

                globalDefine.globalOrderTransErrorlog = "company title does not existed"

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
        return {'mailid':mailid,'companytitle':companytitle}

def saveData2DbSqlite(inOrderId):
    try:
        logger = getLogger()
        logger.debug("start saveData2DbSqlite")
        ret = True
        t = None
        dbSqlite = DbSqliteConnect()
        t = dbSqlite.transaction()

        dbSqlite.insert('orderHist',orderid=inOrderId)
        logger.debug("saveData2DbSqlite success.")
    except :
        logger.debug("saveData2DbSqlite go into excption.")
        logger.error("exception occur, see the traceback.log")
        #异常写入日志文件.
        f = open('traceback.txt','a')
        traceback.print_exc()
        traceback.print_exc(file = f)
        f.flush()
        f.close()
        ret = False
        t.rollback()
    else:
        t.commit()
        pass
    finally:
        pass
        return ret

def saveData2Db(inOrderInfo):
    try:
        logger = getLogger()
        logger.debug("start saveData2Db")
        ret = True
        t = None
        dbI8 = DbConnect()
        t = dbI8.transaction()

        #get sequence for con_contactId
        entries = dbI8.query('select i8.seq_con_contact.nextval from dual')
        localContactId = entries[0].NEXTVAL

        #get sysdate from oracle server
        entries = dbI8.query('select sysdate from dual')
        localCrdt = entries[0].SYSDATE

        dbI8.insert('i8.con_contact',contactid=localContactId,name=inOrderInfo["contactName"],crdt=localCrdt,crusr=inOrderInfo["crusr"],point=0,ticket=0,coupon=0)

        #get sequence for con_address
        entries = dbI8.query('select i8.seq_con_address.nextval from dual')
        localAddressId = entries[0].NEXTVAL

        dbI8.insert('i8.con_address',addressid=localAddressId,contactid=localContactId,nation='china',province=inOrderInfo["orderProvinceId"],city=inOrderInfo["orderCityId"],district=inOrderInfo["orderSpellId"],spellid=inOrderInfo["orderSpellId"],address = inOrderInfo["contactAddr"],prmadd='Y',addrtypeid='1',zip=inOrderInfo['contactPostCode'],crdt=localCrdt,crusr=inOrderInfo["crusr"])

        #get sequence for con_phone
        entries = dbI8.query('select i8.seq_con_phone.nextval from dual')
        localPhoneId = entries[0].NEXTVAL

        dbI8.insert('i8.con_phone',phoneid=localPhoneId,contactid=localContactId,phone=inOrderInfo["contactMobilePhone"],phonetypeid='1',prmphn='Y',crdt=localCrdt,crusr=inOrderInfo["crusr"])

        if (inOrderInfo["contactFixPhone"] != ''):
            #get sequence for con_phone
            entries = dbI8.query('select i8.seq_con_phone.nextval from dual')
            localPhoneId = entries[0].NEXTVAL
            dbI8.insert('i8.con_phone',phoneid=localPhoneId,contactid=localContactId,phone=inOrderInfo["contactFixPhone"],phonetypeid='2',prmphn='N',crdt=localCrdt,crusr=inOrderInfo["crusr"])

        localOrderId ="GWImp"+inOrderInfo["orderId"]

        if(inOrderInfo["orderStatus"] == 'yifu'):
            localStatus = getConfig("orderInfo","orderstatus_yifu","str")
            localOrderDetStatus = getConfig("orderDet","status_yifu","str")
        else:
            localStatus = getConfig("orderInfo","orderstatus_weifu","str")
            localOrderDetStatus = getConfig("orderDet","status_weifu","str")

        dbI8.insert('i8.con_orderhist',orderid=localOrderId,contactid=localContactId,addressid=localAddressId,paytype=getConfig("orderInfo","paytype","str"),mailtype=getConfig("orderInfo","mailtype","str"),ordertype=getConfig("orderInfo","ordertype","str"),crdt=localCrdt,crusr=inOrderInfo["crusr"],grpid='',status=localStatus,mailprice=inOrderInfo["mailPrice"],prodprice=100,discount=0,totalprice=inOrderInfo["orderPrice"],pointuse=0,couponuse=0,couponget=0,nowmoney=100,consignee=inOrderInfo["contactName"],consignphn=inOrderInfo["contactMobilePhone"])

        for localOrderDet in inOrderInfo["orderDet"]:
            #get sequence for con_orderdet
            entries = dbI8.query('select i8.seq_con_orderdet.nextval from dual')
            localOrderDetId = entries[0].NEXTVAL

            #get uprice,snapid from dic_sys_product
            myvar = dict(prodid=localOrderDet["orderProductId"])
            entries = dbI8.select('i8.dic_sys_product',myvar,what="snapid",where="prodid=$prodid")
            localProdSnapId = entries[0].SNAPID

            myvar = dict(prodid=localOrderDet["orderProductId"])
            entries = dbI8.select('i8.dic_sys_product',myvar,what="unitprice",where="prodid=$prodid")
            localProdUnitPrice = entries[0].UNITPRICE

            localDiscout = (float)(localProdUnitPrice) - (float)(localOrderDet["orderProductSalePrice"])

            dbI8.insert('i8.con_orderdet',orderdetid=localOrderDetId,orderid=localOrderId,contactid=localContactId,prodid=localOrderDet["orderProductId"],soldwith=getConfig("orderDet","soldwith","str"),status=localOrderDetStatus,uprice = localProdUnitPrice,prodnum=localOrderDet["orderProductNum"],payment=localOrderDet["orderProductSalePrice"],crdt=localCrdt,snapid=localProdSnapId,discount=localDiscout,pointget=0)

    except :
        t.rollback()
        logger.error("exception occur, see the traceback.log")
        #异常写入日志文件.
        f = open('traceback.txt','a')
        traceback.print_exc()
        traceback.print_exc(file = f)
        f.flush()
        f.close()
        ret = False
    else:
        t.commit()
        globalDefine.globalOrderInfoErrorlog = "operation success"
        pass
    finally:
        pass
        return ret
