"""
Author: Messiah Yusef, Kaporsha Alexander, Paige Gray
Date: March 29, 2026
File: team_pizza_program.py

Team Pizza Project for IS 280 - Python
This program simulates placing a pizza order and prints a recipe for the pizza chef.

Concepts demonstrated:
- Lists and dictionaries
- Accessing container elements by index
- Passing container objects to functions
- Returning container objects from functions
"""

from typing import Dict, List, Tuple

MAX_INGREDIENTS = 8


def get_ingredient_catalog() -> List[Dict[str, object]]:
    """Return the pizza ingredient catalog as a list of dictionaries."""
    return [
        {"code": "1a", "name": "Crust - regular", "measure": "each", "max_qty": 1, "category": "Crust"},
        {"code": "1b", "name": "Crust - gluten-free", "measure": "each", "max_qty": 1, "category": "Crust"},
        {"code": "2", "name": "Red Sauce", "measure": "1/4 cup", "max_qty": 2, "category": "Sauce"},
        {"code": "3", "name": "Pizza cheese", "measure": "1/4 cup", "max_qty": 2, "category": "Cheese"},
        {"code": "4", "name": "Diced onion", "measure": "1/8 cup", "max_qty": 2, "category": "Vegetable"},
        {"code": "5", "name": "Diced green pepper", "measure": "1/8 cup", "max_qty": 2, "category": "Vegetable"},
        {"code": "6", "name": "Pepperoni", "measure": "2 pieces", "max_qty": 4, "category": "Meat"},
        {"code": "7", "name": "Sliced mushroom", "measure": "1/8 cup", "max_qty": 2, "category": "Vegetable"},
        {"code": "8", "name": "Diced jalapenos", "measure": "1/8 cup", "max_qty": 2, "category": "Vegetable"},
        {"code": "9", "name": "Sardines", "measure": "each", "max_qty": 4, "category": "Protein"},
        {"code": "10", "name": "Pineapple Chunks", "measure": "2 pieces", "max_qty": 4, "category": "Fruit"},
        {"code": "11", "name": "Tofu", "measure": "1/4 cup", "max_qty": 2, "category": "Protein"},
        {"code": "12", "name": "Ham Chunks", "measure": "4 pieces", "max_qty": 4, "category": "Meat"},
        {"code": "13", "name": "Dry red pepper", "measure": "Generous sprinkle", "max_qty": 4, "category": "Seasoning"},
        {"code": "14", "name": "Dried basil", "measure": "Generous sprinkle", "max_qty": 2, "category": "Seasoning"},
    ]


def build_code_lookup(catalog: List[Dict[str, object]]) -> Dict[str, Dict[str, object]]:
    """Return a dictionary for quick ingredient lookup by item code."""
    lookup = {}
    for ingredient in catalog:
        lookup[str(ingredient["code"]).lower()] = ingredient
    return lookup


def display_menu(catalog: List[Dict[str, object]]) -> None:
    """Display all available ingredients and quantity limits."""
    print("\n" + "=" * 72)
    print("WELCOME TO THE TEAM PIZZA ORDERING SYSTEM")
    print("=" * 72)
    print(f"You may choose up to {MAX_INGREDIENTS} different ingredients total.")
    print("The order matters because the recipe will be printed in the same order.\n")
    print("{:<4} {:<24} {:<20} {:<8}".format("Code", "Ingredient", "Measure", "Max Qty"))
    print("-" * 72)

    for ingredient in catalog:
        print(
            "{:<4} {:<24} {:<20} {:<8}".format(
                ingredient["code"],
                ingredient["name"],
                ingredient["measure"],
                ingredient["max_qty"],
            )
        )
    print("-" * 72)


def prompt_for_code(lookup: Dict[str, Dict[str, object]], selected_items: List[Dict[str, object]]) -> str:
    """Prompt the user for the next ingredient code and validate it."""
    already_selected = {item["code"].lower() for item in selected_items}

    while True:
        code = input("Enter the next ingredient code: ").strip().lower()

        if code not in lookup:
            print("Invalid code. Please choose a code from the menu.")
            continue

        ingredient = lookup[code]

        if ingredient["category"] == "Crust":
            for item in selected_items:
                if item["category"] == "Crust":
                    print("You may choose only one crust.")
                    break
            else:
                return code
            continue

        if code in already_selected:
            print("That ingredient has already been selected. Choose a different ingredient.")
            continue

        return code


def prompt_for_quantity(ingredient: Dict[str, object]) -> int:
    """Prompt the user for a valid quantity for the chosen ingredient."""
    max_qty = int(ingredient["max_qty"])
    while True:
        quantity_text = input(
            f"Enter quantity for {ingredient['name']} "
            f"(1 to {max_qty}, measure: {ingredient['measure']}): "
        ).strip()

        if not quantity_text.isdigit():
            print("Please enter a whole number.")
            continue

        quantity = int(quantity_text)
        if 1 <= quantity <= max_qty:
            return quantity

        print(f"Quantity must be between 1 and {max_qty}.")


def prompt_yes_no(message: str) -> bool:
    """Return True for yes and False for no."""
    while True:
        response = input(message).strip().lower()
        if response in ("y", "yes"):
            return True
        if response in ("n", "no"):
            return False
        print("Please enter yes or no.")


def collect_order(catalog: List[Dict[str, object]], lookup: Dict[str, Dict[str, object]]) -> List[Dict[str, object]]:
    """Collect the ordered ingredients and return them as a list."""
    selected_items = []

    while len(selected_items) < MAX_INGREDIENTS:
        print(f"\nIngredient {len(selected_items) + 1} of {MAX_INGREDIENTS}")
        code = prompt_for_code(lookup, selected_items)
        ingredient = lookup[code]
        quantity = prompt_for_quantity(ingredient)

        order_item = {
            "code": ingredient["code"],
            "name": ingredient["name"],
            "measure": ingredient["measure"],
            "quantity": quantity,
            "category": ingredient["category"],
        }
        selected_items.append(order_item)

        print(f"Added: {quantity} x {ingredient['measure']} of {ingredient['name']}")

        if len(selected_items) == MAX_INGREDIENTS:
            print("\nYou have reached the maximum of 8 different ingredients.")
            break

        done = prompt_yes_no("Are you finished adding ingredients? (yes/no): ")
        if done:
            break

    return selected_items


def validate_required_items(order: List[Dict[str, object]]) -> Tuple[bool, List[str]]:
    """Check whether the pizza has crust, sauce, and cheese."""
    categories = [item["category"] for item in order]
    missing = []

    if "Crust" not in categories:
        missing.append("a crust")
    if "Sauce" not in categories:
        missing.append("red sauce")
    if "Cheese" not in categories:
        missing.append("pizza cheese")

    return len(missing) == 0, missing


def print_recipe(order: List[Dict[str, object]]) -> None:
    """Print the final recipe for the pizza chef."""
    print("\n" + "=" * 72)
    print("FINAL PIZZA RECIPE")
    print("=" * 72)
    print("Build the pizza in the exact order shown below:\n")

    for index, item in enumerate(order):
        print(
            f"Step {index + 1}: Add {item['quantity']} x {item['measure']} of {item['name']}"
        )

    print(
        "\nCooking Instructions: Pizza is to be appropriately cooked until "
        "crust is cooked and topping is fully warmed."
    )
    print("=" * 72)


def main() -> None:
    """Run the pizza ordering program."""
    catalog = get_ingredient_catalog()
    lookup = build_code_lookup(catalog)

    display_menu(catalog)
    order = collect_order(catalog, lookup)

    is_valid, missing_items = validate_required_items(order)
    if not is_valid:
        print("\nERROR: The pizza order is incomplete.")
        print("Missing required item(s): " + ", ".join(missing_items))
        print("Please restart the program and include crust, sauce, and cheese.")
        return

    print_recipe(order)


if __name__ == "__main__":
    main()