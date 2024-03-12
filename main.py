from flask import Flask, request, jsonify, render_template, url_for
from flask_compress import Compress
from dotenv import load_dotenv
load_dotenv()
from routes import rotas

app = Flask(__name__)
compress = Compress(app)
app.config['JSON_AS_ASCII'] = False

# Register the routes
app.register_blueprint(rotas.bp)
@app.route('/rotas')
def get_rotas():
    route_data = []
    for rule in app.url_map.iter_rules():
        if rule.endpoint != 'static':
            methods = ','.join(rule.methods)
            url = url_for(rule.endpoint)
            doc = app.view_functions[rule.endpoint].__doc__
            route_data.append((url, methods, doc))
    return render_template('routes.html', route_data=route_data)

@app.route('/')
def get_landpage():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
