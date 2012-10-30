#coding=UTF-8
import globalDefine
import logging
import logging.config
import traceback

logging.config.fileConfig("logging.conf")

#根据配置文件取到logger实例。
def getLogger():
	try:
		if globalDefine.globalLogger is None:
			#create logger
			globalDefine.globalLogger = logging.getLogger("root")
		else:
			pass
	except:
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
	return globalDefine.globalLogger
