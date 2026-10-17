from datetime import datetime


def get_hotdogs():
    """Return the hotdogs and their regular prices."""
    hotdogs = [
        ["Classic Hotdog", 3.50],
        ["Chili Cheese Dog", 4.75],
        ["Chicago Dog", 5.25],
        ["Corn Dog", 3.25],
        ["Veggie Dog", 4.00]
    ]
    return hotdogs


def get_daily_special(day, hotdogs):
    """Return the hotdog selected as the daily special."""
    special_index = day % len(hotdogs)
    return hotdogs[special_index]


def calculate_special_price(price):
    """Return a price with the daily 10 percent discount applied."""
    return price * 0.90


def format_menu_line(text, width):
    """Return text centered inside a menu line with the given total width."""
    return f"|{text:^{width - 2}}|"


def print_menu_item(name, price, width):
    """Print one menu item and its price inside the menu border."""
    price_text = f"${price:>6.2f}"
    name_width = width - len(price_text) - 5
    text = f" {name:<{name_width}} {price_text} "
    print(format_menu_line(text, width))


def display_menu(day, width):
    """Print the menu for the specified day at the given width."""
    hotdogs = get_hotdogs()
    auxiliary_items = [
        ["Ice Cream Bar", 2.50],
        ["Bottled Water", 1.50],
        ["Extra Mustard", 0.25]
    ]
    special = get_daily_special(day, hotdogs)
    special_price = calculate_special_price(special[1])

    print(f"+{'=' * (width - 2)}+")
    print(format_menu_line("The Hotdog Stand", width))
    print(f"+{'=' * (width - 2)}+")
    for hotdog in hotdogs:
        print_menu_item(hotdog[0], hotdog[1], width)
    print(format_menu_line("=" * (width - 3), width - 1))
    print(format_menu_line("Daily Special", width))
    print_menu_item(special[0], special_price, width)
    print(format_menu_line("10% off", width))
    print(format_menu_line("=" * (width - 2), width))
    print(format_menu_line("Auxiliary Items", width))
    for item in auxiliary_items:
        print_menu_item(item[0], item[1], width)
    print(f"+{'=' * (width - 2)}+")


def main():
    width = 37
    day = datetime.now().day + 1
    display_menu(day, width)


if __name__ == "__main__":
    main()
