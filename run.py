# coding:utf-8
from app import app
from app.user import user
from app.device import device

app.register_blueprint(user, url_prefix='/user')
app.register_blueprint(device, url_prefix='/device')

if __name__=='__main__':
	app.run()