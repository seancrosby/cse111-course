# Copyright © 2026, Brigham Young University–Idaho. All rights reserved.

import pytest
from pytest import approx
from bom_parser import parse_bom
from bom_catalog import get_parts_catalog

def test_parse_bom():
    # Convert list to dict for the parser's requirement
    catalog = {p[0]: [p[1], p[2]] for p in get_parts_catalog()}
    
    # Test Case 1: Simple parts
    bom1 = "Frm:1, Hnd:1"
    parts1 = parse_bom(bom1, catalog)
    assert ["Frm", 1.0] in parts1
    assert ["Hnd", 1.0] in parts1
    assert len(parts1) == 2

    # Test Case 2: Grouped parts (1 Wheel)
    bom2 = "(Rim:1, Spk:28, Tir:1):1"
    parts2 = parse_bom(bom2, catalog)
    assert ["Rim", 1.0] in parts2
    assert ["Spk", 28.0] in parts2
    assert ["Tir", 1.0] in parts2

    # Test Case 3: Complex nested (The Full Bike)
    # Frm(150) + Hnd(35) + Sdl(20) + 2*(Rim(25) + 28*Spk(0.5) + Tir(15))
    # 150 + 35 + 20 + 2*(54) = 313.00
    bom3 = "Frm:1, Hnd:1, Sdl:1, (Rim:1, Spk:28, Tir:1):2"
    parts3 = parse_bom(bom3, catalog)
    
    rim_qty = next(p[1] for p in parts3 if p[0] == "Rim")
    spk_qty = next(p[1] for p in parts3 if p[0] == "Spk")
    assert rim_qty == 2.0
    assert spk_qty == 56.0

if __name__ == "__main__":
    pytest.main(["-v", "--tb=line", "-rN", __file__])
