from flask import Flask, request
from flask_restful import Resource, Api
from pyzabbix import ZabbixMetric, ZabbixSender
from gevent.pywsgi import WSGIServer

ZBX_ADDRESS = 'YOUR_ZABBIX_ADDRESS'
ZBX_HOST = 'YOUR_ZABBIX_HOST'
API_PORT = 5000

app = Flask(__name__)
api = Api(app)
http_server = WSGIServer(('0.0.0.0', API_PORT), app)

class PushZabbix(Resource):
  def post(self, job_key):
    failed_hosts = []

    try:
      for hostname in request.json['hosts']:
        if request.json['hosts'][hostname]['failed']:
          failed_hosts.append(hostname)

      job_id = request.json['id']
      job_name = request.json['name']
      job_status = request.json['status'].upper()
      failed_hosts = ", ".join(failed_hosts)

      result = f"AWX: {job_id} - {job_name}: {job_status} ({failed_hosts})"
      metrics = [ ZabbixMetric(ZBX_HOST, job_key, result) ]

      ZabbixSender('ZBX_ADDRESS').send(metrics)
      return 200
    except Exception as e:
      print(e)

api.add_resource(PushZabbix, '/push/<job_key>')

if __name__ == '__main__':
  print(f'SERVER IS LISTENING ON PORT {API_PORT}')
  http_server.serve_forever()