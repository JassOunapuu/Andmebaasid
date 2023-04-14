import sqlite3
import tkinter as tk
from tkinter import ttk

# ühendan andmebaasiga
conn = sqlite3.connect('database.db')
c = conn.cursor()

# Teen tabeli, kui juba olemas pole
c.execute('''CREATE TABLE IF NOT EXISTS inimesed
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
             nimi TEXT,
             aaddress TEXT,
             telo TEXT)''')

# Lisan info
c.execute("INSERT INTO inimesed (nimi, aaddress, telo) VALUES ('Ülle Doos', 'kooli 7', '+372 1234 1234')")
c.execute("INSERT INTO inimesed (nimi, aaddress, telo) VALUES ('Jann Uuspõld', 'aafrika tn 13', '+372 1623 5678')")
c.execute("INSERT INTO inimesed (nimi, aaddress, telo) VALUES ('Rita Kurk', 'tallinna mnt 23', '+372 4321 9012')")

# salvestan muudatused
conn.commit()

# teen tkinteri akna
root = tk.Tk()
root.title("inimeste andmed")

# loon andmete kuvamiseks treeview
tree = ttk.Treeview(root, columns=("nimi", "aaddress", "telo"))
tree.heading("#0", text="ID")
tree.column("#0", width=50)
tree.heading("nimi", text="Nimi")
tree.column("nimi", width=150)
tree.heading("aaddress", text="Aaddress")
tree.column("aaddress", width=200)
tree.heading("telo", text="Telo")
tree.column("telo", width=100)
tree.grid(row=0, column=0, padx=5, pady=5)

# funktsioon andmete kuvamiseks treeview's
def show_data():
    
    # kustutan olemasolevad andmed
    for child in tree.get_children():
        tree.delete(child)
        
    # loen andmed andmebaasist
    c.execute("SELECT * FROM inimesed")
    data = c.fetchall()
    
    # kuvan andmed treeview's
    for row in data:
        tree.insert("", "end", text=row[0], values=(row[1], row[2], row[3]))

# funktsioon rohkema info lisamiseks andmebaasi
def add_entry():
    name = name_entry.get()
    address = address_entry.get()
    phone = phone_entry.get()
    c.execute("INSERT INTO inimesed (nimi, aaddress, telo) VALUES (?, ?, ?)", (name, address, phone))
    conn.commit()
    show_data()
    name_entry.delete(0, tk.END)
    address_entry.delete(0, tk.END)
    phone_entry.delete(0, tk.END)

# funktsioon valitud rea kustutamiseks andmebaasist
def delete_entry():
    selected = tree.focus()
    if selected:
        item_id = int(tree.item(selected)["text"])
        c.execute("DELETE FROM inimesed WHERE id=?", (item_id,))
        conn.commit()
        show_data()

# loon sildid ja tekstiväljad uue kirje lisamiseks
name_label = tk.Label(root, text="Nimi")
name_label.grid(row=1, column=0, padx=5, pady=5)
name_entry = tk.Entry(root)
name_entry.grid(row=1, column=1, padx=5, pady=5)

address_label = tk.Label(root, text="Aaddress")
address_label.grid(row=2, column=0, padx=5, pady=5)
address_entry = tk.Entry(root)
address_entry.grid(row=2, column=1, padx=5, pady=5)

phone_label = tk.Label(root, text="telo")
phone_label.grid(row=3, column=0, padx=5, pady=5)
phone_entry = tk.Entry(root)

phone_entry.grid(row=3, column=1, padx=5, pady=5)

add_button = tk.Button(root, text="Add", command=add_entry)
add_button.grid(row=4, column=0, padx=5, pady=5)

delete_button = tk.Button(root, text="Delete", command=delete_entry)
delete_button.grid(row=4, column=1, padx=5, pady=5)


show_data()

root.mainloop()

conn.close()