# Nightbreak Cafe Mobile Ordering System

The program is a small mobile ordering system for a made up cafe called Nightbreak Cafe

## What the program does

It runs in the terminal. From the main menu you can:

1. Show the menu (sorted by price)
2. Create an order
3. Track an order by its order number
4. Start the next order in the kitchen line
5. Advance an order from preparing to ready to completed
6. Show the current kitchen queue

## Data structures and algorithms used

1. `LinkedList` - Stores the menu and the order history
2. `Queue` - Holds the kitchen line in FIFO order
3. `BST` + `inorder` - Sorts the menu by price
4. `merge_sort` - Sorts order numbers before lookup
5. `binary_search` - Finds an order number after sorting


## Menu

1. `Latte $5.00`
2. `Tea $3.50`
3. `Croissant $4.00`
4. `Muffin $3.00`
5. `Sandwich $6.50`

## How to run

Run the file and type in the terminal

For example: The main menu will appear. Type the number for the option you want.

## walk-through

1. Pick option `1` to see the menu sorted from cheapest to most expensive
2. Pick option `2`, type a customer name, then add items by typing the item
   number and a quantity. Type `done` when the cart is finished
3. Pick option `4` to send the next order to the kitchen
4. Pick option `5` to step that order through ready and then completed
5. Pick option `3` and type the order number to see its current status
6. Pick `0` to exit
