"""Pruebas funcionales de los endpoints de la API.""" 
from fastapi.testclient import TestClient 
  
from app.main import app, clasificar_eco 
from unittest.mock import patch, MagicMock
  
cliente = TestClient(app) 
  
"""
def test_health_responde_ok(): 
    r = cliente.get("/health") 
    assert r.status_code == 200 
    assert r.json()["estado"] == "ok"
"""

def test_health_responde_ok():
    # Simulamos el Context Manager de conexion()
    with patch("app.main.conexion") as mock_conexion:
        mock_con = MagicMock()
        mock_cur = MagicMock()
        mock_conexion.return_value.__enter__.return_value = mock_con
        mock_con.cursor.return_value.__enter__.return_value = mock_cur
        
        r = cliente.get("/health")
        
        assert r.status_code == 200
        assert r.json()["estado"] == "ok"

"""
def test_clasificar_eco_devuelve_tipo(): 
    r = cliente.post("/clasificar", json={"texto": "corrige el error de login", "motor": "eco"}) 
    assert r.status_code == 200 
    cuerpo = r.json() 
    assert cuerpo["tipo"] == "fix" 
    assert cuerpo["latencia_ms"] >= 0 
"""

def test_clasificar_eco_devuelve_tipo():
    with patch("app.main.conexion") as mock_conexion:
        # Simulamos que la DB ejecuta las consultas sin fallar
        mock_con = MagicMock()
        mock_cur = MagicMock()
        mock_conexion.return_value.__enter__.return_value = mock_con
        mock_con.cursor.return_value.__enter__.return_value = mock_cur

        r = cliente.post("/clasificar", json={"texto": "corrige el error de login", "motor": "eco"})
        assert r.status_code == 200
        cuerpo = r.json()
        assert cuerpo["tipo"] == "fix"
        assert cuerpo["latencia_ms"] >= 0
  
def test_clasificar_rechaza_motor_invalido(): 
    r = cliente.post("/clasificar", json={"texto": "hola", "motor": "inventado"}) 
    assert r.status_code == 400 
  
  
def test_reglas_del_motor_eco(): 
    assert clasificar_eco("agrega el endpoint de salud") == "feat" 
    assert clasificar_eco("actualiza el readme") == "docs" 
    assert clasificar_eco("agrega pruebas unitarias") == "test" 
  
"""
def test_inferencias_devuelve_lista(): 
    r = cliente.get("/inferencias?limite=5") 
    assert r.status_code == 200 
    assert isinstance(r.json(), list) 
"""

def test_inferencias_devuelve_lista():
    with patch("app.main.conexion") as mock_conexion:
        mock_con = MagicMock()
        mock_cur = MagicMock()
        mock_conexion.return_value.__enter__.return_value = mock_con
        mock_con.cursor.return_value.__enter__.return_value = mock_cur
        
        # Simulamos la respuesta que traería la consulta a la BD (ej. lista vacía o con un elemento)
        mock_cur.fetchall.return_value = []

        r = cliente.get("/inferencias?limite=5")
        assert r.status_code == 200
        assert isinstance(r.json(), list)