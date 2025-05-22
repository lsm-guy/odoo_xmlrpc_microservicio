
from flask import Flask, request, jsonify
import xmlrpc.client

app = Flask(__name__)

@app.route('/odoo/productos', methods=['POST'])
def get_productos():
    data = request.json

    url = data.get("url")
    db = data.get("db")
    login = data.get("login")
    password = data.get("password")

    try:
        common = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/common")
        uid = common.authenticate(db, login, password, {})

        if not uid:
            return jsonify({"error": "Credenciales inválidas"}), 401

        models = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/object")
        result = models.execute_kw(
            db, uid, password,
            'product.template',
            'search_read',
            [[]],
            {'fields': ['name', 'list_price'], 'limit': 50}
        )
        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
