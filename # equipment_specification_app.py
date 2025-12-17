import sys
import sqlite3
from datetime import datetime, date
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class AccountingApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.create_database()
        self.load_data()
        
    def init_ui(self):
        self.setWindowTitle('Бухгалтерское приложение v1.0')
        self.setGeometry(100, 100, 1200, 700)
        
        # Центральный виджет
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Основной layout
        main_layout = QHBoxLayout()
        central_widget.setLayout(main_layout)
        
        # Левая панель (меню)
        left_panel = QWidget()
        left_panel.setMaximumWidth(200)
        left_layout = QVBoxLayout()
        
        # Кнопки меню
        self.btn_dashboard = QPushButton('📊 Дашборд')
        self.btn_transactions = QPushButton('💸 Операции')
        self.btn_invoices = QPushButton('🧾 Счета')
        self.btn_clients = QPushButton('👥 Клиенты')
        self.btn_reports = QPushButton('📈 Отчеты')
        self.btn_settings = QPushButton('⚙️ Настройки')
        
        # Стилизация кнопок
        button_style = """
            QPushButton {
                padding: 15px;
                text-align: left;
                font-size: 14px;
                border: none;
                border-radius: 5px;
                margin: 5px;
            }
            QPushButton:hover {
                background-color: #e0e0e0;
            }
        """
        
        for btn in [self.btn_dashboard, self.btn_transactions, self.btn_invoices, 
                   self.btn_clients, self.btn_reports, self.btn_settings]:
            btn.setStyleSheet(button_style)
            btn.setCursor(Qt.PointingHandCursor)
            left_layout.addWidget(btn)
        
        left_layout.addStretch()
        left_panel.setLayout(left_layout)
        
        # Правая панель (контент)
        self.content_area = QStackedWidget()
        
        # Создаем страницы
        self.dashboard_page = self.create_dashboard_page()
        self.transactions_page = self.create_transactions_page()
        self.invoices_page = self.create_invoices_page()
        self.clients_page = self.create_clients_page()
        self.reports_page = self.create_reports_page()
        self.settings_page = self.create_settings_page()
        
        # Добавляем страницы
        self.content_area.addWidget(self.dashboard_page)
        self.content_area.addWidget(self.transactions_page)
        self.content_area.addWidget(self.invoices_page)
        self.content_area.addWidget(self.clients_page)
        self.content_area.addWidget(self.reports_page)
        self.content_area.addWidget(self.settings_page)
        
        # Добавляем панели в main layout
        main_layout.addWidget(left_panel)
        main_layout.addWidget(self.content_area)
        
        # Подключаем кнопки
        self.btn_dashboard.clicked.connect(lambda: self.content_area.setCurrentIndex(0))
        self.btn_transactions.clicked.connect(lambda: self.content_area.setCurrentIndex(1))
        self.btn_invoices.clicked.connect(lambda: self.content_area.setCurrentIndex(2))
        self.btn_clients.clicked.connect(lambda: self.content_area.setCurrentIndex(3))
        self.btn_reports.clicked.connect(lambda: self.content_area.setCurrentIndex(4))
        self.btn_settings.clicked.connect(lambda: self.content_area.setCurrentIndex(5))
        
        # Статус бар
        self.statusBar().showMessage('Готово к работе')
        
    def create_dashboard_page(self):
        widget = QWidget()
        layout = QVBoxLayout()
        
        # Заголовок
        title = QLabel('📊 Дашборд')
        title.setStyleSheet("font-size: 24px; font-weight: bold; margin: 20px;")
        layout.addWidget(title)
        
        # Статистика
        stats_widget = QWidget()
        stats_layout = QHBoxLayout()
        
        # Карточки статистики
        cards = [
            ('💰 Общий доход', '500,000 ₽', '#4CAF50'),
            ('💸 Общие расходы', '250,000 ₽', '#F44336'),
            ('📈 Прибыль', '250,000 ₽', '#2196F3'),
            ('👥 Клиенты', '45', '#FF9800')
        ]
        
        for title_text, value, color in cards:
            card = self.create_stat_card(title_text, value, color)
            stats_layout.addWidget(card)
        
        stats_widget.setLayout(stats_layout)
        layout.addWidget(stats_widget)
        
        # Графики
        chart_widget = QWidget()
        chart_layout = QHBoxLayout()
        
        # Здесь можно добавить графики (используя matplotlib или pyqtgraph)
        self.income_chart_label = QLabel('График доходов')
        self.income_chart_label.setMinimumHeight(300)
        self.income_chart_label.setStyleSheet("border: 1px solid #ccc; padding: 20px;")
        self.expense_chart_label = QLabel('График расходов')
        self.expense_chart_label.setMinimumHeight(300)
        self.expense_chart_label.setStyleSheet("border: 1px solid #ccc; padding: 20px;")
        
        chart_layout.addWidget(self.income_chart_label)
        chart_layout.addWidget(self.expense_chart_label)
        chart_widget.setLayout(chart_layout)
        layout.addWidget(chart_widget)
        
        widget.setLayout(layout)
        return widget
    
    def create_stat_card(self, title, value, color):
        card = QWidget()
        card.setStyleSheet(f"""
            QWidget {{
                background-color: white;
                border-radius: 10px;
                border: 1px solid #e0e0e0;
                padding: 20px;
            }}
        """)
        
        layout = QVBoxLayout()
        
        title_label = QLabel(title)
        title_label.setStyleSheet("font-size: 14px; color: #666;")
        
        value_label = QLabel(value)
        value_label.setStyleSheet(f"font-size: 28px; font-weight: bold; color: {color};")
        
        layout.addWidget(title_label)
        layout.addWidget(value_label)
        layout.addStretch()
        
        card.setLayout(layout)
        card.setMinimumWidth(250)
        return card
    
    def create_transactions_page(self):
        widget = QWidget()
        layout = QVBoxLayout()
        
        # Заголовок и кнопки
        header_widget = QWidget()
        header_layout = QHBoxLayout()
        
        title = QLabel('💸 Операции')
        title.setStyleSheet("font-size: 24px; font-weight: bold;")
        
        self.btn_add_transaction = QPushButton('➕ Добавить операцию')
        self.btn_add_transaction.clicked.connect(self.add_transaction)
        
        header_layout.addWidget(title)
        header_layout.addStretch()
        header_layout.addWidget(self.btn_add_transaction)
        header_widget.setLayout(header_layout)
        
        # Фильтры
        filter_widget = QWidget()
        filter_layout = QHBoxLayout()
        
        self.filter_type = QComboBox()
        self.filter_type.addItems(['Все типы', 'Доход', 'Расход'])
        
        self.filter_category = QComboBox()
        self.filter_category.addItems(['Все категории', 'Зарплата', 'Аренда', 'Услуги', 'Товары'])
        
        date_filter_layout = QHBoxLayout()
        self.date_from = QDateEdit()
        self.date_from.setDate(QDate.currentDate().addMonths(-1))
        self.date_to = QDateEdit()
        self.date_to.setDate(QDate.currentDate())
        
        date_filter_layout.addWidget(QLabel('С:'))
        date_filter_layout.addWidget(self.date_from)
        date_filter_layout.addWidget(QLabel('По:'))
        date_filter_layout.addWidget(self.date_to)
        
        btn_filter = QPushButton('Фильтровать')
        btn_filter.clicked.connect(self.filter_transactions)
        
        filter_layout.addWidget(QLabel('Тип:'))
        filter_layout.addWidget(self.filter_type)
        filter_layout.addWidget(QLabel('Категория:'))
        filter_layout.addWidget(self.filter_category)
        filter_layout.addLayout(date_filter_layout)
        filter_layout.addWidget(btn_filter)
        filter_widget.setLayout(filter_layout)
        
        # Таблица операций
        self.transactions_table = QTableWidget()
        self.transactions_table.setColumnCount(6)
        self.transactions_table.setHorizontalHeaderLabels([
            'Дата', 'Описание', 'Тип', 'Категория', 'Сумма', 'Действия'
        ])
        self.transactions_table.setAlternatingRowColors(True)
        
        layout.addWidget(header_widget)
        layout.addWidget(filter_widget)
        layout.addWidget(self.transactions_table)
        
        widget.setLayout(layout)
        return widget
    
    def create_invoices_page(self):
        widget = QWidget()
        layout = QVBoxLayout()
        
        title = QLabel('🧾 Счета')
        title.setStyleSheet("font-size: 24px; font-weight: bold; margin: 20px;")
        layout.addWidget(title)
        
        # Здесь будет таблица счетов
        table = QTableWidget()
        table.setColumnCount(5)
        table.setHorizontalHeaderLabels(['Номер', 'Клиент', 'Сумма', 'Статус', 'Дата'])
        layout.addWidget(table)
        
        widget.setLayout(layout)
        return widget
    
    def create_clients_page(self):
        widget = QWidget()
        layout = QVBoxLayout()
        
        title = QLabel('👥 Клиенты')
        title.setStyleSheet("font-size: 24px; font-weight: bold; margin: 20px;")
        layout.addWidget(title)
        
        # Здесь будет таблица клиентов
        table = QTableWidget()
        table.setColumnCount(4)
        table.setHorizontalHeaderLabels(['Имя', 'Email', 'Телефон', 'Баланс'])
        layout.addWidget(table)
        
        widget.setLayout(layout)
        return widget
    
    def create_reports_page(self):
        widget = QWidget()
        layout = QVBoxLayout()
        
        title = QLabel('📈 Отчеты')
        title.setStyleSheet("font-size: 24px; font-weight: bold; margin: 20px;")
        layout.addWidget(title)
        
        # Кнопки отчетов
        reports_btns = QWidget()
        reports_layout = QHBoxLayout()
        
        reports = [
            ('📊 Отчет о прибылях и убытках', self.generate_profit_loss_report),
            ('💰 Денежный поток', self.generate_cash_flow_report),
            ('🧾 Налоговый отчет', self.generate_tax_report),
            ('📅 Ежемесячный отчет', self.generate_monthly_report)
        ]
        
        for report_name, handler in reports:
            btn = QPushButton(report_name)
            btn.clicked.connect(handler)
            btn.setMinimumHeight(80)
            reports_layout.addWidget(btn)
        
        reports_btns.setLayout(reports_layout)
        layout.addWidget(reports_btns)
        
        widget.setLayout(layout)
        return widget
    
    def create_settings_page(self):
        widget = QWidget()
        layout = QVBoxLayout()
        
        title = QLabel('⚙️ Настройки')
        title.setStyleSheet("font-size: 24px; font-weight: bold; margin: 20px;")
        layout.addWidget(title)
        
        # Настройки
        form = QFormLayout()
        
        self.setting_company_name = QLineEdit()
        self.setting_company_name.setText('Моя компания')
        
        self.setting_currency = QComboBox()
        self.setting_currency.addItems(['RUB', 'USD', 'EUR', 'KZT'])
        
        self.setting_tax_rate = QDoubleSpinBox()
        self.setting_tax_rate.setRange(0, 100)
        self.setting_tax_rate.setValue(20)
        self.setting_tax_rate.setSuffix('%')
        
        form.addRow('Название компании:', self.setting_company_name)
        form.addRow('Валюта:', self.setting_currency)
        form.addRow('Налоговая ставка:', self.setting_tax_rate)
        
        layout.addLayout(form)
        layout.addStretch()
        
        widget.setLayout(layout)
        return widget
    
    def create_database(self):
        """Создание базы данных SQLite"""
        self.conn = sqlite3.connect('accounting.db')
        self.cursor = self.conn.cursor()
        
        # Таблица операций
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date DATE NOT NULL,
                description TEXT,
                type TEXT NOT NULL,
                category TEXT,
                amount REAL NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Таблица клиентов
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS clients (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT,
                phone TEXT,
                address TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Таблица счетов
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS invoices (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                number TEXT UNIQUE NOT NULL,
                client_id INTEGER,
                amount REAL NOT NULL,
                status TEXT DEFAULT 'pending',
                issue_date DATE,
                due_date DATE,
                FOREIGN KEY (client_id) REFERENCES clients (id)
            )
        ''')
        
        self.conn.commit()
    
    def load_data(self):
        """Загрузка данных из базы"""
        # Загрузка операций
        self.cursor.execute("SELECT * FROM transactions ORDER BY date DESC")
        transactions = self.cursor.fetchall()
        
        self.transactions_table.setRowCount(len(transactions))
        for row_idx, transaction in enumerate(transactions):
            for col_idx, value in enumerate(transaction[1:6]):  # Пропускаем id
                item = QTableWidgetItem(str(value))
                self.transactions_table.setItem(row_idx, col_idx, item)
            
            # Кнопки действий
            actions_widget = QWidget()
            actions_layout = QHBoxLayout()
            actions_layout.setContentsMargins(0, 0, 0, 0)
            
            btn_edit = QPushButton('✏️')
            btn_edit.clicked.connect(lambda checked, id=transaction[0]: self.edit_transaction(id))
            btn_delete = QPushButton('🗑️')
            btn_delete.clicked.connect(lambda checked, id=transaction[0]: self.delete_transaction(id))
            
            actions_layout.addWidget(btn_edit)
            actions_layout.addWidget(btn_delete)
            actions_widget.setLayout(actions_layout)
            
            self.transactions_table.setCellWidget(row_idx, 5, actions_widget)
    
    def add_transaction(self):
        """Добавление новой операции"""
        dialog = QDialog(self)
        dialog.setWindowTitle('Добавить операцию')
        dialog.setModal(True)
        
        layout = QFormLayout()
        
        date_edit = QDateEdit()
        date_edit.setDate(QDate.currentDate())
        
        description_edit = QLineEdit()
        
        type_combo = QComboBox()
        type_combo.addItems(['Доход', 'Расход'])
        
        category_combo = QComboBox()
        category_combo.addItems(['Зарплата', 'Аренда', 'Услуги', 'Товары', 'Другое'])
        
        amount_edit = QDoubleSpinBox()
        amount_edit.setRange(0, 100000000)
        amount_edit.setPrefix('₽ ')
        
        layout.addRow('Дата:', date_edit)
        layout.addRow('Описание:', description_edit)
        layout.addRow('Тип:', type_combo)
        layout.addRow('Категория:', category_combo)
        layout.addRow('Сумма:', amount_edit)
        
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)
        
        layout.addRow(buttons)
        dialog.setLayout(layout)
        
        if dialog.exec_() == QDialog.Accepted:
            self.cursor.execute('''
                INSERT INTO transactions (date, description, type, category, amount)
                VALUES (?, ?, ?, ?, ?)
            ''', (
                date_edit.date().toString('yyyy-MM-dd'),
                description_edit.text(),
                type_combo.currentText(),
                category_combo.currentText(),
                amount_edit.value()
            ))
            self.conn.commit()
            self.load_data()
            self.statusBar().showMessage('Операция добавлена')
    
    def edit_transaction(self, transaction_id):
        """Редактирование операции"""
        print(f"Редактирование операции {transaction_id}")
    
    def delete_transaction(self, transaction_id):
        """Удаление операции"""
        reply = QMessageBox.question(
            self, 'Подтверждение',
            'Вы уверены, что хотите удалить эту операцию?',
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.cursor.execute("DELETE FROM transactions WHERE id = ?", (transaction_id,))
            self.conn.commit()
            self.load_data()
            self.statusBar().showMessage('Операция удалена')
    
    def filter_transactions(self):
        """Фильтрация операций"""
        print("Фильтрация операций")
    
    def generate_profit_loss_report(self):
        """Генерация отчета о прибылях и убытках"""
        QMessageBox.information(self, 'Отчет', 'Отчет о прибылях и убытках сгенерирован')
    
    def generate_cash_flow_report(self):
        """Генерация отчета о денежных потоках"""
        QMessageBox.information(self, 'Отчет', 'Отчет о денежных потоках сгенерирован')
    
    def generate_tax_report(self):
        """Генерация налогового отчета"""
        QMessageBox.information(self, 'Отчет', 'Налоговый отчет сгенерирован')
    
    def generate_monthly_report(self):
        """Генерация ежемесячного отчета"""
        QMessageBox.information(self, 'Отчет', 'Ежемесячный отчет сгенерирован')

def main():
    app = QApplication(sys.argv)
    
    # Установка стиля
    app.setStyle('Fusion')
    
    # Палитра
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(240, 240, 240))
    app.setPalette(palette)
    
    window = AccountingApp()
    window.show()
    
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()