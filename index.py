"""
Author: Messiah Yusef, Kaporsha Alexander, Paige Gray
Date: March 29, 2026
File: index.py

Team Pizza Project for IS 280 - Python
This version adds a simple tkinter GUI to the pizza ordering program.
"""

from typing import Dict, List, Tuple
import tkinter as tk
from tkinter import ttk, messagebox

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


class PizzaOrderingApp:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Team Pizza Ordering System")
        self.root.geometry("1000x650")

        self.catalog = get_ingredient_catalog()
        self.lookup = build_code_lookup(self.catalog)
        self.selected_items: List[Dict[str, object]] = []

        self.selected_code = tk.StringVar()
        self.quantity_var = tk.StringVar(value="1")
        self.status_var = tk.StringVar(value="Choose ingredients for your pizza.")

        self.build_ui()

    def build_ui(self) -> None:
        title = tk.Label(
            self.root,
            text="WELCOME TO THE TEAM PIZZA ORDERING SYSTEM",
            font=("Arial", 18, "bold"),
            pady=10,
        )
        title.pack()

        subtitle = tk.Label(
            self.root,
            text=f"Choose up to {MAX_INGREDIENTS} different ingredients. Order matters.",
            font=("Arial", 11),
        )
        subtitle.pack(pady=(0, 10))

        main_frame = tk.Frame(self.root, padx=10, pady=10)
        main_frame.pack(fill="both", expand=True)

        left_frame = tk.LabelFrame(main_frame, text="Ingredient Menu", padx=10, pady=10)
        left_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))

        right_frame = tk.LabelFrame(main_frame, text="Current Order", padx=10, pady=10)
        right_frame.pack(side="right", fill="both", expand=True)

        columns = ("code", "name", "measure", "max_qty", "category")
        self.tree = ttk.Treeview(left_frame, columns=columns, show="headings", height=16)
        self.tree.heading("code", text="Code")
        self.tree.heading("name", text="Ingredient")
        self.tree.heading("measure", text="Measure")
        self.tree.heading("max_qty", text="Max Qty")
        self.tree.heading("category", text="Category")

        self.tree.column("code", width=70, anchor="center")
        self.tree.column("name", width=220)
        self.tree.column("measure", width=140, anchor="center")
        self.tree.column("max_qty", width=80, anchor="center")
        self.tree.column("category", width=100, anchor="center")

        for ingredient in self.catalog:
            self.tree.insert(
                "",
                "end",
                values=(
                    ingredient["code"],
                    ingredient["name"],
                    ingredient["measure"],
                    ingredient["max_qty"],
                    ingredient["category"],
                ),
            )

        self.tree.pack(fill="both", expand=True)
        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)

        controls = tk.Frame(left_frame, pady=10)
        controls.pack(fill="x")

        tk.Label(controls, text="Selected Code:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.code_entry = tk.Entry(controls, textvariable=self.selected_code, width=12)
        self.code_entry.grid(row=0, column=1, sticky="w", padx=5, pady=5)

        tk.Label(controls, text="Quantity:").grid(row=0, column=2, sticky="w", padx=5, pady=5)
        self.quantity_spinbox = tk.Spinbox(controls, from_=1, to=4, textvariable=self.quantity_var, width=8)
        self.quantity_spinbox.grid(row=0, column=3, sticky="w", padx=5, pady=5)

        add_button = tk.Button(controls, text="Add Ingredient", width=15, command=self.add_ingredient)
        add_button.grid(row=0, column=4, padx=8, pady=5)

        clear_button = tk.Button(controls, text="Clear Order", width=12, command=self.clear_order)
        clear_button.grid(row=0, column=5, padx=8, pady=5)

        self.order_listbox = tk.Listbox(right_frame, width=45, height=16, font=("Courier New", 11))
        self.order_listbox.pack(fill="both", expand=True, pady=(0, 10))

        button_row = tk.Frame(right_frame)
        button_row.pack(fill="x")

        remove_button = tk.Button(button_row, text="Remove Selected", width=15, command=self.remove_selected)
        remove_button.pack(side="left", padx=5)

        finish_button = tk.Button(button_row, text="Finish Order", width=15, command=self.finish_order)
        finish_button.pack(side="right", padx=5)

        self.status_label = tk.Label(
            self.root,
            textvariable=self.status_var,
            anchor="w",
            relief="sunken",
            padx=10,
            pady=8,
        )
        self.status_label.pack(fill="x", side="bottom")

    def on_tree_select(self, event=None) -> None:
        selected = self.tree.selection()
        if not selected:
            return

        values = self.tree.item(selected[0], "values")
        code = str(values[0]).lower()
        ingredient = self.lookup[code]
        self.selected_code.set(code)
        self.quantity_var.set("1")
        self.quantity_spinbox.config(to=int(ingredient["max_qty"]))
        self.status_var.set(f"Selected {ingredient['name']} ({ingredient['measure']}).")

    def add_ingredient(self) -> None:
        if len(self.selected_items) >= MAX_INGREDIENTS:
            messagebox.showerror("Maximum Reached", "You have already selected the maximum of 8 ingredients.")
            return

        code = self.selected_code.get().strip().lower()
        if code not in self.lookup:
            messagebox.showerror("Invalid Code", "Please select a valid ingredient code.")
            return

        ingredient = self.lookup[code]

        try:
            quantity = int(self.quantity_var.get())
        except ValueError:
            messagebox.showerror("Invalid Quantity", "Please enter a whole number for quantity.")
            return

        max_qty = int(ingredient["max_qty"])
        if not 1 <= quantity <= max_qty:
            messagebox.showerror("Invalid Quantity", f"Quantity must be between 1 and {max_qty}.")
            return

        already_selected = {str(item["code"]).lower() for item in self.selected_items}
        crust_already_selected = any(item["category"] == "Crust" for item in self.selected_items)

        if ingredient["category"] == "Crust" and crust_already_selected:
            messagebox.showerror("Crust Error", "You may choose only one crust.")
            return

        if code in already_selected:
            messagebox.showerror("Duplicate Ingredient", "That ingredient has already been selected.")
            return

        order_item = {
            "code": ingredient["code"],
            "name": ingredient["name"],
            "measure": ingredient["measure"],
            "quantity": quantity,
            "category": ingredient["category"],
        }
        self.selected_items.append(order_item)
        self.refresh_order_list()
        self.status_var.set(f"Added {quantity} x {ingredient['measure']} of {ingredient['name']}.")

    def refresh_order_list(self) -> None:
        self.order_listbox.delete(0, tk.END)
        for index, item in enumerate(self.selected_items, start=1):
            line = f"{index}. {item['quantity']} x {item['measure']} of {item['name']}"
            self.order_listbox.insert(tk.END, line)

    def remove_selected(self) -> None:
        selected_index = self.order_listbox.curselection()
        if not selected_index:
            messagebox.showerror("No Selection", "Please select an ingredient from the order list to remove.")
            return

        index = selected_index[0]
        removed_item = self.selected_items.pop(index)
        self.refresh_order_list()
        self.status_var.set(f"Removed {removed_item['name']} from the order.")

    def clear_order(self) -> None:
        self.selected_items.clear()
        self.refresh_order_list()
        self.status_var.set("Order cleared.")

    def finish_order(self) -> None:
        is_valid, missing_items = validate_required_items(self.selected_items)
        if not is_valid:
            messagebox.showerror(
                "Incomplete Pizza Order",
                "Missing required item(s): " + ", ".join(missing_items),
            )
            return

        recipe_lines = []
        recipe_lines.append("FINAL PIZZA RECIPE")
        recipe_lines.append("=" * 40)
        recipe_lines.append("Build the pizza in the exact order shown below:\n")

        for index, item in enumerate(self.selected_items, start=1):
            recipe_lines.append(
                f"Step {index}: Add {item['quantity']} x {item['measure']} of {item['name']}"
            )

        recipe_lines.append(
            "\nCooking Instructions: Pizza is to be appropriately cooked until crust is cooked and topping is fully warmed."
        )

        recipe_text = "\n".join(recipe_lines)
        messagebox.showinfo("Pizza Recipe", recipe_text)


def main() -> None:
    root = tk.Tk()
    app = PizzaOrderingApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
