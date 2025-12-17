import tkinter as tk
from tkinter import ttk
import csv
from tkinter import filedialog

totalSalesFinalVariableIDEK = 0  # why did i put this at the top idecatp


class Car:
    def __init__(self, make, model, year, color, price, repBool, count=1):
        self.make = make
        self.model = model
        self.year = year
        self.color = color
        self.price = price
        self.repBool = repBool
        self.count = count

    def __str__(self):
        return f'{self.year} {self.make} {self.model} ({self.color}) | ${self.price:,.2f} | Requires Repairs: {self.repBool}'


class Inventory:
    def __init__(self):
        self.cars = []
        self.sales = []

    def addCar(self, make, model, year, color, price, repBool, count):

        newCar = Car(make, model, year, color, price, repBool, count)
        self.cars.append(newCar)
        print(f'Vehicle Added: {color} {year} {make} {model} | ${price:,.2f} | Requires Repairs: {repBool}')

    def displayInv(self):
        print('\nCurrent Inventory:')
        if not self.cars:
            print('No cars in inventory.')
        else:
            for i, car in enumerate(self.cars, start=1):
                print(f'({i}) {car}')
        print()

    def sell(self, index):
        if 0 <= index < len(self.cars):
            car = self.cars[index]
            if car.count >= 1:
                totalPrice = car.price
                print(f'Sold {car.make} {car.model}(s) for ${totalPrice:,.2f}')
                self.sales.append(f"{car.year} {car.make} {car.model} ({car.color}) for ${car.price:,.2f}")
                self.cars.remove(car)
                return totalPrice
            else:
                print('Invalid number of vehicles in stock.')
                return 0
        else:
            print('Invalid car selection.')
            return 0

    def sellCar(self, make, model, year, color, price, repBoolYN):
        tempBool = (repBoolYN == 'Y')
        for car in self.cars:
            if (car.make == make and car.model == model and car.year == year and
                    car.color == color and car.price == price and car.repBool == tempBool):
                self.cars.remove(car)
                self.sales.append(car)
                print(f'Sold {car}')
                return car
        return None


class DealershipOOP:
    def __init__(self):
        self.inventory = Inventory()
        self.totalSales = 0


app = DealershipOOP()


def main():
    root = tk.Tk()
    root.title('Dealership Application')
    root.geometry('800x600')
    root.resizable(False, False)

    notebook = ttk.Notebook(root)
    notebook.pack(expand=True, fill='both')

    # Frame Creation:
    AddFrame = tk.Frame(notebook, width=500, height=500)
    InventoryFrame = tk.Frame(notebook, width=500, height=500)

    SalesFrame = tk.Frame(notebook, width=500, height=500)

    AddFrame.pack()
    InventoryFrame.pack()

    SalesFrame.pack()

    notebook.add(AddFrame, text='Add Car')
    notebook.add(InventoryFrame, text='Inventory')

    notebook.add(SalesFrame, text='Sales History')

    def saveSales():
        if not app.inventory.sales:
            tk.messagebox.showinfo('Info', 'No sales to save.')
            return
        filePath = filedialog.asksaveasfilename(defaultextension='.csv', filetypes=[('CSV Files', '*.csv')], title='Save Sales As CSV')

        if not filePath:
            return

        with open(filePath, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Make", "Model", "Year", "Color", "Price", "Needs Repairs"])
            for car in app.inventory.sales:
                rep = 'Y' if car.repBool else 'N'
                writer.writerow([car.make, car.model, car.year, car.color, f'{car.price:.2f}', rep])
            writer.writerow([f'Total Sales: ${totalSalesFinalVariableIDEK:,.2f}'])

        tk.messagebox.showinfo('Success', f'Saved Sales History to {filePath}.')

    def sellOnSelect():
        selected_item = tree.selection()
        if selected_item:
            item_id = selected_item[0]
            values = tree.item(item_id, "values")

            make = values[0]
            model = values[1]
            year = values[2]
            color = values[3]
            price = float(values[4].replace('$', '').replace(',', ''))
            repBoolYN = values[5]

            app.inventory.sellCar(make, model, year, color, price, repBoolYN)
            updateTab(None)

    def populateInventoryTree(cars):
        for item in tree.get_children():
            tree.delete(item)
        for car in cars:
            check = 'Y' if car.repBool else 'N'
            tree.insert(
                '', tk.END, text=car,
                values=(car.make, car.model, car.year, car.color, f'${car.price:,.2f}', check)
            )

    def updateTab(event):
        selectedTab = notebook.select()
        print(f'Selected tab: {selectedTab}')
        global totalSalesFinalVariableIDEK
        if selectedTab == '.!notebook.!frame2':
            populateInventoryTree(app.inventory.cars)
        elif selectedTab == '.!notebook.!frame3':
            for widget in Salestree.winfo_children():
                widget.destroy()
            for item in Salestree.get_children():
                Salestree.delete(item)
            for car in app.inventory.sales:
                if car.repBool:
                    check = 'Y'
                else:
                    check = 'N'
                Salestree.insert('', tk.END, text=car,
                                 values=(car.make, car.model, car.year, car.color, f'${car.price:,.2f}', check))
                totalSalesFinalVariableIDEK += car.price
                totalSalesLabel.config(text=f'Total Sales: ${totalSalesFinalVariableIDEK:,.2f}')

    notebook.bind('<<NotebookTabChanged>>', updateTab)

    # <--------------------Add Car Frame------------------>:
    makeVar = tk.StringVar()
    modelVar = tk.StringVar()
    yearVar = tk.StringVar()
    colorVar = tk.StringVar()
    priceVar = tk.StringVar()
    repairCheck = tk.IntVar()

    def submit():
        if repairCheck.get() == 1:
            repBool = True
        else:
            repBool = False
        make = makeVar.get()
        model = modelVar.get()
        year = yearVar.get()
        color = colorVar.get()
        price = float(priceVar.get())
        app.inventory.addCar(make, model, year, color, price, repBool, 1)
        makeEntry.delete(0, tk.END)
        modelEntry.delete(0, tk.END)
        yearEntry.delete(0, tk.END)
        colorEntry.delete(0, tk.END)
        priceEntry.delete(0, tk.END)
        repairCheckbox.deselect()

    def loadDefaults():
        dummyCars = [
            ("Toyota", "Camry", "2019", "Silver", 18500, False),
            ("Honda", "Civic", "2020", "Blue", 19500, False),
            ("Ford", "F-150", "2018", "Red", 27000, True),
            ("Chevrolet", "Malibu", "2017", "Black", 15000, False),
            ("Tesla", "Model 3", "2021", "White", 38000, False),
            ("BMW", "X5", "2019", "Gray", 45000, True),
            ("Audi", "A4", "2018", "Black", 28000, False),
            ("Nissan", "Altima", "2020", "Blue", 21000, False),
            ("Hyundai", "Tucson", "2017", "Red", 17000, True),
            ("Kia", "Sorento", "2019", "Silver", 25000, False),
            ("Subaru", "Outback", "2018", "Green", 23000, False),
            ("Volkswagen", "Jetta", "2016", "White", 12000, True),
            ("Dodge", "Charger", "2020", "Black", 30000, False),
            ("Jeep", "Wrangler", "2019", "Yellow", 34000, True),
            ("Mazda", "CX-5", "2021", "Red", 29000, False)
        ]

        for make, model, year, color, price, repBool in dummyCars:
            app.inventory.addCar(make, model, year, color, price, repBool, 1)

    makeLabel = tk.Label(AddFrame, text='Make: ', font=('calibre', 10, 'bold'))
    makeEntry = tk.Entry(AddFrame, textvariable=makeVar, font=('calibre', 10, 'normal'))

    modelLabel = tk.Label(AddFrame, text='Model: ', font=('calibre', 10, 'bold'))
    modelEntry = tk.Entry(AddFrame, textvariable=modelVar, font=('calibre', 10, 'normal'))

    yearLabel = tk.Label(AddFrame, text='Year: ', font=('calibre', 10, 'bold'))
    yearEntry = tk.Entry(AddFrame, textvariable=yearVar, font=('calibre', 10, 'normal'))

    colorLabel = tk.Label(AddFrame, text='Color: ', font=('calibre', 10, 'bold'))
    colorEntry = tk.Entry(AddFrame, textvariable=colorVar, font=('calibre', 10, 'normal'))

    priceLabel = tk.Label(AddFrame, text='Price: $', font=('calibre', 10, 'bold'))
    priceEntry = tk.Entry(AddFrame, textvariable=priceVar, font=('calibre', 10, 'normal'))

    repairCheckbox = tk.Checkbutton(AddFrame, text='Requires Repairs', variable=repairCheck)

    submitButton = tk.Button(AddFrame, text='Submit', command=submit)
    loadDefaultsButton = tk.Button(AddFrame, text='Load Defaults: Debugging Only',
                                   bg='lightgray', command=loadDefaults)
    loadDefaultsButton.grid(row=8, column=5, pady=10)

    makeLabel.grid(row=1, column=4)
    makeEntry.grid(row=1, column=5)

    modelLabel.grid(row=2, column=4)
    modelEntry.grid(row=2, column=5)

    yearLabel.grid(row=3, column=4)
    yearEntry.grid(row=3, column=5)

    colorLabel.grid(row=4, column=4)
    colorEntry.grid(row=4, column=5)

    priceLabel.grid(row=5, column=4)
    priceEntry.grid(row=5, column=5)
    repairCheckbox.grid(row=6, column=5)

    submitButton.grid(row=7, column=5)

    # <--------------------Inventory Frame------------------>:

    SearchFrame = tk.LabelFrame(InventoryFrame, text="Search / Filter Cars")
    SearchFrame.pack(fill="x", padx=8, pady=5)

    makeSearch = tk.StringVar()
    modelSearch = tk.StringVar()
    yearSearch = tk.StringVar()
    colorSearch = tk.StringVar()
    repairSearch = tk.StringVar(value="Any")

    tk.Label(SearchFrame, text="Make").grid(row=0, column=0)
    tk.Entry(SearchFrame, textvariable=makeSearch, width=10).grid(row=0, column=1)

    tk.Label(SearchFrame, text="Model").grid(row=0, column=2)
    tk.Entry(SearchFrame, textvariable=modelSearch, width=10).grid(row=0, column=3)

    tk.Label(SearchFrame, text="Year").grid(row=0, column=4)
    tk.Entry(SearchFrame, textvariable=yearSearch, width=8).grid(row=0, column=5)

    tk.Label(SearchFrame, text="Color").grid(row=0, column=6)
    tk.Entry(SearchFrame, textvariable=colorSearch, width=10).grid(row=0, column=7)

    tk.Label(SearchFrame, text="Needs Repairs").grid(row=0, column=8)
    ttk.Combobox(
        SearchFrame,
        textvariable=repairSearch,
        values=["Any", "Yes", "No"],
        width=8,
        state="readonly"
    ).grid(row=0, column=9)

    columns = ("Make", "Model", "Year", 'Color', 'Price', 'Needs Repairs')
    tree = ttk.Treeview(InventoryFrame, columns=columns, show="headings", selectmode="browse")
    for col in columns:
        tree.heading(col, text=col)
        if col == "Make":
            tree.column(col, width=100, anchor="center")
        elif col == "Model":
            tree.column(col, width=100, anchor="center")
        elif col == 'Needs Repairs':
            tree.column(col, width=50, anchor='center')
        else:
            tree.column(col, width=100, anchor="center")
    tree.pack(fill="both", expand=True, padx=8, pady=6)

    sellButton = tk.Button(InventoryFrame, text='SELL', bg='red', height=2, width=10, command=sellOnSelect)
    sellButton.pack(padx=10, pady=10, side=tk.LEFT, anchor='w')

    def applyFilters():
        filteredCars = []
        for car in app.inventory.cars:
            if makeSearch.get() and makeSearch.get().lower() not in car.make.lower(): continue
            if modelSearch.get() and modelSearch.get().lower() not in car.model.lower(): continue
            if yearSearch.get() and yearSearch.get() != str(car.year): continue
            if colorSearch.get() and colorSearch.get().lower() not in car.color.lower(): continue
            if repairSearch.get() == "Yes" and not car.repBool: continue
            if repairSearch.get() == "No" and car.repBool: continue
            filteredCars.append(car)
        populateInventoryTree(filteredCars)

    def resetFilters():
        makeSearch.set("")
        modelSearch.set("")
        yearSearch.set("")
        colorSearch.set("")
        repairSearch.set("Any")
        populateInventoryTree(app.inventory.cars)

    tk.Button(SearchFrame, text="Search", command=applyFilters).grid(row=0, column=10, padx=5)
    tk.Button(SearchFrame, text="Reset", command=resetFilters).grid(row=0, column=11)

    # <--------------------Sales Frame------------------>:
    Salestree = ttk.Treeview(SalesFrame, columns=columns, show="headings", selectmode="browse")
    for col in columns:
        Salestree.heading(col, text=col)
        if col == "Make":
            Salestree.column(col, width=100, anchor="center")
        elif col == "Model":
            Salestree.column(col, width=100, anchor="center")
        elif col == 'Needs Repairs':
            Salestree.column(col, width=50, anchor='center')
        else:
            Salestree.column(col, width=100, anchor="center")
    Salestree.pack(fill="both", expand=True, padx=8, pady=6)

    totalSalesLabel = tk.Label(SalesFrame, text=f'Total Sales: ${totalSalesFinalVariableIDEK:,.2f}')
    totalSalesLabel.pack(padx=10, pady=10, anchor='center')

    saveCSVButton = tk.Button(SalesFrame, text="Save Sales as CSV", command=saveSales)
    saveCSVButton.pack(pady=10)

    root.mainloop()


if __name__ == '__main__':
    main()
