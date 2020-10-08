from SQLite import WWDB
import sqlite3

class DB_enterer(WWDB):
    def __init__(self, path_txt_file, file_mode):#инициализация переменных и подключение к текстовому файлу. В аргументы - путь до файда и режми работы с файлом(r,w или др.)
        self.conn = sqlite3.connect('sql.sqlite')
        self.curs = self.conn.cursor()
        self.file_r = open(f"{path_txt_file}",f"{file_mode}")

    def reader_text(self):# метод построчного чтения файла. Каждый раз при вызове метода выводится одна строка. 1-й вызов - строка 1, второй - строка 2 и т.д.
        temp=self.file_r
        for line in temp:
            line
            return line

if __name__ == '__main__':
    text_obj = DB_enterer('mobs.txt.','r')
    #print(text_obj.reader_text())
    #print(text_obj.reader())
    #print(text_obj.reader())




