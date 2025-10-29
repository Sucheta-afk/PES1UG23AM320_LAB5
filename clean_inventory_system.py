import json
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Global inventory
stock_data = {}

def addItem(item="default", qty=0, logs=None):
    if logs is None:
        logs = []

    # Type and value checks
    if not isinstance(item, str):
        logging.warning(f"Invalid item name type: {item}")
        return
    if not isinstance(qty, (int, float)):
        logging.warning(f"Invalid quantity type for {item}: {qty}")
        return
    if qty <= 0:
        logging.warning(f"Ignoring non-positive quantity {qty} for {item}")
        return

    stock_data[item] = stock_data.get(item, 0) + qty
    entry = f"{datetime.now()}: Added {qty} of {item}"
    logs.append(entry)
    logging.info(entry)
    return logs[-1]

def removeItem(item, qty):
    if not isinstance(qty, (int, float)) or qty <= 0:
        logging.warning(f"Invalid removal quantity {qty} for {item}")
        return
    if item not in stock_data:
        logging.warning(f"Attempted to remove non-existent item: {item}")
        return

    stock_data[item] -= qty
    if stock_data[item] <= 0:
        del stock_data[item]
        logging.info(f"{item} removed completely from inventory")
    else:
        logging.info(f"Removed {qty} of {item}, remaining {stock_data[item]}")

def getQty(item):
    return stock_data.get(item, 0)

def loadData(file="inventory.json"):
    global stock_data
    try:
        with open(file, "r") as f:
            stock_data = json.load(f)
        logging.info(f"Loaded inventory from {file}")
    except FileNotFoundError:
        logging.warning(f"No inventory file found ({file}). Starting fresh.")
        stock_data = {}
    except json.JSONDecodeError:
        logging.error("Inventory file is corrupted. Starting fresh.")
        stock_data = {}

def saveData(file="inventory.json"):
    with open(file, "w") as f:
        json.dump(stock_data, f, indent=4)
    logging.info(f"Saved inventory to {file}")

def printData():
    print("\n=== Inventory Report ===")
    if not stock_data:
        print("No items in stock.")
    else:
        for item, qty in sorted(stock_data.items()):
            print(f"{item}: {qty}")
    print("========================\n")

def checkLowItems(threshold=5):
    return [i for i, q in stock_data.items() if q < threshold]

def main():
    loadData()
    addItem("apple", 10)
    addItem("banana", 2)
    addItem(123, "ten")      # Logged and ignored
    removeItem("apple", 3)
    removeItem("orange", 1)  # Warns, doesn't crash
    print("Apple stock:", getQty("apple"))
    print("Low items:", checkLowItems())
    saveData()
    printData()

if __name__ == "__main__":
    main()
