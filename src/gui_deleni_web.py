#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Web GUI pro výpočty dělicí hlavy
"""

from flask import Flask, render_template, request, jsonify
from deleni import DeliciHlava

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('deleni.html')

@app.route('/api/pocty', methods=['POST'])
def vypocitat_pocty():
    data = request.json
    ratio = int(data.get('ratio', 40))
    ratio_table = int(data.get('ratio_table', 120))
    pocet_der = int(data.get('pocet_der'))
    
    hlava = DeliciHlava(ratio, ratio_table)
    deleni = hlava.prozkoumej_deleni(pocet_der)
    max_deleni = pocet_der * ratio
    
    return jsonify({
        'pocet_der': pocet_der,
        'max_deleni': max_deleni,
        'deleni': list(deleni),
        'celkem': len(deleni)
    })

@app.route('/api/deleni', methods=['POST'])
def vypocitat_deleni():
    data = request.json
    ratio = int(data.get('ratio', 40))
    ratio_table = int(data.get('ratio_table', 120))
    deleni = int(data.get('deleni'))
    
    hlava = DeliciHlava(ratio, ratio_table)
    pocet_der = hlava.vypocti_pocet_der(deleni)
    
    result = {
        'deleni': deleni,
        'ratio': ratio,
        'ratio_table': ratio_table,
        'pocet_der': pocet_der,
        'success': pocet_der > 0
    }
    
    if pocet_der > 0:
        result['nasobky'] = [pocet_der * i for i in range(1, 6)]
    
    return jsonify(result)

@app.route('/api/options')
def get_options():
    hlava = DeliciHlava()
    return jsonify({
        'diry': list(hlava.diry),
        'diry2': list(hlava.diry2)
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)