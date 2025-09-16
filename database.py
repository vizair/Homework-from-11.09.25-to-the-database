import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3
import hashlib
from tkinter import font as tkfont

class ElegantAuthApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Авторизация")
        self.root.geometry("620x820")
        self.root.resizable(False, False)
        self.root.configure(bg='#fafafa')
        
        # Центрирование окна
        self.center_window()
        
        # Настройка стилей
        self.setup_styles()
        
        # Инициализация базы данных
        self.init_db()
        
        # Главный контейнер
        main_container = ttk.Frame(root, style='Main.TFrame')
        main_container.pack(fill='both', expand=True, padx=25, pady=25)
        
        # Логотип и заголовок
        self.setup_header(main_container)
        
        # Создание вкладок
        self.setup_notebook(main_container)
        
    def center_window(self):
        """Центрирование окна на экране"""
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (420 // 2)
        y = (self.root.winfo_screenheight() // 2) - (520 // 2)
        self.root.geometry(f"420x620+{x}+{y}")
        
    def setup_styles(self):
        """Настройка элегантных стилей"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Основные стили
        style.configure('Main.TFrame', background='#fafafa')
        style.configure('Card.TFrame', background='white', relief='flat')
        
        # Вкладки
        style.configure('Elegant.TNotebook', background='#fafafa', borderwidth=0)
        style.configure('Elegant.TNotebook.Tab', 
                       padding=(5, 3), 
                       font=('Segoe UI', 11),
                       background='#f5f5f5',
                       foreground='#666666')
        style.map('Elegant.TNotebook.Tab', 
                 background=[('selected', 'white')],
                 foreground=[('selected', '#2c3e50')])
        
        # Заголовки
        style.configure('Header.TLabel', 
                       font=('Segoe UI', 20, 'normal'), 
                       background='#fafafa', 
                       foreground='#34495e')
        style.configure('Subheader.TLabel', 
                       font=('Segoe UI', 11), 
                       background='#fafafa', 
                       foreground='#7f8c8d')
        
        # Поля ввода
        style.configure('Elegant.TEntry',
                       font=('Segoe UI', 11),
                       padding=(12, 10),
                       fieldbackground='white',
                       borderwidth=1,
                       relief='solid')
        style.map('Elegant.TEntry',
                 bordercolor=[('focus', '#95a5a6')])
        
        # Кнопки
        style.configure('Primary.TButton',
                       font=('Segoe UI', 11, 'normal'),
                       padding=(20, 12),
                       background='#ecf0f1',
                       foreground='#2c3e50',
                       borderwidth=0)
        style.map('Primary.TButton',
                 background=[('active', '#dde4e6'), ('pressed', '#ccd5d8')])
        
        style.configure('Success.TButton',
                       font=('Segoe UI', 11, 'normal'),
                       padding=(20, 12),
                       background='#ecf0f1',
                       foreground='#2c3e50',
                       borderwidth=0)
        style.map('Success.TButton',
                 background=[('active', '#dde4e6'), ('pressed', '#ccd5d8')])
        
        # Метки
        style.configure('Label.TLabel',
                       font=('Segoe UI', 10),
                       background='white',
                       foreground='#7f8c8d')
        
    def setup_header(self, parent):
        """Настройка заголовка"""
        header_frame = ttk.Frame(parent, style='Main.TFrame')
        header_frame.pack(pady=(0, 25))
        
        ttk.Label(header_frame, text="Добро пожаловать", 
                 style='Header.TLabel').pack(pady=(0, 5))
        ttk.Label(header_frame, text="Войдите в свою учетную запись", 
                 style='Subheader.TLabel').pack()
        
    def setup_notebook(self, parent):
        """Настройка вкладок"""
        self.notebook = ttk.Notebook(parent, style='Elegant.TNotebook')
        self.notebook.pack(fill='both', expand=True)
        
        # Создание фреймов для вкладок
        self.login_frame = ttk.Frame(self.notebook, style='Card.TFrame')
        self.register_frame = ttk.Frame(self.notebook, style='Card.TFrame')
        
        self.notebook.add(self.login_frame, text='Вход')
        self.notebook.add(self.register_frame, text='Регистрация')
        
        # Настройка интерфейса
        self.setup_login_frame()
        self.setup_register_frame()
        
    def init_db(self):
        """Инициализация базы данных"""
        self.conn = sqlite3.connect('users.db', check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                username TEXT PRIMARY KEY,
                password TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        self.conn.commit()
    
    def hash_password(self, password):
        """Хеширование пароля"""
        return hashlib.sha256(f'salt_{password}_secure'.encode()).hexdigest()
    
    def setup_login_frame(self):
        """Настройка интерфейса входа"""
        container = ttk.Frame(self.login_frame, style='Card.TFrame')
        container.pack(padx=30, pady=30, fill='both', expand=True)
        
        # Форма входа
        form_frame = ttk.Frame(container, style='Card.TFrame')
        form_frame.pack(fill='x')
        
        # Поле для имени пользователя
        ttk.Label(form_frame, text="Имя пользователя", style='Label.TLabel').pack(anchor='w', pady=(0, 8))
        self.login_username = ttk.Entry(form_frame, style='Elegant.TEntry')
        self.login_username.pack(pady=(0, 20), fill='x', ipady=8)
        
        # Поле для пароля
        ttk.Label(form_frame, text="Пароль", style='Label.TLabel').pack(anchor='w', pady=(0, 8))
        self.login_password = ttk.Entry(form_frame, show="•", style='Elegant.TEntry')
        self.login_password.pack(pady=(0, 30), fill='x', ipady=8)
        
        # Кнопка входа
        login_btn = ttk.Button(form_frame, text="Войти", 
                              style='Primary.TButton', command=self.login)
        login_btn.pack(fill='x', pady=(0, 10))
        
        # Связываем Enter с кнопкой входа
        self.login_password.bind('<Return>', lambda e: self.login())
        self.login_username.focus()
    
    def setup_register_frame(self):
        """Настройка интерфейса регистрации"""
        container = ttk.Frame(self.register_frame, style='Card.TFrame')
        container.pack(padx=30, pady=30, fill='both', expand=True)
        
        # Форма регистрации
        form_frame = ttk.Frame(container, style='Card.TFrame')
        form_frame.pack(fill='x')
        
        # Поле для имени пользователя
        ttk.Label(form_frame, text="Имя пользователя", style='Label.TLabel').pack(anchor='w', pady=(0, 8))
        self.register_username = ttk.Entry(form_frame, style='Elegant.TEntry')
        self.register_username.pack(pady=(0, 15), fill='x', ipady=8)
        
        # Поле для пароля
        ttk.Label(form_frame, text="Пароль", style='Label.TLabel').pack(anchor='w', pady=(0, 8))
        self.register_password = ttk.Entry(form_frame, show="•", style='Elegant.TEntry')
        self.register_password.pack(pady=(0, 15), fill='x', ipady=8)
        
        # Подтверждение пароля
        ttk.Label(form_frame, text="Подтверждение пароля", style='Label.TLabel').pack(anchor='w', pady=(0, 8))
        self.register_confirm = ttk.Entry(form_frame, show="•", style='Elegant.TEntry')
        self.register_confirm.pack(pady=(0, 30), fill='x', ipady=8)
        
        # Кнопка регистрации
        register_btn = ttk.Button(form_frame, text="Создать аккаунт", 
                                 style='Success.TButton', command=self.register)
        register_btn.pack(fill='x')
        
        # Связываем Enter с кнопкой регистрации
        self.register_confirm.bind('<Return>', lambda e: self.register())
    
    def login(self):
        """Функция авторизации"""
        username = self.login_username.get().strip()
        password = self.login_password.get()
        
        if not username or not password:
            self.show_message("Заполните все поля", "info")
            return
        
        hashed_password = self.hash_password(password)
        
        self.cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', 
                           (username, hashed_password))
        
        if self.cursor.fetchone():
            self.show_message(f"Добро пожаловать, {username}", "success")
            self.clear_login_fields()
            self.show_welcome_window(username)
        else:
            self.show_message("Неверные учетные данные", "error")
    
    def register(self):
        """Функция регистрации"""
        username = self.register_username.get().strip()
        password = self.register_password.get()
        confirm_password = self.register_confirm.get()
        
        if not all([username, password, confirm_password]):
            self.show_message("Заполните все поля", "info")
            return
        
        if len(username) < 3:
            self.show_message("Имя пользователя должно содержать минимум 3 символа", "info")
            return
        
        if len(password) < 6:
            self.show_message("Пароль должен содержать минимум 6 символов", "info")
            return
        
        if password != confirm_password:
            self.show_message("Пароли не совпадают", "info")
            return
        
        hashed_password = self.hash_password(password)
        
        try:
            self.cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', 
                              (username, hashed_password))
            self.conn.commit()
            self.show_message("Аккаунт успешно создан", "success")
            self.clear_register_fields()
            self.notebook.select(0)
            self.login_username.insert(0, username)
            self.login_password.focus()
        except sqlite3.IntegrityError:
            self.show_message("Пользователь с таким именем уже существует", "info")
    
    def show_message(self, message, msg_type="info"):
        """Показать сообщение в соответствующем стиле"""
        if msg_type == "error":
            messagebox.showerror("Ошибка", message, parent=self.root)
        elif msg_type == "success":
            messagebox.showinfo("Успех", message, parent=self.root)
        else:
            messagebox.showinfo("Информация", message, parent=self.root)
    
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
        """Показать окно приветствия"""
        welcome_window = tk.Toplevel(self.root)
        welcome_window.title("Добро пожаловать")
        welcome_window.geometry("350x250")
        welcome_window.resizable(False, False)
        welcome_window.configure(bg='white')
        welcome_window.transient(self.root)
        welcome_window.grab_set()
        
        # Центрирование
        welcome_window.update_idletasks()
        x = (welcome_window.winfo_screenwidth() // 2) - (350 // 2)
        y = (welcome_window.winfo_screenheight() // 2) - (250 // 2)
        welcome_window.geometry(f"350x250+{x}+{y}")
        
        # Содержимое
        content_frame = ttk.Frame(welcome_window, style='Card.TFrame')
        content_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        ttk.Label(content_frame, text=f"Привет, {username}!",
                 font=('Segoe UI', 16), background='white').pack(pady=(40, 10))
        
        ttk.Label(content_frame, text="Вы успешно вошли в систему",
                 font=('Segoe UI', 11), background='white', 
                 foreground='#7f8c8d').pack(pady=(0, 30))
        
        ttk.Button(content_frame, text="Продолжить", 
                  style='Primary.TButton',
                  command=lambda: [welcome_window.destroy(), self.root.destroy()]).pack()
    
    def __del__(self):
        """Закрытие соединения с БД"""
        if hasattr(self, 'conn'):
            self.conn.close()

def main():
    root = tk.Tk()
    app = ElegantAuthApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
