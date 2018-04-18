from app.device import device 

from flask import jsonify
import json
from app.models import mySqlDB

select_all_devices = '''
SELECT * FROM lily_device
'''

@device.route('/devices', methods=['GET'])
def get_devices():
	cursor = mySqlDB.select_command(select_all_devices)
	result = cursor.fetchone()
	return jsonify(result)