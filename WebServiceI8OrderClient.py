__author__ = 'stone'
#coding=UTF-8

import pycurl
import cStringIO
import os
import time

import httplib2
import json
import urllib

buf = cStringIO.StringIO()

def getOrderTrans():
    try:
        c = pycurl.Curl()
        c.setopt(pycurl.URL,'http://180.169.94.232:8080/orderTrans/12345')
        #c.setopt(pycurl.URL,'http://localhost:8080/orderTrans/1234567')
        c.setopt(c.WRITEFUNCTION,buf.write)
        c.setopt(c.VERBOSE, True)
        c.setopt(pycurl.USERPWD,'jery:jery123')
        c.perform()

        print buf.getvalue()
        buf.close()
    except pycurl.error, error:
        errno, errstr = error
        print 'An error occurred: ', errstr

def putOrderInfoNoFile():
    try:
        btime = time.time()

        #s = '[{"orderDet":[{"orderProductId":"testprid002","orderProductNum":"5","orderProductSalePrice":"68"},{"orderProductId":"testprid003","orderProductNum":"2","orderProductSalePrice":"58"}],"contactName":"海工","contactMobilePhone":"13817541163","contactFixPhone":"","contactAddr":"丰镇路14号A楼1101室","contactPostCode":"200434","contactProvince":"上海市","contactCity":"上海市","contactDistrict":"虹口区","crusr":"taobao","orderStatus":"yifu","orderPrice":"485","mailPrice":"29"}]'
        s = '[{"orderDet":[{"orderProductId":"C.CBA.038.01","orderProductNum":"5","orderProductSalePrice":"68"},{"orderProductId":"C.CB.601.04","orderProductNum":"2","orderProductSalePrice":"58"}],"contactName":"海工","contactMobilePhone":"13817541163","contactFixPhone":"","contactAddr":"丰镇路14号A楼1101室","contactPostCode":"200434","contactProvince":"上海市","contactCity":"上海市","contactDistrict":"虹口区","crusr":"taobao","orderStatus":"yifu","orderPrice":"485","mailPrice":"29"}]'

        localOrderInfo = s

        c = pycurl.Curl()
        c.setopt(pycurl.URL,'http://180.169.94.232:8080/orderInfo/20120929001')
        #c.setopt(pycurl.URL,'http://localhost:8080/orderInfo/623456')
        c.setopt(pycurl.HTTPHEADER,['Content-Type: application/json','Content-Length: '+str(len(localOrderInfo))])
        c.setopt(c.VERBOSE, True)
        c.setopt(pycurl.CUSTOMREQUEST,"PUT")
        c.setopt(pycurl.POSTFIELDS,localOrderInfo)
        c.setopt(c.WRITEFUNCTION,buf.write)
        c.setopt(pycurl.USERPWD,'jery:jery123')
        print "after ready curl : %f " % ((time.time() - btime),)
        c.perform()
        c.close()
        print "after do curl : %f " % ((time.time() - btime),)

        print buf.getvalue()
        buf.close()
    except pycurl.error, error:
        errno, errstr = error
        print 'An error occurred: ', errstr

def putOrderInfo():
    try:
        btime = time.time()
        filename = 'd:/I8WebServiceJson.json'
        filesize = os.path.getsize(filename)
        f = file(filename, 'rb')
        c = pycurl.Curl()
        c.setopt(pycurl.URL,'http://localhost:8080/orderInfo/12345')
        c.setopt(pycurl.PUT,1)
        c.setopt(pycurl.INFILE,f)
        c.setopt(pycurl.INFILESIZE,filesize)
        c.setopt(c.WRITEFUNCTION,buf.write)
        c.setopt(c.VERBOSE, True)
        c.setopt(pycurl.USERPWD,'jery:jery123')
        print "after ready curl : %f " % ((time.time() - btime),)
        c.perform()
        c.close()
        f.close()
        print "after do curl : %f " % ((time.time() - btime),)

        print buf.getvalue()
        buf.close()
    except pycurl.error, error:
        errno, errstr = error
        print 'An error occurred: ', errstr

def putOrderInfoHttplib2():
    h = httplib2.Http(".cache")
    h.add_credentials('jery','jery123')
    resp,content = h.request("http://localhost:8080/orderInfo/6123456","PUT",body="This is test")

if __name__ == "__main__":
    getOrderTrans()
    #putOrderInfo()
    #putOrderInfoNoFile()
    #putOrderInfoHttplib2()

