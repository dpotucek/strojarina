#!/usr/bin/env python3
"""
API Example - Demonstrace použití Strojarina REST API
Ukázky volání všech dostupných API endpointů pro integraci s jinými programy

Konfigurace:
1. Spusť Strojarina server: make web (nebo python src/gui_deleni_web.py)
2. Server běží na http://localhost:5000
3. Nainstaluj requests: pip install requests
4. Spusť tento soubor: python src/apiExample.py

Created by David Potucek on Sep 18, 2025
Project: strojarina
"""

try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    import urllib.request
    import urllib.parse
    import urllib.error
    HAS_REQUESTS = False
    print("Warning: requests not installed, using urllib (limited functionality)")
    print("Install requests: pip install requests")

import json
import sys

# Konfigurace API
BASE_URL = "http://localhost:5000"
HEADERS = {"Content-Type": "application/json"}

def make_request(url, data=None, method='GET'):
    """Universal request function with fallback"""
    if HAS_REQUESTS:
        try:
            if method == 'GET':
                response = requests.get(url)
                return response.status_code, response.json() if response.status_code == 200 else None
            else:
                response = requests.post(url, headers=HEADERS, json=data)
                return response.status_code, response.json() if response.status_code == 200 else None
        except requests.exceptions.ConnectionError:
            return None, None
    else:
        try:
            if method == 'GET':
                with urllib.request.urlopen(url) as response:
                    return response.status, json.loads(response.read().decode())
            else:
                json_data = json.dumps(data).encode('utf-8')
                req = urllib.request.Request(url, data=json_data, headers=HEADERS)
                with urllib.request.urlopen(req) as response:
                    return response.status, json.loads(response.read().decode())
        except (urllib.error.URLError, urllib.error.HTTPError):
            return None, None

def test_api_connection():
    """Test připojení k API serveru"""
    status, data = make_request(f"{BASE_URL}/")
    if status == 200:
        print("✓ API server je dostupný")
        return True
    elif status:
        print(f"✗ API server nedostupný (status: {status})")
        return False
    else:
        print("✗ Nelze se připojit k API serveru")
        print("  Spusťte server: make web nebo python src/gui_deleni_web.py")
        return False

def triangle_right_api_example():
    """Ukázka API pro pravoúhlé trojúhelníky"""
    print("\n=== Pravoúhlé trojúhelníky ===")
    
    # Příklad 1: Ze dvou stran
    data = {
        "a": 3,
        "b": 4,
        "precision": "1min"
    }
    
    status, result = make_request(f"{BASE_URL}/api/triangles/right", data, 'POST')
    
    if status == 200 and result:
        if result["success"]:
            t = result["triangle"]
            h = result["heights"]
            cg = result["circles_geometry"]
            print(f"Strany a=3, b=4:")
            print(f"  Přepona: c = {t['c']}")
            print(f"  Úhly: A = {t['angle_A']}°, B = {t['angle_B']}°")
            print(f"  Výšky: h_a = {h['h_a']}, h_c = {h['h_c']}")
            print(f"  Vepsaná kružnice: r = {cg['inradius']}")
            print(f"  Těžiště: {cg['centroid']}")
        else:
            print(f"Chyba: {result['error']}")
    else:
        print(f"HTTP chyba: {status or 'Connection failed'}")

def triangle_common_api_example():
    """Ukázka API pro obecné trojúhelníky"""
    print("\n=== Obecné trojúhelníky ===")
    
    # Příklad: Ze tří stran
    data = {
        "a": 5,
        "b": 7,
        "c": 9,
        "precision": "1sec"
    }
    
    status, result = make_request(f"{BASE_URL}/api/triangles/common", data, 'POST')
    
    if status == 200 and result:
        if result["success"]:
            t = result["triangle"]
            cg = result["circles_geometry"]
            tt = result["triangle_type"]
            print(f"Strany a=5, b=7, c=9:")
            print(f"  Úhly: A = {t['angle_A']}°, B = {t['angle_B']}°, C = {t['angle_C']}°")
            print(f"  Obsah: {t['area']}")
            print(f"  Opsaná kružnice: R = {cg['circumradius']}")
            print(f"  Těžnice: {cg['medians']}")
            print(f"  Typ: {'pravoúhlý' if tt['right'] else 'obecný'}")
        else:
            print(f"Chyba: {result['error']}")

def division_head_api_example():
    """Ukázka API pro dělicí hlavu"""
    print("\n=== Dělicí hlava ===")
    
    # Výpočet děr pro dělení
    data = {
        "ratio": 40,
        "ratio_table": 120,
        "deleni": 17,
        "use_table": False
    }
    
    status, result = make_request(f"{BASE_URL}/api/deleni", data, 'POST')
    
    if status == 200 and result:
        if result["success"]:
            print(f"Pro dělení {result['deleni']}:")
            print(f"  Potřebný počet děr: {result['pocet_der']}")
            print(f"  Možné násobky: {result['nasobky']}")
        else:
            print("Nelze vypočítat - příliš mnoho děr")

def differential_thread_api_example():
    """Ukázka API pro diferenciální závit"""
    print("\n=== Diferenciální závit ===")
    
    data = {
        "pozadovane_stoupani": 1.3,
        "jednotky": "mm"
    }
    
    status, result = make_request(f"{BASE_URL}/api/differential", data, 'POST')
    
    if status == 200 and result:
        if result["success"]:
            print(f"Pro stoupání {result['pozadovane_stoupani']} mm:")
            print(f"  Hrubý závit: {result['hruby_zavit']} TPI")
            print(f"  Jemný závit: {result['jemny_zavit']} mm")
            print(f"  Efektivní stoupání: {result['efektivni_stoupani']} mm")
        else:
            print(f"Chyba: {result['error']}")

def knurling_api_example():
    """Ukázka API pro vroubkování"""
    print("\n=== Vroubkování ===")
    
    data = {
        "pitch": 0.8,
        "diameter": 25.4
    }
    
    status, result = make_request(f"{BASE_URL}/api/knurling", data, 'POST')
    
    if status == 200 and result:
        if result["success"]:
            print(f"Průměr {result['diameter']} mm, rozteč {result['pitch']} mm:")
            print(f"  Počet zubů: {result['crest_count']}")
            print(f"  Ideální průměr: {result['ideal_diameter']} mm")

def batch_calculations_example():
    """Ukázka dávkových výpočtů"""
    print("\n=== Dávkové výpočty ===")
    
    # Výpočet více trojúhelníků najednou
    triangles = [
        {"a": 3, "b": 4, "precision": "10min"},
        {"a": 5, "b": 12, "precision": "1min"},
        {"c": 10, "angle_A": 30, "precision": "1sec"}
    ]
    
    results = []
    for i, triangle_data in enumerate(triangles):
        status, result = make_request(f"{BASE_URL}/api/triangles/right", triangle_data, 'POST')
        if status == 200 and result:
            if result["success"]:
                results.append(result)
                t = result["triangle"]
                print(f"Trojúhelník {i+1}: c = {t['c']}, obsah = {t['area']}")
    
    print(f"Zpracováno {len(results)} trojúhelníků")

def error_handling_example():
    """Ukázka zpracování chyb"""
    print("\n=== Zpracování chyb ===")
    
    # Neplatné parametry
    invalid_data = {
        "a": 3,
        "b": 4,
        "c": 10,  # Neplatná kombinace - příliš mnoho parametrů
        "precision": "1min"
    }
    
    status, result = make_request(f"{BASE_URL}/api/triangles/right", invalid_data, 'POST')
    
    if status == 200 and result:
        if not result["success"]:
            print(f"Očekávaná chyba: {result['error']}")
    
    # Chybějící parametry
    empty_data = {"precision": "1min"}
    
    status, result = make_request(f"{BASE_URL}/api/triangles/right", empty_data, 'POST')
    
    if status == 200 and result:
        if not result["success"]:
            print(f"Očekávaná chyba: {result['error']}")

def main():
    """Hlavní funkce - spuštění všech ukázek"""
    print("Strojarina API Examples")
    print("=" * 50)
    
    # Test připojení
    if not test_api_connection():
        sys.exit(1)
    
    # Spuštění ukázek
    triangle_right_api_example()
    triangle_common_api_example()
    division_head_api_example()
    differential_thread_api_example()
    knurling_api_example()
    batch_calculations_example()
    error_handling_example()
    
    print("\n" + "=" * 50)
    print("Všechny API ukázky dokončeny")
    print("\nDostupné endpointy:")
    print("- POST /api/triangles/right - Pravoúhlé trojúhelníky")
    print("- POST /api/triangles/common - Obecné trojúhelníky")
    print("- POST /api/deleni - Dělicí hlava")
    print("- POST /api/pocty - Dosažitelná dělení")
    print("- POST /api/differential - Diferenciální závit")
    print("- POST /api/knurling - Vroubkování")
    print("- POST /api/shaft-surfaces - Plochy na hřídeli")
    print("- POST /api/material-bending - Ohýbání materiálu")
    print("- POST /api/pulleys - Řemenice")
    print("- POST /api/sine-bar - Sinusové pravítko")
    print("- POST /api/tapping-drills - Závitníkové vrtáky")
    print("- POST /api/find-thread - Hledání závitů")
    print("- POST /api/division-plate - Dělicí kotouček")

if __name__ == "__main__":
    main()