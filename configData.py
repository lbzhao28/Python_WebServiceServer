#coding=UTF-8
import ConfigParser
import traceback

#get the config from config.conf file.
#[system]
#UsrID = "FJ"
#UsrPwd = "FJ123"
#freqTime = 1
#system is section
#UsrID is item
#if get UsrID, the type is str
#if get freqTime,the type is int.
#str->stirng,int->int.
def getConfig(section,item,type):
	try:
		cf = ConfigParser.ConfigParser()
		cf.read("config.conf")

		if (type == "str"):
			o = cf.get(section,item)
			return str(o)
		else:
			if (type == "int"): 
				o = cf.getint(section,item)
				return int(o)
			else:
				pass
	except:
		#异常写入日志文件.
		f = open('traceback.txt','a')
		traceback.print_exc()
		traceback.print_exc(file = f)
		f.flush()
		f.close()
	finally:
		pass