__author__ = 'stone'
# -*- coding: utf-8 -*-
import json

s = '[{"name":"鸟巢","point":{"lat":"39.990","lng":"116.397"},"desc":"奥运会主场地"},{"name":"北大乒乓球馆","point":{"lat":"39.988","lng":"116.315"},"desc":"乒乓球比赛场地"},{"name":"北京工人体育场","point":{"lat":"39.930","lng":"116.446"},"desc":"足球比赛场地"}]'

locations = json.loads(s)
print str(len(locations))
for location in locations:
    print location["name"]
    print location["point"]["lat"]