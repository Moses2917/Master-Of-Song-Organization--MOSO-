from waitress import serve
import app
serve(app,host='192.168.1.160', port=5000)