#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Web GUI pro výpočty dělicí hlavy
"""

from flask import Flask, render_template, request, jsonify
from deleni import DeliciHlava
from differentialThread import DifferentialThread
from DivisionPlatePlain import calculate_disks_radius
from findThread import ThreadPool
from knurling import count_crest_num4_dia
from plochyNaHrideli import PlochyNaHrideli
from pulleys import calculate2_pulleys, find_driven_diameter
from sineBar import calculate_link_sine_bar, calculate_contact_sine_bar
from tappingDrills import MetricThread
import math

# Thread pitch constants for performance
STOUPANI_MM = [0.4, 0.45, 0.5, 0.6, 0.7, 0.75, 0.8, 1.0, 1.25, 1.5, 1.75, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0]
STOUPANI_TPI = [4, 4.5, 5, 5.5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 16, 18, 20, 24, 28, 32, 36, 40, 44, 48, 56, 64, 72, 80]

def safe_float(value, param_name):
    """Safely convert value to float with validation"""
    if value is None:
        raise ValueError(f"Missing required parameter: {param_name}")
    try:
        result = float(value)
        if math.isnan(result) or math.isinf(result):
            raise ValueError(f"Invalid numeric value for {param_name}")
        return result
    except (ValueError, TypeError):
        raise ValueError(f"Invalid numeric value for {param_name}: {value}")

def safe_int(value, param_name):
    """Safely convert value to int with validation"""
    if value is None:
        raise ValueError(f"Missing required parameter: {param_name}")
    try:
        return int(value)
    except (ValueError, TypeError):
        raise ValueError(f"Invalid integer value for {param_name}: {value}")

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/deleni')
def deleni():
    return render_template('deleni.html')

@app.route('/differential')
def differential():
    return render_template('differential.html')

@app.route('/division-plate')
def division_plate():
    return render_template('division_plate.html')

@app.route('/find-thread')
def find_thread():
    return render_template('find_thread.html')

@app.route('/knurling')
def knurling():
    return render_template('knurling.html')

@app.route('/shaft-surfaces')
def shaft_surfaces():
    return render_template('shaft_surfaces.html')

@app.route('/en')
def index_en():
    return render_template('index_en.html')

@app.route('/en/dividing-head')
def dividing_head_en():
    return render_template('deleni_en.html')

@app.route('/en/differential-thread')
def differential_thread_en():
    return render_template('differential_en.html')

@app.route('/en/division-plate')
def division_plate_en():
    return render_template('division_plate_en.html')

@app.route('/en/find-thread')
def find_thread_en():
    return render_template('find_thread_en.html')

@app.route('/en/knurling')
def knurling_en():
    return render_template('knurling_en.html')

@app.route('/en/shaft-surfaces')
def shaft_surfaces_en():
    return render_template('shaft_surfaces_en.html')

@app.route('/material-bending')
def material_bending():
    return render_template('material_bending.html')

@app.route('/en/material-bending')
def material_bending_en():
    return render_template('material_bending_en.html')

@app.route('/pulleys')
def pulleys():
    return render_template('pulleys.html')

@app.route('/en/pulleys')
def pulleys_en():
    return render_template('pulleys_en.html')

@app.route('/sine-bar')
def sine_bar():
    return render_template('sine_bar.html')

@app.route('/en/sine-bar')
def sine_bar_en():
    return render_template('sine_bar_en.html')

@app.route('/tapping-drills')
def tapping_drills():
    return render_template('tapping_drills.html')

@app.route('/en/tapping-drills')
def tapping_drills_en():
    return render_template('tapping_drills_en.html')

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
    use_table = data.get('use_table', False)
    
    hlava = DeliciHlava(ratio, ratio_table)
    pocet_der = hlava.vypocti_pocet_der(deleni, use_table)
    
    result = {
        'deleni': deleni,
        'ratio': ratio,
        'ratio_table': ratio_table,
        'pocet_der': pocet_der,
        'success': pocet_der > 0,
        'use_table': use_table
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

@app.route('/api/differential', methods=['POST'])
def calculate_differential():
    data = request.json
    pozadovane_stoupani = float(data.get('pozadovane_stoupani'))
    jednotky = data.get('jednotky', 'mm')
    
    # Kontrola, zda je požadované stoupání přímo dostupné
    dostupne_hodnoty = STOUPANI_MM if jednotky == 'mm' else STOUPANI_TPI
    if pozadovane_stoupani in dostupne_hodnoty:
        return jsonify({
            'success': False,
            'error': f'Stoupání {pozadovane_stoupani} {jednotky} je přímo dostupné - nepotřebujete diferenciální závit!'
        })
    
    dt = DifferentialThread()
    
    try:
        kombinace = dt.vyzkousej_kombinace(pozadovane_stoupani, STOUPANI_TPI, STOUPANI_MM, jednotky)
        
        if kombinace:
            result = {
                'success': True,
                'pozadovane_stoupani': pozadovane_stoupani,
                'jednotky': jednotky,
                'hruby_zavit': kombinace[0],
                'jemny_zavit': kombinace[1],
                'efektivni_stoupani': kombinace[2],
                'odchylka': abs(pozadovane_stoupani - kombinace[2])
            }
        else:
            result = {
                'success': False,
                'error': 'Nelze najít vhodnou kombinaci'
            }
    except Exception as e:
        result = {
            'success': False,
            'error': str(e)
        }
    
    return jsonify(result)

@app.route('/api/division-plate', methods=['POST'])
def calculate_division_plate():
    data = request.json
    divisions = int(data.get('divisions'))
    diameter = float(data.get('diameter'))
    
    try:
        small_disk_radius = calculate_disks_radius(divisions, diameter)
        small_disk_diameter = small_disk_radius * 2
        
        result = {
            'success': True,
            'divisions': divisions,
            'diameter': diameter,
            'small_disk_radius': round(small_disk_radius, 4),
            'small_disk_diameter': round(small_disk_diameter, 4)
        }
    except Exception as e:
        result = {
            'success': False,
            'error': str(e)
        }
    
    return jsonify(result)

@app.route('/api/find-thread', methods=['POST'])
def find_thread_api():
    data = request.json
    value = float(data.get('value'))
    units = data.get('units', 'mm')
    criterion = data.get('criterion', 'diameter')
    
    try:
        thread_pool = ThreadPool()
        results = thread_pool.search_threads(value, units, criterion)
        
        threads_data = []
        for thread in results:
            threads_data.append({
                'name': thread.name,
                'diameter_mm': thread.diaMM if thread.diaMM != 'N/A' else None,
                'diameter_in': thread.diaInch if thread.diaInch != 'N/A' else None,
                'pitch_mm': thread.pitchMM if thread.pitchMM != 'N/A' else None,
                'pitch_tpi': thread.pitchTPI if thread.pitchTPI != 'N/A' else None
            })
        
        result = {
            'success': True,
            'value': value,
            'units': units,
            'criterion': criterion,
            'threads': threads_data,
            'count': len(threads_data)
        }
    except Exception as e:
        result = {
            'success': False,
            'error': str(e)
        }
    
    return jsonify(result)

@app.route('/api/knurling', methods=['POST'])
def calculate_knurling():
    data = request.json
    pitch = float(data.get('pitch'))
    diameter = float(data.get('diameter'))
    
    try:
        crest_count, required_circumference, ideal_diameter = count_crest_num4_dia(pitch, diameter)
        
        result = {
            'success': True,
            'pitch': pitch,
            'diameter': diameter,
            'crest_count': crest_count,
            'required_circumference': round(required_circumference, 3),
            'ideal_diameter': round(ideal_diameter, 2),
            'diameter_difference': round(ideal_diameter - diameter, 2)
        }
    except Exception as e:
        result = {
            'success': False,
            'error': str(e)
        }
    
    return jsonify(result)

@app.route('/api/shaft-surfaces', methods=['POST'])
def calculate_shaft_surfaces():
    data = request.json
    calculation_type = data.get('type')  # 'flat' or 'square'
    diameter = float(data.get('diameter'))
    
    try:
        pnh = PlochyNaHrideli()
        
        if calculation_type == 'square':
            depth, edge_length = pnh.hloubka_ctverce(diameter)
            result = {
                'success': True,
                'type': 'square',
                'diameter': diameter,
                'depth': round(depth, 2),
                'edge_length': round(edge_length, 2)
            }
        elif calculation_type == 'square_custom':
            edge_length = float(data.get('edge_length'))
            depth = pnh.hloubka_ctverce_custom(diameter, edge_length)
            result = {
                'success': True,
                'type': 'square_custom',
                'diameter': diameter,
                'edge_length': edge_length,
                'depth': round(depth, 2)
            }
        else:  # flat surface
            width = float(data.get('width'))
            depth = pnh.hloubka_plosky(diameter, width)
            result = {
                'success': True,
                'type': 'flat',
                'diameter': diameter,
                'width': width,
                'depth': round(depth, 2)
            }
    except Exception as e:
        result = {
            'success': False,
            'error': str(e)
        }
    
    return jsonify(result)

@app.route('/api/material-bending', methods=['POST'])
def calculate_material_bending():
    data = request.json
    thickness = float(data.get('thickness'))  # mm
    radius = float(data.get('radius'))        # mm
    angle = float(data.get('angle'))          # degrees
    
    try:
        # Convert to inches for calculation (as in original)
        thickness_in = thickness / 25.4
        radius_in = radius / 25.4
        
        # Convert angle to radians
        angle_rad = math.radians(angle)
        
        # Calculate x factor based on radius/thickness ratio
        x = 0.4 * thickness_in
        if radius_in < (2 * thickness_in):
            x = 0.3333 * thickness_in
        if radius_in > (4 * thickness_in):
            x = 0.5 * thickness_in
        
        # Calculate lengths
        material_length_in = angle_rad * (radius_in + x)
        outer_length_in = angle_rad * (radius_in + thickness_in)
        inner_length_in = angle_rad * radius_in
        
        # Convert back to mm
        material_length = material_length_in * 25.4
        outer_length = outer_length_in * 25.4
        inner_length = inner_length_in * 25.4
        
        result = {
            'success': True,
            'thickness': thickness,
            'radius': radius,
            'angle': angle,
            'material_length': round(material_length, 2),
            'outer_length': round(outer_length, 2),
            'inner_length': round(inner_length, 2)
        }
    except Exception as e:
        result = {
            'success': False,
            'error': str(e)
        }
    
    return jsonify(result)

@app.route('/api/pulleys', methods=['POST'])
def calculate_pulleys():
    data = request.json
    calculation_type = data.get('type')
    
    try:
        if calculation_type == 'calculate':
            driver_rpm = float(data.get('driver_rpm'))
            driver_dia = float(data.get('driver_dia'))
            driven_dia = float(data.get('driven_dia'))
            distance = float(data.get('distance'))
            
            driven_rpm, belt_length = calculate2_pulleys(driver_rpm, driver_dia, driven_dia, distance)
            
            result = {
                'success': True,
                'type': 'calculate',
                'driver_rpm': driver_rpm,
                'driver_dia': driver_dia,
                'driven_dia': driven_dia,
                'distance': distance,
                'driven_rpm': round(driven_rpm, 2),
                'belt_length': round(belt_length, 2)
            }
        else:  # find_diameter
            driver_rpm = float(data.get('driver_rpm'))
            driver_dia = float(data.get('driver_dia'))
            target_rpm = float(data.get('target_rpm'))
            
            driven_dia = find_driven_diameter(driver_rpm, target_rpm, driver_dia)
            
            result = {
                'success': True,
                'type': 'find_diameter',
                'driver_rpm': driver_rpm,
                'driver_dia': driver_dia,
                'target_rpm': target_rpm,
                'driven_dia': round(driven_dia, 2)
            }
    except Exception as e:
        result = {
            'success': False,
            'error': str(e)
        }
    
    return jsonify(result)

@app.route('/api/sine-bar', methods=['POST'])
def calculate_sine_bar():
    data = request.json
    method = data.get('method')  # 'link' or 'contact'
    angle = float(data.get('angle'))
    big_cylinder = float(data.get('big_cylinder'))
    
    try:
        if method == 'link':
            center_distance = float(data.get('center_distance'))
            small_cylinder = 2 * center_distance * math.sin(0.5 * math.radians(angle)) + big_cylinder
            
            result = {
                'success': True,
                'method': 'link',
                'angle': angle,
                'big_cylinder': big_cylinder,
                'center_distance': center_distance,
                'small_cylinder': round(small_cylinder, 4)
            }
        else:  # contact method
            sin_value = math.sin(0.5 * math.radians(angle))
            small_cylinder = big_cylinder * (1 - sin_value) / (1 + sin_value)
            
            result = {
                'success': True,
                'method': 'contact',
                'angle': angle,
                'big_cylinder': big_cylinder,
                'small_cylinder': round(small_cylinder, 4)
            }
    except Exception as e:
        result = {
            'success': False,
            'error': str(e)
        }
    
    return jsonify(result)

@app.route('/api/tapping-drills', methods=['POST'])
def calculate_tapping_drill():
    data = request.json
    thread_diameter = float(data.get('thread_diameter'))
    thread_pitch = float(data.get('thread_pitch'))
    thread_strength = float(data.get('thread_strength', 75))
    
    try:
        drill_diameter = MetricThread.countTapDrillSingle(thread_diameter, thread_pitch, thread_strength)
        
        result = {
            'success': True,
            'thread_diameter': thread_diameter,
            'thread_pitch': thread_pitch,
            'thread_strength': thread_strength,
            'drill_diameter': round(drill_diameter, 3)
        }
    except Exception as e:
        result = {
            'success': False,
            'error': str(e)
        }
    
    return jsonify(result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)