# Strojarina API Configuration Guide

## Požadavky pro API přístup

### 1. Spuštění serveru
```bash
# Pomocí Docker (doporučeno)
make web
# Server běží na http://localhost:5000

# Nebo manuálně
python src/gui_deleni_web.py
```

### 2. Instalace závislostí pro klienta
```bash
pip install requests
```

### 3. Testování API
```bash
# Spuštění ukázkového klienta
python src/apiExample.py

# Test připojení
curl http://localhost:5000/
```

## Dostupné API endpointy

### Trojúhelníky
- **POST** `/api/triangles/right` - Pravoúhlé trojúhelníky
- **POST** `/api/triangles/common` - Obecné trojúhelníky

### Strojařské výpočty
- **POST** `/api/deleni` - Dělicí hlava (výpočet děr)
- **POST** `/api/pocty` - Dělicí hlava (dosažitelná dělení)
- **POST** `/api/differential` - Diferenciální závit
- **POST** `/api/knurling` - Vroubkování
- **POST** `/api/shaft-surfaces` - Plochy na hřídeli
- **POST** `/api/material-bending` - Ohýbání materiálu
- **POST** `/api/pulleys` - Řemenice
- **POST** `/api/sine-bar` - Sinusové pravítko
- **POST** `/api/tapping-drills` - Závitníkové vrtáky
- **POST** `/api/find-thread` - Hledání závitů
- **POST** `/api/division-plate` - Dělicí kotouček

### Pomocné endpointy
- **GET** `/api/options` - Dostupné možnosti pro dělicí hlavu

## Formát požadavků

### Headers
```
Content-Type: application/json
```

### Příklad požadavku (pravoúhlý trojúhelník)
```json
{
    "a": 3,
    "b": 4,
    "precision": "1min"
}
```

### Příklad odpovědi
```json
{
    "success": true,
    "precision": "1min",
    "triangle": {
        "a": 3.0,
        "b": 4.0,
        "c": 5.0,
        "angle_A": 36.87,
        "angle_B": 53.13,
        "angle_C": 90.0,
        "area": 6.0,
        "perimeter": 12.0
    },
    "heights": {
        "h_a": 4.0,
        "h_b": 3.0,
        "h_c": 2.4
    },
    "circles_geometry": {
        "inradius": 1.0,
        "circumradius": 2.5,
        "medians": {
            "m_a": 4.272,
            "m_b": 3.606,
            "m_c": 2.5
        },
        "centroid": [1.333, 1.0]
    },
    "mollweide_valid": true
}
```

## Integrace s jinými programy

### Python
```python
import requests

response = requests.post(
    "http://localhost:5000/api/triangles/right",
    headers={"Content-Type": "application/json"},
    json={"a": 3, "b": 4, "precision": "1sec"}
)
result = response.json()
```

### JavaScript/Node.js
```javascript
const response = await fetch('http://localhost:5000/api/triangles/right', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({a: 3, b: 4, precision: '1sec'})
});
const result = await response.json();
```

### cURL
```bash
curl -X POST http://localhost:5000/api/triangles/right \
  -H "Content-Type: application/json" \
  -d '{"a": 3, "b": 4, "precision": "1sec"}'
```

### C# (.NET)
```csharp
using System.Text.Json;
using System.Text;

var client = new HttpClient();
var data = new { a = 3, b = 4, precision = "1sec" };
var json = JsonSerializer.Serialize(data);
var content = new StringContent(json, Encoding.UTF8, "application/json");

var response = await client.PostAsync(
    "http://localhost:5000/api/triangles/right", content);
var result = await response.Content.ReadAsStringAsync();
```

### Java
```java
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.net.URI;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.JsonNode;

// Using Jackson for JSON processing
ObjectMapper mapper = new ObjectMapper();
HttpClient client = HttpClient.newHttpClient();

// Create request data
var data = mapper.createObjectNode();
data.put("a", 3);
data.put("b", 4);
data.put("precision", "1sec");

// Build request
HttpRequest request = HttpRequest.newBuilder()
    .uri(URI.create("http://localhost:5000/api/triangles/right"))
    .header("Content-Type", "application/json")
    .POST(HttpRequest.BodyPublishers.ofString(mapper.writeValueAsString(data)))
    .build();

// Send request
HttpResponse<String> response = client.send(request, 
    HttpResponse.BodyHandlers.ofString());

// Parse response
if (response.statusCode() == 200) {
    JsonNode result = mapper.readTree(response.body());
    if (result.get("success").asBoolean()) {
        JsonNode triangle = result.get("triangle");
        System.out.println("Hypotenuse: " + triangle.get("c").asDouble());
        System.out.println("Area: " + triangle.get("area").asDouble());
    }
}
```

### Java (Spring Boot)
```java
@RestController
public class TriangleController {
    
    @Autowired
    private RestTemplate restTemplate;
    
    @PostMapping("/calculate")
    public ResponseEntity<?> calculateTriangle(@RequestBody TriangleRequest request) {
        String url = "http://localhost:5000/api/triangles/right";
        
        HttpHeaders headers = new HttpHeaders();
        headers.setContentType(MediaType.APPLICATION_JSON);
        
        HttpEntity<TriangleRequest> entity = new HttpEntity<>(request, headers);
        
        try {
            ResponseEntity<TriangleResponse> response = restTemplate.postForEntity(
                url, entity, TriangleResponse.class);
            return ResponseEntity.ok(response.getBody());
        } catch (Exception e) {
            return ResponseEntity.status(500).body("API call failed: " + e.getMessage());
        }
    }
}

// Data classes
class TriangleRequest {
    public double a, b;
    public String precision = "1min";
}

class TriangleResponse {
    public boolean success;
    public Triangle triangle;
    public Map<String, Double> heights;
    public CirclesGeometry circles_geometry;
}
```

## Zpracování chyb

### Chybové odpovědi
```json
{
    "success": false,
    "error": "At least 2 parameters required"
}
```

### HTTP status kódy
- **200** - Úspěch
- **400** - Chybný požadavek
- **500** - Chyba serveru

## Bezpečnost a limity

### CORS
Server podporuje CORS pro webové aplikace.

### Rate limiting
Momentálně nejsou implementovány limity rychlosti.

### Autentifikace
API je veřejné, autentifikace není vyžadována.

## Příklady použití

### CAD/CAM integrace
```python
# Výpočet geometrie pro CNC program
triangle_data = {"a": part_width, "b": part_height, "precision": "1sec"}
response = requests.post(api_url, json=triangle_data)
centroid = response.json()["circles_geometry"]["centroid"]
# Použití centroidu pro pozicování obrobku
```

### Java CAD/CAM Integration
```java
// CNC programming with triangle calculations
public class CNCProgrammer {
    private final HttpClient client = HttpClient.newHttpClient();
    private final ObjectMapper mapper = new ObjectMapper();
    
    public Point2D calculateCentroid(double partWidth, double partHeight) {
        var data = mapper.createObjectNode();
        data.put("a", partWidth);
        data.put("b", partHeight);
        data.put("precision", "1sec");
        
        HttpRequest request = HttpRequest.newBuilder()
            .uri(URI.create("http://localhost:5000/api/triangles/right"))
            .header("Content-Type", "application/json")
            .POST(HttpRequest.BodyPublishers.ofString(data.toString()))
            .build();
            
        try {
            HttpResponse<String> response = client.send(request,
                HttpResponse.BodyHandlers.ofString());
            JsonNode result = mapper.readTree(response.body());
            JsonNode centroid = result.get("circles_geometry").get("centroid");
            
            return new Point2D.Double(
                centroid.get(0).asDouble(),
                centroid.get(1).asDouble()
            );
        } catch (Exception e) {
            throw new RuntimeException("Failed to calculate centroid", e);
        }
    }
}
```

### Kontrola kvality
```python
# Ověření rozměrů trojúhelníkového dílu
measured_data = {"a": measured_a, "b": measured_b, "c": measured_c}
response = requests.post(common_triangle_url, json=measured_data)
if response.json()["mollweide_valid"]:
    print("Díl je v toleranci")
```

### Dávkové zpracování
```python
# Zpracování více dílů najednou
for part in parts_list:
    response = requests.post(api_url, json=part.to_dict())
    part.calculated_values = response.json()
```