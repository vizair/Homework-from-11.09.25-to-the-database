import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3
import hashlib

class AuthApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Система авторизации")
        self.root.geometry("500x400")
        self.root.resizable(False, False)
        
        # Инициализация базы данных
        self.init_db()
        
        # Создание вкладок
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(pady=20, padx=20, fill='both', expand=True)
        
        # Создание фреймов для вкладок
        self.login_frame = ttk.Frame(self.notebook, padding=20)
        self.register_frame = ttk.Frame(self.notebook, padding=20)
        
        self.notebook.add(self.login_frame, text='Вход')
        self.notebook.add(self.register_frame, text='Регистрация')
        
        # Настройка интерфейса входа
        self.setup_login_frame()
        
        # Настройка интерфейса регистрации
        self.setup_register_frame()
        
    def init_db(self):
        """Инициализация базы данных"""
        self.conn = sqlite3.connect('users.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                username TEXT PRIMARY KEY,
                password TEXT NOT NULL
            )
        ''')
        self.conn.commit()
    
    def hash_password(self, password):
        """Хеширование пароля"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def setup_login_frame(self):
        """Настройка интерфейса входа"""
        # Заголовок
        login_label = ttk.Label(self.login_frame, text="Вход в систему", 
                               font=('Arial', 16, 'bold'))
        login_label.pack(pady=10)
        
        # Поле для имени пользователя
        ttk.Label(self.login_frame, text="Имя пользователя:").pack(anchor='w', pady=(10, 5))
        self.login_username = ttk.Entry(self.login_frame, width=30)
        self.login_username.pack(pady=5, fill='x')
        
        # Поле для пароля
        ttk.Label(self.login_frame, text="Пароль:").pack(anchor='w', pady=(10, 5))
        self.login_password = ttk.Entry(self.login_frame, show="*", width=30)
        self.login_password.pack(pady=5, fill='x')
        
        # Кнопка входа
        login_btn = ttk.Button(self.login_frame, text="Войти", 
                              command=self.login, width=20)
        login_btn.pack(pady=20)
        
        # Связываем Enter с кнопкой входа
        self.login_password.bind('<Return>', lambda e: self.login())
    
    def setup_register_frame(self):
        """Настройка интерфейса регистрации"""
        # Заголовок
        register_label = ttk.Label(self.register_frame, text="Регистрация", 
                                  font=('Arial', 16, 'bold'))
        register_label.pack(pady=10)
        
        # Поле для имени пользователя
        ttk.Label(self.register_frame, text="Имя пользователя:").pack(anchor='w', pady=(10, 5))
        self.register_username = ttk.Entry(self.register_frame, width=30)
        self.register_username.pack(pady=5, fill='x')
        
        # Поле для пароля
        ttk.Label(self.register_frame, text="Пароль:").pack(anchor='w', pady=(10, 5))
        self.register_password = ttk.Entry(self.register_frame, show="*", width=30)
        self.register_password.pack(pady=5, fill='x')
        
        # Подтверждение пароля
        ttk.Label(self.register_frame, text="Подтвердите пароль:").pack(anchor='w', pady=(10, 5))
        self.register_confirm = ttk.Entry(self.register_frame, show="*", width=30)
        self.register_confirm.pack(pady=5, fill='x')
        
        # Кнопка регистрации
        register_btn = ttk.Button(self.register_frame, text="Зарегистрироваться", 
                                 command=self.register, width=20)
        register_btn.pack(pady=20)
        
        # Связываем Enter с кнопкой регистрации
        self.register_confirm.bind('<Return>', lambda e: self.register())
    
    def login(self):
        """Функция авторизации"""
        username = self.login_username.get().strip()
        password = self.login_password.get()
        
        if not username or not password:
            messagebox.showwarning("Ошибка", "Пожалуйста, заполните все поля!")
            return
        
        hashed_password = self.hash_password(password)
        
        self.cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', 
                           (username, hashed_password))
        
        if self.cursor.fetchone():
            messagebox.showinfo("Успех", f"Добро пожаловать, {username}!")
            self.clear_login_fields()
            self.show_welcome_window(username)
        else:
            messagebox.showerror("Ошибка", "Неверное имя пользователя или пароль")
    
    def register(self):
        """Функция регистрации"""
        username = self.register_username.get().strip()
        password = self.register_password.get()
        confirm_password = self.register_confirm.get()
        
        if not username or not password or not confirm_password:
            messagebox.showwarning("Ошибка", "Пожалуйста, заполните все поля!")
            return
        
        if len(username) < 3:
            messagebox.showwarning("Ошибка", "Имя пользователя должно содержать минимум 3 символа!")
            return
        
        if len(password) < 4:
            messagebox.showwarning("Ошибка", "Пароль должен содержать минимум 4 символа!")
            return
        
        if password != confirm_password:
            messagebox.showwarning("Ошибка", "Пароли не совпадают!")
            return
        
        hashed_password = self.hash_password(password)
        
        try:
            self.cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', 
                              (username, hashed_password))
            self.conn.commit()
            messagebox.showinfo("Успех", "Регистрация успешна!")
            self.clear_register_fields()
            # Переключаемся на вкладку входа
            self.notebook.select(0)
        except sqlite3.IntegrityError:
            messagebox.showwarning("Ошибка", "Пользователь с таким именем уже существует!")
    
    def clear_login_fields(self):
        """Очистка полей входа"""
        self.login_username.delete(0, tk.END)
        self.login_password.delete(0, tk.END)
    
    def clear_register_fields(self):
        """Очистка полей регистрации"""
        self.register_username.delete(0, tk.END)
        self.register_password.delete(0, tk.END)
        self.register_confirm.delete(0, tk.END)
    
    def show_welcome_window(self, username):
        """Показать окно приветствия после успешного входа"""
        welcome_window = tk.Toplevel(self.root)
        welcome_window.title("Добро пожаловать!")
        welcome_window.geometry("300x200")
        welcome_window.resizable(False, False)
        
        # Центрирование окна
        welcome_window.transient(self.root)
        welcome_window.grab_set()
        
        # Содержимое окна приветствия
        ttk.Label(welcome_window, text=f"Добро пожаловать, {username}!",
                 font=('Arial', 14, 'bold')).pack(pady=30)
        
        ttk.Label(welcome_window, text="Вы успешно вошли в систему",
                 font=('Arial', 10)).pack(pady=10)
        
        ttk.Button(welcome_window, text="Выход", 
                  command=lambda: [welcome_window.destroy(), self.root.destroy()]).pack(pady=20)
    
    def __del__(self):
        """Закрытие соединения с БД при уничтожении объекта"""
        if hasattr(self, 'conn'):
            self.conn.close()

def main():
    root = tk.Tk()
    app = AuthApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
