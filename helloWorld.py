import web

urls = ("/.*","hello")
app = web.application(urls,globals())

class hello:
	def GET(self):
		return 'Hello, tutu & lulu!'

if __name__ == "__main__":
	app.run()
