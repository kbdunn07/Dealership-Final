import tkinter as tk
from tkinter import ttk
import threading
import DealershipModule as dealership
import RepairModule as repairshop

def openDealership():
    threading.Thread(target=dealership.main).start()
    root.withdraw()

def openRepairShop():
    threading.Thread(target=repairshop.main).start()
    root.withdraw()

root = tk.Tk()
root.title("Automotive Management System")
root.geometry("400x200")
tk.Label(root, text="Welcome! Choose a Module:", font=("Arial", 14)).pack(pady=20)
tk.Button(root, text="Dealership", width=20, height=2, command=openDealership).pack(pady=10)
tk.Button(root, text="Repair Shop", width=20, height=2, command=openRepairShop).pack(pady=10)
root.mainloop()
