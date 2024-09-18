import os
import random
import yaml
import uuid
import numpy as np
from PyQt5 import QtCore
from pydub import AudioSegment
from datetime import date


class MusicEditor(QtCore.QThread):
    source_directory = ''
    result_directory = ''
    round_count = 1
    theme_count = 1
    questions_count = 1
    need_music = 1
    params = ((0, 1),)
    finished = QtCore.pyqtSignal()
    uploading = QtCore.pyqtSignal()
    pbarsig = QtCore.pyqtSignal(int)

    def __init__(self):
        QtCore.QThread.__init__(self)

    def run(self):
        file_list = os.listdir(self.source_directory)
        i = 0

        for filename in file_list:
            if filename.endswith(".mp3"):
                i += 1

                file_path = os.path.join(self.source_directory, filename)
                # Загрузка аудиофайла
                audio = AudioSegment.from_mp3(file_path)

                if len(self.params) == 2:
                    start = int(self.params[0])
                    stop = int(self.params[1])
                    max_length = (stop - start) * 1000  # Время в миллисекундах
                    if len(audio) > max_length and len(audio) > stop:
                        bot = start * 1000
                        top = stop * 1000
                        audio = audio[bot:top]
                else:
                    _len = self.params[0]
                    max_length = _len * 1000  # Время в миллисекундах
                    if len(audio) > max_length:
                        mid = len(audio) // 2
                        bot = mid - (max_length // 2)
                        top = mid + (max_length // 2)
                        audio = audio[bot:top]

                # Генерация случайной цифры
                random_digit = str(random.randint(10000, 100000))

                # Получение имени файла без расширения
                file_name_without_extension = os.path.splitext(os.path.basename(file_path))[0]

                # Создание нового имени файла с добавлением случайной цифры в начале
                new_file_name = os.path.join(self.result_directory, random_digit + " " + file_name_without_extension + ".mp3")

                # Сохранение обрезанного файла
                audio.export(new_file_name, format="mp3")

                pb_state = int(i / self.need_music * 100)
                self.pbarsig.emit(pb_state)
                if i == self.need_music:
                    break

        self.uploading.emit()

        file_list = np.asarray([f for f in os.listdir(self.result_directory) if f.endswith("mp3")][:self.need_music])
        file_list = file_list.reshape((self.round_count, self.theme_count, self.questions_count))

        with open(os.path.join(self.result_directory, "pack.yaml"), "w", encoding="utf-8") as f:
            init_data = dict()
            init_data["name"] = "pack_name"
            init_data["date"] = date.today().strftime("%d.%m.%Y")
            init_data["difficulty"] = 5
            init_data["version"] = 4
            init_data["id"] = str(uuid.uuid4())
            init_data["logo"] = ''
            init_data["tags"] = ['']
            init_data["rounds"] = [dict.fromkeys(["name"], "Round " + str(i + 1)) for i in range(self.round_count)]
            for i in range(self.round_count):
                init_data["rounds"][i]["themes"] = [dict().fromkeys(["name"], i + 1) for i in range(self.theme_count)]
                for j in range(self.theme_count):
                    init_data["rounds"][i]["themes"][j]["questions"] = [dict().fromkeys(["price"], 1)
                                                                        for k
                                                                        in range(self.questions_count)]
                    for k in range(self.questions_count):
                        init_data["rounds"][i]["themes"][j]["questions"][k]["scenario"] = [
                            dict().fromkeys(["type", "text"])]
                        init_data["rounds"][i]["themes"][j]["questions"][k]["scenario"][0]["type"] = "voice"

                        init_data["rounds"][i]["themes"][j]["questions"][k]["scenario"][0][
                            "text"] = f"@{file_list[i][j][k]}"

                        init_data["rounds"][i]["themes"][j]["questions"][k]["right"] = [f"{file_list[i][j][k][6:-4]}"]
            init_data["info"] = dict()
            init_data["info"]["authors"] = ["Created with SiPack Generator v0.1"]
            # print(init_data)
            yaml.dump(init_data, f, sort_keys=False)

        self.finished.emit()
