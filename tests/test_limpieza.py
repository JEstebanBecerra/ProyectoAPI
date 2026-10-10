"""Pruebas de la limpieza de datos. Ejecutar: python -m unittest discover -s tests -v"""
import math
import os
import sys
import unittest
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from api.limpieza import limpiar_fosforo, limpiar_ph, limpiar_potasio, normalizar


class PruebasLimpieza(unittest.TestCase):
    def test_normalizar(self):
        self.assertEqual(normalizar("Santa Rosa de Cábal "), "SANTA ROSA DE CABAL")
        self.assertEqual(normalizar("BOGOTÁ,  D.C."), "BOGOTA D C")

    def test_ph(self):
        self.assertAlmostEqual(limpiar_ph("5.66"), 5.66)
        self.assertAlmostEqual(limpiar_ph(datetime(2024, 5, 6)), 6.05)   # fecha -> pH
        self.assertAlmostEqual(limpiar_ph(5), 5.0)
        self.assertTrue(math.isnan(limpiar_ph(6686)))                    # fuera de rango

    def test_fosforo(self):
        self.assertTrue(math.isnan(limpiar_fosforo("<3,87")))            # bajo detección
        self.assertAlmostEqual(limpiar_fosforo("4.13"), 4.13)
        self.assertAlmostEqual(limpiar_fosforo(5622298591549290), 5.62229859154929)
        self.assertAlmostEqual(limpiar_fosforo(38940497284938496), 38.940497284938496)
        self.assertAlmostEqual(limpiar_fosforo(2594), 2.594)

    def test_potasio(self):
        self.assertTrue(math.isnan(limpiar_potasio("<0,09")))
        self.assertAlmostEqual(limpiar_potasio("0.16"), 0.16)
        self.assertAlmostEqual(limpiar_potasio(524192688), 0.524192688)
        self.assertAlmostEqual(limpiar_potasio(24003928799999900), 0.240039287999999)


if __name__ == "__main__":
    unittest.main()
