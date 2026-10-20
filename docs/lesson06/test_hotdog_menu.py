import pytest

from hotdog_menu import (
    calculate_special_price,
    display_menu,
    format_menu_line,
    get_daily_special,
    get_hotdogs,
    print_menu_item,
)


def test_get_hotdogs():
    prices = get_hotdogs()
    assert prices == [
        ["Classic Hotdog", 3.50],
        ["Chili Cheese Dog", 4.75],
        ["Chicago Dog", 6.25],
        ["Corn Dog", 3.25],
        ["Veggie Dog", 4.00],
    ]


def test_get_daily_special():
    hotdogs = get_hotdogs()

    assert get_daily_special(7, hotdogs) == ["Chicago Dog", 5.25]


def test_calculate_special_price():
    assert calculate_special_price(5.25) == pytest.approx(4.725)


def test_format_menu_line():
    assert format_menu_line("Test", 10) == "|  Test  |"


def test_print_menu_item(capsys):
    print_menu_item("Classic Hotdog", 3.50, 37)

    assert capsys.readouterr().out == "| Classic Hotdog            $  3.50 |\n"


def test_display_menu_line_widths(capsys):
    width = 37
    display_menu(1, width)

    menu_lines = capsys.readouterr().out.splitlines()
    for number, line in enumerate(menu_lines, start=1):
        assert len(line) == width, (
            f"Menu line {number} has length {len(line)}: {line!r}"
        )


pytest.main(["-v", "--tb=line", "-rN", __file__])
