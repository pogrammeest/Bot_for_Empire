import sqlite3


class sqlite():
    def __init__(self, path):  # метод чтения БД и создания курсора
        self.conn = sqlite3.connect(path)
        self.curs = self.conn.cursor()  # курсор

    def enter(self, table_name,
              values):  # метод ввода любых значений в любую таблицу.В аргументы ввести имя таблицы с перечислением столбцов и значения в виде кортежа
        count = len(values)
        self.curs.execute(f"INSERT INTO {table_name} VALUES ({(count - 1) * '?,'} ?)", values)

    def read(self, argue,
             table_name):  # метод вывода любых значений из любой таблицы. В аргументы ввести выборку и имя таблицы
        self.curs.execute(f"select {argue} from {table_name}")
        rows = self.curs.fetchall()  # кусок кода
        for row in rows:  # для человечекого вывода
            print(row)  # значения, а не указания ячейки памяти

    def delete(self, table_name,
               where):  # метод удаления значения с условием.В аргументы ввести название таблицы и условие
        self.curs.execute(f"DELETE FROM {table_name} WHERE {where}")

    def update(self, table_name, coloumn_name, values, where):
        self.curs.execute(f"UPDATE {table_name} SET {coloumn_name} = '{values}' WHERE {where}")


if __name__ == '__main__':
    obj = sqlite('sql.sqlite')

    obj.enter('locations(name,max_lvl)', ('bolota', 20))  # примеры использования каждого метода
    obj.read('*', 'locations')
    obj.update('locations', 'max_lvl', '40', 'id=1')
    obj.read('*', 'locations')
    obj.delete('locations', 'id=1')
