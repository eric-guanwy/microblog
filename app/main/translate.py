import json
import requests
import hashlib
from urllib.parse import quote
import random
from flask import current_app
from flask_babel import _

def translate(text, source_language, dest_language):
	
	if 'YOUDAO_TRANSLATOR_KEY' not in current_app.config or not current_app.config['YOUDAO_TRANSLATOR_KEY']:
		return _('Error: the translation service is not configured.')

	httpClient = None
	myurl = '/api'
	salt = random.randint(1, 65536)
	sign = current_app.config['YOUDAO_TRANSLATOR_KEY']+text+str(salt)+current_app.config['YOUDAO_SECRET_KEY']
	m1 = hashlib.md5()
	m1.update(sign.encode('utf-8'))
	sign = m1.hexdigest()
	myurl = myurl+'?appKey='+current_app.config['YOUDAO_TRANSLATOR_KEY']+'&q='+quote(text)+'&from='+source_language+'&to='+dest_language+'&salt='+str(salt)+'&sign='+sign
	 
	r = requests.get('http://openapi.youdao.com'+myurl)
	#print(type(r))
	res = json.loads(r.content.decode('utf-8-sig'))
	#print (type(res))
	#print (res['translation'][0])

	return res['translation'][0]
