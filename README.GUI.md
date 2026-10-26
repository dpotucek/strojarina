# Architektura webového GUI

Tento dokument popisuje, jak spolupracují HTML/JavaScript rozhraní, Flask a výpočtové moduly. Aplikace je jeden Flask proces: Flask obsluhuje jak stránky, tak JSON API. Nejde o samostatný frontendový server ani o oddělenou síťovou službu pro výpočty.

## 1. Tři vrstvy a jejich odpovědnosti

| Vrstva | Kde ji hledat | Odpovědnost |
| --- | --- | --- |
| GUI | `src/templates/*.html`, případně `src/static/*.js` | Vykreslení formulářů, tabulek a výsledků, jazykové varianty, interakce uživatele a volání API pomocí `fetch`. Některé jednoduché nebo starší nástroje provádějí část výpočtů přímo v JavaScriptu. |
| Spojovací vrstva | `src/flask_app.py` | Flask aplikace a routy. Zobrazuje šablony, načítá formulářová/JSON data, převádí a validuje vstupy, volá výpočty a vrací HTML nebo JSON. |
| Výpočtový backend | Moduly `src/*.py` a knihovna `DaPTools` | Výpočtová logika a doménová data. Moduly zpravidla neznají webové formuláře ani HTTP; přijímají hodnoty funkcí/tříd a vracejí výsledky. |

Flask je tedy prostředníkem mezi GUI a výpočty: šablona neposílá požadavky přímo do Python modulu a výpočtový modul nevykresluje webovou stránku.

## 2. Průchod požadavku aplikací

1. Prohlížeč otevře stránku, například `/tapers`.
2. Flask vybere obslužnou funkci podle URL a zavolá `render_template(...)`. Jinja dosadí texty a referenční data do HTML šablony.
3. Uživatel zadá hodnoty. JavaScript může provést základní kontrolu a pošle je metodou HTTP `POST` jako JSON na `/api/...`.
4. Příslušná API routa získá data z `request`, převede číselné hodnoty přes pomocné funkce jako `safe_float` a `safe_int` a zavolá funkci nebo třídu výpočtového backendu.
5. Routa připraví odpověď pomocí `jsonify(...)`. JavaScript zpracuje JSON a vykreslí výsledek do aktuální stránky bez jejího opětovného načtení.

Jednotlivé nástroje se liší: některé hodnoty a tabulky Flask dosazuje už při načtení stránky, jiné interakce obsluhuje JavaScript a některé starší nástroje mají část výpočtové logiky v prohlížeči. Konkrétní implementaci proto vždy ověřte v odpovídající šabloně a routě.

## 3. Příklad: výpočet kužele

Pro stránku kuželů je vazba rozdělena takto:

- `src/templates/tapers.html` obsahuje formulář a JavaScript. JavaScript pošle vstupy na `/api/tapers/calculate`.
- `calculate_taper_api()` v `src/flask_app.py` převezme JSON, převede rozměry a zavolá výpočtovou funkci.
- `calculate_taper()` v `src/tapers.py` provede výpočet bez znalosti Flasku a HTML.
- Flask vrátí výstup funkce jako JSON; JavaScript doplní výsledné úhly, posuv koníku a kontrolní rozměry do stránky.

Převody poměru a úhlu používají obdobnou cestu přes `/api/tapers/ratio-to-angle` a `/api/tapers/angle-to-ratio`. Tabulky Morse a ISO jsou data backendu předaná při vykreslení šablony, takže pro jejich zobrazení není potřeba samostatný požadavek JavaScriptu.

## 4. Příklad: napojení výpočtu z DaPTools

Flask může volat také funkce z externí knihovny. Například v `src/flask_app.py` se importují:

```python
from daptools.redeni import dilution, mixing
```

Šablona `src/templates/redeni.html` pošle data na `/api/redeni/dilution` nebo `/api/redeni/mixing`. Routa převede vstupy, zavolá odpovídající funkci z `daptools.redeni` a připraví webovou odpověď. Samotný modul `redeni.py` obsahuje výpočty a jejich doménovou validaci; neřeší Flask ani webové formuláře.

DaPTools se do tohoto projektu instaluje jako wheel v `wheels/`. Dockerfile wheel nainstaluje při sestavení obrazu. Cíl `make update-daptools` sestaví wheel v sousedním projektu `../DaPTools`, zkopíruje jej do `wheels/` a znovu sestaví kontejner.

## 5. Routy a umístění kódu

- **Stránky:** routy v `flask_app.py` vracejí `render_template(...)`. České a anglické stránky mají obvykle různé URL a buď dvě šablony, nebo jednu šablonu s předanými lokalizovanými popisky. Příklady: `/tapers`, `/en/tapers`, `/cutting-conditions`, `/en/cutting-conditions`.
- **Výpočtové API:** routy `/api/...` přijímají vstupy a vracejí JSON. Novější samostatné nástroje mají vlastní moduly, například `tapers.py` a `cutting_conditions.py`; některé starší výpočty jsou přímo uvnitř `gui_deleni_web.py`.
- **Statické obrázky a data:** `/static/data/<soubor>` obsluhuje soubory z adresáře `data/`, například obrázky geometrie. JavaScriptové soubory jsou v `src/static/`.
- **Šablony:** Flask hledá Jinja šablony v `src/templates/`. Soubory s příponou `_en.html` jsou anglické varianty tam, kde aplikace používá oddělené šablony.

API není zcela sjednoceno do jediného formátu chyb. Některé routy vracejí HTTP `400` při neplatném vstupu a JSON `{"success": false, "error": "..."}`, jiné historické routy vracejí JSON s příznakem `success` a mohou použít HTTP `200`. Při přidávání funkce se řiďte konvencí nejbližšího příbuzného API a tuto odlišnost zachovejte nebo cíleně otestujte.

## 6. Přidání dalšího nástroje

1. Umístěte výpočet do samostatného modulu `src/<nastroj>.py`, pokud jej lze oddělit od HTTP a vykreslování. Funkce mají přijímat běžné hodnoty, vracet datový výsledek a hlásit neplatné vstupy výjimkou `ValueError`.
2. V `flask_app.py` importujte výpočet a přidejte stránkovou routu. Pro API vytvořte routu, která načte požadavek, převede vstupy, zavolá výpočet a převede výsledek na JSON.
3. Přidejte šablonu do `src/templates/`. Použijte API routu pro výpočet v prohlížeči; nezávislé hodnoty a formátování mohou zůstat v JavaScriptu, ale výpočtová logika by neměla být nechtěně rozdělena mezi dvě implementace.
4. Přidejte odkaz na nástroj do české i anglické domovské stránky a odpovídající lokalizované popisky.
5. Otestujte výpočtový modul zvlášť a přes `app.test_client()` ověřte stránku, API odpovědi, neplatné vstupy a jazykové varianty.

Základní pravidlo: validace v prohlížeči zlepšuje použitelnost, ale není náhradou serverové validace. API musí zkontrolovat příchozí data i v případě, že je formulář kontroluje už před odesláním.

## 7. Příklad: změna popisku v kalkulaci kuželu

Chcete-li změnit text uživatelského popisku „Délka kužele l (mm)“, změňte lokalizační slovník v `src/gui_deleni_web.py`:

```python
_TAPER_LABELS = {
    "cs": {
        "taper_length": "Délka kužele l (mm)",
        # ostatní české popisky
    },
    "en": {
        "taper_length": "Taper length l (mm)",
        # ostatní anglické popisky
    },
}
```

Šablona `src/templates/tapers.html` zobrazuje tuto hodnotu přes `{{ labels.taper_length }}` u vstupního pole. Zpravidla tedy stačí upravit text ve správném jazyce v `_TAPER_LABELS`; do šablony ani výpočtu v `src/tapers.py` není třeba zasahovat.

Pokud měníte popisek, který se skládá přímo v HTML nebo JavaScriptu, upravte příslušné místo v `tapers.html`. Jestliže se mění význam či samotný výpočet, upravte backend v `tapers.py` a návaznou Flask routu v `flask_app.py` podle změny vstupů nebo výstupů. Po změně ověřte obě jazykové varianty a spusťte `tests/testTapers.py`.

## 8. Spuštění a testování

- Webové GUI v Dockeru se spouští příkazem `make web`; Makefile nejprve aktualizuje DaPTools a potom kontejner. Stránka je dostupná na `http://localhost:5000`.
- Výchozí příkaz kontejneru je `python src/flask_app.py`; Flask server poslouchá na portu `5000`.
- Testy jsou v `tests/`. Pro test Flask rout používejte testovací klient Flasku namísto závislosti na běžícím serveru.
- `make test` nejprve sestaví aktuální Docker image a poté v něm spustí `pytest`. Dockerfile instaluje hlavní i vývojové závislosti pomocí `poetry install --with dev`, takže image obsahuje i test runner.
- Pro rychlý lokální běh lze použít `python -m pytest tests/` ve výše uvedeném prostředí.

Příklady volání API z terminálu:

```bash
curl -X POST http://localhost:5000/api/tapers/calculate \
  -H 'Content-Type: application/json' \
  -d '{"large_diameter":30,"small_diameter":20,"taper_length":100,"work_length":200}'

curl -X POST http://localhost:5000/api/redeni/dilution \
  -H 'Content-Type: application/json' \
  -d '{"v_start":1,"c_poc":74,"c_cil":40}'
```
