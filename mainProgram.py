import tkinter as tk
from tkinter import messagebox

from DealershipModule import runDealershipApp
from RepairModule import runRepairApp


def launch(choice, root):
    root.destroy()
    if choice == "dealership":
        runDealershipApp()
    elif choice == "repair":
        runRepairApp()


def main():
    root = tk.Tk()
    root.title("Select Application")
    root.geometry("300x150")
    root.resizable(False, False)

    tk.Label(
        root,
        text="Select Application Mode",
        font=("Arial", 12, "bold")
    ).pack(pady=15)

    tk.Button(
        root,
        text="Dealership",
        width=20,
        command=lambda: launch("dealership", root)
    ).pack(pady=5)

    tk.Button(
        root,
        text="Repair Shop",
        width=20,
        command=lambda: launch("repair", root)
    ).pack(pady=5)

    root.mainloop()


if __name__ == "__main__":
    main()
