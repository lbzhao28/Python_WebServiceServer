__author__ = 'stone'
#coding=UTF-8
import web
import json
import mimerender

import globalDefine
import traceback
from configData import getConfig
from logHelper import getLogger

from orderInfoHandler import orderInfoObj

from orderTransHandler import orderTransObj

import re
import base64

mimerender = mimerender.WebPyMimeRender()

render_xml_order =  lambda ret:'<ret>%s</ret>'%ret
render_json_order = lambda **args:json.dumps(args)
render_html_order = lambda ret:'<html><body>ret is:%s<body></html>'%ret
render_txt_order =  lambda ret:ret

render_xml_trans =  lambda orderid,mailid:'<orderid>%s</orderid><mailid>%s</mailid>'%(orderid,mailid)
render_json_trans = lambda **args:json.dumps(args)
render_html_trans = lambda orderid,mailid:'<html><body>orderid is:%s<br>mailid is:%s</body></html>'%(orderid,mailid)
render_txt_trans =  lambda orderid,mailid:orderid+mailid

urls = (
    "/orderTrans/(.+)","trans",
    "/orderInfo/(.+)","order",
    )
app = web.application(urls,globals())

allowed = (
    (getConfig('allowedUser1','UserName','str'),getConfig('allowedUser1','Password','str')),
    (getConfig('allowedUser2','UserName','str'),getConfig('allowedUser2','Password','str'))
    )

class trans:
    @mimerender(
        default = 'json',
        html = render_html_trans,
        xml  = render_xml_trans,
        json = render_json_trans,
        txt  = render_txt_trans
    )
    def GET(self,orderid):
        try:
            logger = getLogger()
            logger.debug("start Trans GET response")

            globalDefine.globalOrderInfoErrorlog = "No Error"

            auth = web.ctx.env.get('HTTP_AUTHORIZATION')
            authreq = False
            if auth is None:
                authreq = True
            else:
                auth = re.sub('^Basic ','',auth)
                username,password = base64.decodestring(auth).split(':')
                if (username,password) in allowed:
                    logger.debug("has right HTTP_AUTHORIZATION")
                    pass
                else:
                    authreq = True
            if authreq:
                web.header('WWW-Authenticate','Basic realm="Auth example"')
                web.ctx.status = '401 Unauthorized'
                logger.debug("no right HTTP_AUTHORIZATION")
                #TODO:why only two para?
                return {'orderid':'','mailid':'','companytitle':''}

            if not orderid:
                orderid = 'no orderid'
                mailid = 'no mailid'
                companytitle = 'no companytitle'
            else:
                OTO = orderTransObj()
                transInfo = OTO.getTransInfo(orderid)
                mailid = transInfo['mailid']
                companytitle = transInfo['companytitle']
                utf8companytitle = unicode(companytitle,"cp936")
            return {'orderid':orderid,'mailid':mailid,'companytitle':utf8companytitle,'error info':globalDefine.globalOrderTransErrorlog}

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

class order:
    @mimerender(
        default = 'json',
        html = render_html_order,
        xml  = render_xml_order,
        json = render_json_order,
        txt  = render_txt_order
    )

    def GET(self,orderid):
        try:
            logger = getLogger()
            logger.debug("start Order GET response")

            globalDefine.globalOrderInfoErrorlog = "No Error"

            if not orderid:
                orderid = 'no orderid'

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
            return {'orderid':orderid}

    def POST(self, orderid):
        try:
            logger = getLogger()
            logger.debug("start Order POST response")

            globalDefine.globalOrderInfoErrorlog = "No Error"

            data = web.data()
            #result = urlparse.parse_qs(data)
            #uid = result['child1'][0]
            #add_count = 0
            #list = json.loads(result['child2'][0])
            #for u in list:
                #add_count += self.add_orderInfo(orderid , u[0])
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
            return orderid

    def PUT(self, orderid):
        try:
            logger = getLogger()
            logger.debug("start Order PUT response")

            globalDefine.globalOrderInfoErrorlog = "No Error"

            ret = False

            auth = web.ctx.env.get('HTTP_AUTHORIZATION')
            authreq = False
            if auth is None:
                authreq = True
            else:
                auth = re.sub('^Basic ','',auth)
                username,password = base64.decodestring(auth).split(':')
                if (username,password) in allowed:
                    logger.debug("has right HTTP_AUTHORIZATION")
                    pass
                else:
                    authreq = True
            if authreq:
                web.header('WWW-Authenticate','Basic realm="Auth example"')
                web.ctx.status = '401 Unauthorized'
                logger.debug("no right HTTP_AUTHORIZATION")
                #TODO:why only one para?
                return {'orderid':''}

            #get PUT body data.
            data = web.data()

            #get the data from json.
            localOrderInfos = json.loads(data)

            #for each data, save the Json orderInfo to Dict:orderhist,orderdet,contact,only one record.
            for localOrderInfo in localOrderInfos:
                updateDict = {'orderId':orderid}
                localOrderInfo.update(updateDict)

                OIO = orderInfoObj()
                ret = OIO.saveOrderInfo(localOrderInfo)

                #one record return.
                return {'orderid':orderid,'return value':ret,'error info':globalDefine.globalOrderInfoErrorlog}

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

if __name__ == "__main__":
    app.run()
