import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as messagebox
import sqlite3


#класс главного окна
class Main(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.init_main()
        self.db = db
        self.view_records()

    def init_main(self):
        """Инициализация основного интерфейса программы"""
        toolbar = tk.Frame(bg="#d7d8e0", bd=2)
        toolbar.pack(side=tk.TOP, fill=tk.X)

        self.add_img = tk.PhotoImage(file="./img/add.png")
        btn_open_dialog = tk.Button(
            toolbar, bg="#d7d8e0", bd=0, image=self.add_img, command=self.open_dialog
        )
        btn_open_dialog.pack(side=tk.LEFT)

        self.tree = ttk.Treeview(
            self, columns=("ID", "name", "tel", "email"), height=45, show="headings"
        )

        # Конфигурация колонок таблицы
        self.tree.column("ID", width=30, anchor=tk.CENTER)
        self.tree.column("name", width=300, anchor=tk.CENTER)
        self.tree.column("tel", width=150, anchor=tk.CENTER)
        self.tree.column("email", width=150, anchor=tk.CENTER)

        # Заголовки колонок таблицы
        self.tree.heading("ID", text="ID")
        self.tree.heading("name", text="ФИО")
        self.tree.heading("tel", text="Телефон")
        self.tree.heading("email", text="E-mail")

        self.tree.pack(side=tk.LEFT)

        # Кнопка редактирования записи
        self.update_img = tk.PhotoImage(file="./img/update.png")
        btn_edit_dialog = tk.Button(
            toolbar,
            bg="#d7d8e0",
            bd=0,
            image=self.update_img,
            command=self.open_update_dialog,
        )
        btn_edit_dialog.pack(side=tk.LEFT)

        # Кнопка удаления записи
        self.delete_img = tk.PhotoImage(file="./img/delete.png")
        btn_delete = tk.Button(
            toolbar,
            bg="#d7d8e0",
            bd=0,
            image=self.delete_img,
            command=self.delete_records,
        )
        btn_delete.pack(side=tk.LEFT)

        # Кнопка поиска записей
        self.search_img = tk.PhotoImage(file="./img/search.png")
        btn_search = tk.Button(
            toolbar,
            bg="#d7d8e0",
            bd=0,
            image=self.search_img,
            command=self.open_search_dialog,
        )
        btn_search.pack(side=tk.LEFT)
    def open_dialog(self):
        """Открытие диалогового окна для добавления записи"""
        Child()

    def records(self, name, tel, email):
        """Добавление новой записи в базу данных и обновление отображения"""
        self.db.insert_data(name, tel, email)
        self.view_records()

    def view_records(self):
        """Отображение всех записей базы данных в виде таблицы"""
        self.db.cursor.execute("SELECT * FROM db")
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert("", "end", values=row) for row in self.db.cursor.fetchall()]

    def open_update_dialog(self):
        """Открытие диалогового окна для редактирования записи"""
        UpdateEmployeeData()

    def update_records(self, name, tel, email):
        """Обновление выбранной записи в базе данных и обновление отображения"""
        self.db.cursor.execute(
            """UPDATE db SET name=?, tel=?, email=? WHERE id=?""",
            (name, tel, email, self.tree.set(self.tree.selection()[0], "#1")),
        )
        self.db.conn.commit()
        self.view_records()

    def delete_records(self):
        """Удаление выбранных записей из базы данных и обновление отображения"""
        for selection_items in self.tree.selection():
            self.db.cursor.execute(
                "DELETE FROM db WHERE id=?", (self.tree.set(selection_items, "#1"),)
            )
        self.db.conn.commit()
        self.view_records()

    def open_search_dialog(self):
        """Открытие диалогового окна для поиска записей"""
        SearchEmployee()

    def search_records(self, name):
        """Поиск записей в базе данных по заданному имени и обновление отображения"""
        name = "%" + name + "%"
        self.db.cursor.execute("SELECT * FROM db WHERE name LIKE ?", (name,)) 

        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert("", "end", values=row) for row in self.db.cursor.fetchall()]


#класс дочернего окна
class Child(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.view = app
        self.title("Добавить")
        self.geometry("400x220")
        self.resizable(False, False)

        self.grab_set()
        self.focus_set()

        label_name = tk.Label(self, text="ФИО:")
        label_name.place(x=50, y=50)
        label_select = tk.Label(self, text="Телефон:")
        label_select.place(x=50, y=80)
        label_sum = tk.Label(self, text="E-mail:")
        label_sum.place(x=50, y=110)

        self.entry_name = ttk.Entry(self)
        self.entry_name.place(x=200, y=50)
        self.entry_email = ttk.Entry(self)
        self.entry_email.place(x=200, y=80)
        self.entry_tel = ttk.Entry(self)
        self.entry_tel.place(x=200, y=110)

        self.btn_cancel = ttk.Button(self, text="Закрыть", command=self.destroy)
        self.btn_cancel.place(x=220, y=170)

        self.btn_ok = ttk.Button(self, text="Добавить")
        self.btn_ok.place(x=300, y=170)

        self.btn_ok.bind(
            "<Button-1>",
            lambda event: self.view.records(
                self.entry_name.get(), self.entry_email.get(), self.entry_tel.get()
            ),
        )


#класс окна для редактирования записи
class UpdateEmployeeData(Child):
    def __init__(self):
        super().__init__()

        self.view = app
        self.db = db
        try:
            self.default_data()

            """Инициализация окна редактирования"""
            self.title("Редактирование сотрудника")
            btn_edit = ttk.Button(self, text="Редактировать")
            btn_edit.place(x=205, y=170)
            btn_edit.bind(
                "<Button-1>",
                lambda event: self.view.update_records(
                    self.entry_name.get(), self.entry_email.get(), self.entry_tel.get()
                ),
            )
            btn_edit.bind("<Button-1>", lambda event: self.destroy(), add="+")
            self.btn_ok.destroy()
        except IndexError:
            messagebox.showerror("Error", "Пожалуйста, выберите сотрудника.")
            self.destroy()
   

    def default_data(self):
        selected_item = self.view.tree.selection()[0]
        value = self.view.tree.set(selected_item, "#1") 
        self.db.cursor.execute("SELECT * FROM db WHERE id=?", (value,))
        row = self.db.cursor.fetchone()
        self.entry_name.insert(0, row[1])
        self.entry_email.insert(0, row[2])
        self.entry_tel.insert(0, row[3])


#класс окна для поиска записей
class SearchEmployee(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.view = app
        self.title("Поиск сотрудника")
        self.geometry("300x100")
        self.resizable(False, False)

        label_search = tk.Label(self, text="Имя:")
        label_search.place(x=50, y=20)

        self.entry_search = ttk.Entry(self)
        self.entry_search.place(x=100, y=20, width=150)

        btn_cancel = ttk.Button(self, text="Закрыть", command=self.destroy) 
        btn_cancel.place(x=185, y=50)

        search_btn = ttk.Button(self, text="Найти")
        search_btn.place(x=105, y=50)
        search_btn.bind(
            "<Button-1>",
            lambda event: self.view.search_records(self.entry_search.get()),
        )
        search_btn.bind("<Button-1>", lambda event: self.destroy(), add="+")


#класс базы данных
class DB:
    def __init__(self):
        self.conn = sqlite3.connect("db.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute(
            """CREATE TABLE IF NOT EXISTS db (
                id INTEGER PRIMARY KEY,
                name TEXT,
                tel TEXT,
                email TEXT
            )"""
        )

        self.conn.commit()

    def insert_data(self, name, tel, email):
        self.cursor.execute(
            """INSERT INTO db(name, tel, email) VALUES(?, ?, ?)""", (name, tel, email)
        )
        self.conn.commit()


#действия при запуске программы
if __name__ == "__main__":
    root = tk.Tk()
    db = DB()
    app = Main(root)
    app.pack()
    root.title("Список сотрудников компании")
    root.geometry("665x450")
    root.resizable(False, False)
    root.mainloop()
