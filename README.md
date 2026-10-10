# ProyectoAPI – Propiedades edáficas de cultivos

Aplicación de consola, modular, que consulta el Excel *Resultados de Análisis de Laboratorio de Suelos en Colombia*.
Pide **departamento, municipio, cultivo y número de registros** y muestra una tabla con
**Departamento, Municipio, Cultivo, Topografía y la mediana de pH, Fósforo (P) y Potasio (K)**.

## Estructura
```
ProyectoAPI/
├── api/                 # Módulo API: datos y lógica
│   ├── __init__.py
│   ├── limpieza.py      # limpieza de pH / P / K y normalización de texto
│   └── suelos.py        # carga del Excel, consulta y medianas
├── ui/                  # Módulo UI: entrada/salida por consola
│   ├── __init__.py
│   └── consola.py
├── data/resultado_laboratorio_suelo.xlsx
├── tests/test_limpieza.py
├── evidencias/          # pantallazos y diagrama de componentes
├── main.py              # punto de entrada
└── requirements.txt
```

## Ejecución
```bash
python -m venv venv && source venv/bin/activate     
pip install -r requirements.txt
python main.py
python -m unittest discover -s tests -v              
```
Ejemplo: `RISARALDA` → `SANTA ROSA DE CABAL` → `Plátano` → `30`. En cualquier pregunta, `?` lista las opciones válidas.
La carga del Excel (≈46.700 filas) tarda ~13 s.

## Decisiones y limitaciones 
* **Registros:** se toman los primeros *N* que coinciden con departamento + municipio + cultivo (orden del archivo).
  Se muestra una fila por topografía y una fila `TODAS` (si hay más de una).
* **Valores `<límite` y `ND`** (p. ej. `<3,87`, `<0,09`) no se promedian; `N/D` indica que no hubo datos válidos.
* **El Excel está dañado**: al abrirse con otra configuración regional se perdió el punto decimal en P y K y varios pH
  quedaron como fechas. `api/limpieza.py` los reconstruye con reglas heurísticas (documentadas en el código).
  pH desde fecha (dd/mm → dd.mm) es fiable; la reubicación del punto en P y K es una **estimación** (distribución resultante:
  pH mediana 5,47; P 8,2 mg/kg; K 0,29 cmol/kg, coherente con suelos colombianos). Con el archivo original sin dañar, bastaría
  quitar esas reglas y usar `float()`.
