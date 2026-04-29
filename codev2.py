# Nightbreak Cafe Mobile Ordering System
# CSCI 046 final project

# Data structures used:
#   - LinkedList for the menu and the order history
#   - Queue for the kitchen line, FIFO
#   - BST to sort the menu by price
#   - merge_sort + binary_search to look up an order by number


# Linked List
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None


class LinkedList:
    def __init__(self):
        self.head = None

    def insert(self, data):
        newNode = Node(data)
        if self.head is None:
            self.head = newNode
            return
        currentNode = self.head
        while currentNode.next is not None:
            currentNode = currentNode.next
        currentNode.next = newNode


# Queue
class Queue:
    def __init__(self):
        self.items = []

    def enqueue(self, value):
        self.items.append(value)

    def dequeue(self):
        if len(self.items) == 0:
            return None
        return self.items.pop(0)

    def peek(self):
        if len(self.items) == 0:
            return None
        return self.items[0]


# Binary Search Tree
class BSTNode:
    def __init__(self, data):
        self.left = None
        self.right = None
        self.data = data

    def insert(self, data):
        if data < self.data:
            if self.left:
                self.left.insert(data)
            else:
                self.left = BSTNode(data)
        else:
            if self.right:
                self.right.insert(data)
            else:
                self.right = BSTNode(data)


class BST:
    def __init__(self):
        self.root = None

    def insert(self, data):
        if self.root:
            self.root.insert(data)
        else:
            self.root = BSTNode(data)


def inorder(node, results):
    if node is not None:
        inorder(node.left, results)
        results.append(node.data)
        inorder(node.right, results)


# Merge sort
def merge_sort(arr):
    if len(arr) > 1:
        mid = len(arr) // 2
        left = arr[:mid]
        right = arr[mid:]

        merge_sort(left)
        merge_sort(right)

        i = 0
        j = 0
        k = 0
        while i < len(left) and j < len(right):
            if left[i] < right[j]:
                arr[k] = left[i]
                i += 1
            else:
                arr[k] = right[j]
                j += 1
            k += 1
        while i < len(left):
            arr[k] = left[i]
            i += 1
            k += 1
        while j < len(right):
            arr[k] = right[j]
            j += 1
            k += 1
    return arr


# Binary search
def binary_search(arr, query):
    low = 0
    high = len(arr) - 1
    while low <= high:
        mid = (low + high) // 2
        if arr[mid] == query:
            return mid
        elif arr[mid] < query:
            low = mid + 1
        else:
            high = mid - 1
    return -1


# Money helper
def money(price):
    whole = int(price)
    cents = int(round((price - whole) * 100))
    if cents < 10:
        return "$" + str(whole) + ".0" + str(cents)
    return "$" + str(whole) + "." + str(cents)


# Cafe state
menu_list = LinkedList()
menu_tree = BST()
orders = LinkedList()
kitchen = Queue()


def load_menu():
    items = [
        {"id": 1, "name": "Latte",     "category": "Drink", "price": 5.00},
        {"id": 2, "name": "Tea",       "category": "Drink", "price": 3.50},
        {"id": 3, "name": "Croissant", "category": "Food",  "price": 4.00},
        {"id": 4, "name": "Muffin",    "category": "Food",  "price": 3.00},
        {"id": 5, "name": "Sandwich",  "category": "Food",  "price": 6.50},
    ]
    for item in items:
        menu_list.insert(item)
        menu_tree.insert((item["price"], item["id"], item["name"], item["category"]))


def count_orders():
    count = 0
    currentNode = orders.head
    while currentNode is not None:
        count += 1
        currentNode = currentNode.next
    return count


def find_menu_item(item_id):
    currentNode = menu_list.head
    while currentNode is not None:
        if currentNode.data["id"] == item_id:
            return currentNode.data
        currentNode = currentNode.next
    return None


def find_order(order_id):
    ids = []
    currentNode = orders.head
    while currentNode is not None:
        ids.append(currentNode.data["id"])
        currentNode = currentNode.next

    if len(ids) == 0:
        return None

    merge_sort(ids)
    if binary_search(ids, order_id) == -1:
        return None

    currentNode = orders.head
    while currentNode is not None:
        if currentNode.data["id"] == order_id:
            return currentNode.data
        currentNode = currentNode.next
    return None


def queue_position(order_id):
    position = 1
    for value in kitchen.items:
        if value == order_id:
            return position
        position += 1
    return None


# Display
def line():
    print("\n" + "-" * 50)


def show_menu():
    line()
    print("Nightbreak Cafe Menu")
    sorted_items = []
    inorder(menu_tree.root, sorted_items)
    for item in sorted_items:
        price = item[0]
        item_id = item[1]
        name = item[2]
        category = item[3]
        print(str(item_id) + " | " + name + " | " + category + " | " + money(price))


def show_order(order):
    line()
    print("Order:", order["id"])
    print("Customer:", order["customer"])
    print("Status:", order["status"])
    print("Subtotal:", money(order["subtotal"]))

    if order["status"] == "RECEIVED":
        position = queue_position(order["id"])
        if position is not None:
            print("Queue position:", position)
            ahead = position - 1
            if ahead == 0:
                print("Your order is next in line.")
            else:
                print("There are " + str(ahead) + " orders ahead of you.")
    elif order["status"] == "PREPARING":
        print("Your order is being prepared.")
    elif order["status"] == "READY":
        print("Your order is ready for pickup.")
    elif order["status"] == "COMPLETED":
        print("Your order has been completed.")

    print("Items:")
    for item in order["items"]:
        print("  " + str(item["quantity"]) + " x " + item["name"])


# Actions
def create_order():
    line()
    print("Create Order")
    show_menu()

    name = input("Customer name: ")
    if name == "":
        name = "Guest"

    items = []
    subtotal = 0
    while True:
        choice = input("Item number (or done): ")
        if choice == "done":
            break
        item_id = int(choice)
        quantity = int(input("Quantity: "))
        if quantity < 1:
            quantity = 1

        menu_item = find_menu_item(item_id)
        if menu_item is None:
            print("Item not found.")
        else:
            line_total = round(menu_item["price"] * quantity, 2)
            items.append({"name": menu_item["name"], "quantity": quantity, "line_total": line_total})
            subtotal += line_total

    if len(items) == 0:
        print("Cart was empty. No order made.")
        return

    new_id = count_orders() + 1
    order = {
        "id": new_id,
        "customer": name,
        "items": items,
        "subtotal": round(subtotal, 2),
        "status": "RECEIVED",
    }
    orders.insert(order)
    kitchen.enqueue(order["id"])
    show_order(order)


def track_order():
    line()
    raw = input("Order number: ")
    order = find_order(int(raw))
    if order is None:
        print("Order was not found.")
        return
    show_order(order)


def start_next_order():
    order_id = kitchen.dequeue()
    if order_id is None:
        print("No orders waiting.")
        return
    order = find_order(order_id)
    order["status"] = "PREPARING"
    show_order(order)


def advance_order():
    line()
    raw = input("Order number: ")
    order = find_order(int(raw))
    if order is None:
        print("Order was not found.")
        return
    if order["status"] == "PREPARING":
        order["status"] = "READY"
    elif order["status"] == "READY":
        order["status"] = "COMPLETED"
    else:
        print("Order must be preparing or ready.")
        return
    show_order(order)


def show_queue():
    line()
    print("Kitchen Queue")
    if len(kitchen.items) == 0:
        print("(empty)")
        return
    position = 1
    for order_id in kitchen.items:
        order = find_order(order_id)
        print(str(position) + ". Order " + str(order["id"]) + " - " + order["customer"] + " - " + order["status"])
        position += 1


# Main loop
def main():
    load_menu()
    while True:
        line()
        print("Nightbreak Cafe")
        print("1. Show menu")
        print("2. Create order")
        print("3. Track order")
        print("4. Start next order")
        print("5. Advance order")
        print("6. Show queue")
        print("0. Exit")

        choice = input("Choice: ")
        if choice == "1":
            show_menu()
        elif choice == "2":
            create_order()
        elif choice == "3":
            track_order()
        elif choice == "4":
            start_next_order()
        elif choice == "5":
            advance_order()
        elif choice == "6":
            show_queue()
        elif choice == "0":
            print("Goodbye.")
            break
        else:
            print("Try again.")


main()
