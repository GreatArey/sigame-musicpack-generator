import os
from music_editor import MusicEditor
from PyQt5.QtWidgets import QProgressBar, QGridLayout, QSpinBox, QWidget, QLabel, QLineEdit, QPushButton, QRadioButton, QGroupBox, QFileDialog, QMessageBox


class MyWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.editor = MusicEditor()

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('SiGame MusicPack Generator v0.1')
        self.setGeometry(100, 100, 500, 400)

        # Название программы сверху
        title_label = QLabel('SiGame MusicPack Generator v0.1', self)
        title_label.setStyleSheet("font-size: 20px; font-weight: bold;")

        self.msg = QMessageBox()

        # Поля для выбора директорий
        source_dir_label = QLabel('Исходная папка:', self)
        self.source_dir_edit = QLineEdit(self)
        source_dir_button = QPushButton('Выбрать', self)
        source_dir_button.clicked.connect(self.select_source_directory)

        found_tracks_text = QLabel("Найдено треков:", self)
        self.found_tracks = QLineEdit(self)
        self.found_tracks.setText("0")
        self.found_tracks.setReadOnly(True)

        target_dir_label = QLabel('Конечная папка:', self)
        self.target_dir_edit = QLineEdit(self)
        target_dir_button = QPushButton('Выбрать', self)
        target_dir_button.clicked.connect(self.select_target_directory)

        # Поля для ввода целых чисел с произвольными надписями
        int_label1 = QLabel('Количество раундов:', self)
        self.round_count = QSpinBox(self)
        self.round_count.setMinimum(1)
        self.round_count.setMaximum(10)
        self.round_count.valueChanged.connect(self.update_params)

        int_label2 = QLabel('Количество тем в раунде:', self)
        self.theme_count = QSpinBox(self)
        self.theme_count.setMinimum(1)
        self.theme_count.setMaximum(10)
        self.theme_count.valueChanged.connect(self.update_params)

        int_label3 = QLabel('Количество вопросов в теме:', self)
        self.qs_count = QSpinBox(self)
        self.qs_count.setMinimum(1)
        self.qs_count.setMaximum(10)
        self.qs_count.valueChanged.connect(self.update_params)

        # Поле для вывода текста
        need_music_text = QLabel('Требуемое количество треков:', self)
        self.need_music = QLineEdit(self)
        self.need_music.setText("1")
        self.need_music.setReadOnly(True)

        # Переключатель между вариантами "кастомный промежуток" и "центральная часть"
        self.custom_radio = QRadioButton('Кастомный промежуток в секундах', self)
        self.custom_radio.setChecked(True)
        self.custom_radio.toggled.connect(self.on_radio_toggled)

        self.central_radio = QRadioButton('Центральная часть в секундах', self)
        self.central_radio.toggled.connect(self.on_radio_toggled)

        # Поля для ввода целых чисел, связанные с переключателем
        self.custom_or_center = True
        self._from = QLabel("От:", self)
        self._to = QLabel("До:", self)
        self.from_edit = QSpinBox(self)
        self.to_edit = QSpinBox(self)
        self.from_edit.setMinimum(0)
        self.to_edit.setMinimum(self.from_edit.value() + 1)
        self.to_edit.setMaximum(self.from_edit.value() + 60)
        self.from_edit.valueChanged.connect(self.update_params)

        self.central_int_edit = QSpinBox(self)
        self.central_int_edit.setMinimum(1)
        self.central_int_edit.setMaximum(60)
        self.central_int_edit.hide()

        # Кнопка "Создать"
        self.create_button = QPushButton('Создать', self)
        self.create_button.clicked.connect(self.create_output_text)

        status = QLabel("Статус", self)
        self.status_field = QLineEdit()
        self.status_field.setText("Настройка")
        self.status_field.setReadOnly(True)

        self.pbar1 = QProgressBar(self)
        self.pbar1.setValue(0)

        # Размещение элементов на форме
        layout = QGridLayout()
        layout.addWidget(title_label, 0, 0, 1, 2)

        layout.addWidget(source_dir_label, 1, 0)
        layout.addWidget(self.source_dir_edit, 1, 1)
        layout.addWidget(source_dir_button, 2, 0, 1, 2)

        layout.addWidget(found_tracks_text, 3, 0)
        layout.addWidget(self.found_tracks, 3, 1)

        layout.addWidget(target_dir_label, 4, 0)
        layout.addWidget(self.target_dir_edit, 4, 1)
        layout.addWidget(target_dir_button, 5, 0, 1, 2)

        layout.addWidget(int_label1, 6, 0)
        layout.addWidget(self.round_count, 6, 1)

        layout.addWidget(int_label2, 7, 0)
        layout.addWidget(self.theme_count, 7, 1)

        layout.addWidget(int_label3, 8, 0)
        layout.addWidget(self.qs_count, 8, 1)

        layout.addWidget(need_music_text, 9, 0)
        layout.addWidget(self.need_music, 9, 1)

        radio_layout = QGridLayout()
        radio_layout.addWidget(self.custom_radio, 0, 0, 1, 2)
        radio_layout.addWidget(self._from, 1, 0)
        radio_layout.addWidget(self.from_edit, 1, 1)
        radio_layout.addWidget(self._to, 2, 0)
        radio_layout.addWidget(self.to_edit, 2, 1)

        radio_layout.addWidget(self.central_radio, 3, 0, 1, 2)
        radio_layout.addWidget(self.central_int_edit, 4, 0)

        group_box = QGroupBox('Выбор варианта')
        group_box.setLayout(radio_layout)

        layout.addWidget(group_box, 10, 0)
        layout.addWidget(status, 11, 0)
        layout.addWidget(self.status_field, 11, 1)
        layout.addWidget(self.pbar1, 12, 0, 1, 2)

        self.button_layout = QGridLayout()
        self.button_layout.addWidget(self.create_button, 0, 0, 1, 2)

        layout.addLayout(self.button_layout, 13, 0, 1, 2)

        self.setLayout(layout)

    def select_source_directory(self):
        directory = QFileDialog.getExistingDirectory(self, 'Выберите исходную папку')
        self.source_dir_edit.setText(directory)
        file_list = [f for f in os.listdir(directory) if f.endswith("mp3")]
        self.found_tracks.setText(str(len(file_list)))

    def select_target_directory(self):
        directory = QFileDialog.getExistingDirectory(self, 'Выберите конечную папку')
        self.target_dir_edit.setText(directory)

    def on_radio_toggled(self):
        if self.custom_radio.isChecked():
            self.custom_or_center = True
            self._from.show()
            self.from_edit.show()
            self._to.show()
            self.to_edit.show()
            self.central_int_edit.hide()
        else:
            self.custom_or_center = False
            self._from.hide()
            self.from_edit.hide()
            self._to.hide()
            self.to_edit.hide()
            self.central_int_edit.show()

    def create_output_text(self):
        self.status_field.setText("Проверка настроек.")
        if self.source_dir_edit.text() == '' or self.target_dir_edit.text() == '':
            self.msg.setIcon(QMessageBox.Critical)
            self.msg.setText("Не указаны директории")
            self.msg.setInformativeText("Начальная или конечная директории не указаны!!!")
            self.msg.setWindowTitle("Ошибка")
            self.msg.setStandardButtons(QMessageBox.Ok)

            self.msg.exec_()
            self.status_field.setText("Настройка")
            return
        if int(self.found_tracks.text()) < int(self.need_music.text()):
            self.msg.setIcon(QMessageBox.Critical)
            self.msg.setText("Мало песенок")
            self.msg.setInformativeText("С указанной исходной директории слишком мало треков!!!")
            self.msg.setWindowTitle("Ошибка")
            self.msg.setStandardButtons(QMessageBox.Ok)

            self.msg.exec_()
            self.status_field.setText("Настройка")
            return

        source_directory = self.source_dir_edit.text()
        result_directory = self.target_dir_edit.text()
        round_count = self.round_count.value()
        theme_count = self.theme_count.value()
        questions_count = self.qs_count.value()

        if self.custom_or_center:
            start_time = self.from_edit.value()
            stop_time = self.to_edit.value()
            length = stop_time - start_time
        else:
            length = self.central_int_edit.value()

        if length > 30:
            self.msg.setIcon(QMessageBox.Warning)
            self.msg.setText("Слишком длинно")
            self.msg.setInformativeText("Выбран слишком большой промежуток это может сказаться на размере пакета!!!")
            self.msg.setWindowTitle("Внимание")
            self.msg.setStandardButtons(QMessageBox.Ok)

            self.msg.exec_()

        self.create_button.setDisabled(True)
        self.status_field.setText("Обработка музыки..")

        # self.thread = QtCore.QThread()
        self.editor.source_directory = source_directory
        self.editor.result_directory = result_directory
        self.editor.round_count = round_count
        self.editor.theme_count = theme_count
        self.editor.questions_count = questions_count
        self.editor.need_music = int(self.need_music.text())

        if self.custom_or_center:
            self.editor.params = (self.from_edit.value(), self.to_edit.value())
        else:
            self.editor.params = (self.central_int_edit.value(), )

        self.editor.start()
        self.editor.pbarsig.connect(self.update_pbar)
        self.editor.uploading.connect(self.uploading)
        self.editor.finished.connect(self.on_finish)

    def update_params(self):
        self.need_music.setText(str(self.round_count.value() * self.theme_count.value() * self.qs_count.value()))
        self.to_edit.setValue(self.from_edit.value() + 1)
        self.to_edit.setMinimum(self.from_edit.value() + 1)
        self.to_edit.setMaximum(self.from_edit.value() + 60)

    def update_pbar(self, msg):
        self.pbar1.setValue(int(msg))

    def uploading(self):
        self.status_field.setText("Упаковка в пакет...")

    def on_finish(self):
        self.status_field.setText("Готово!!!")
        self.pbar1.setValue(0)
        self.create_button.setEnabled(True)
