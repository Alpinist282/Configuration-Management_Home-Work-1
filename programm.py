import os
import tarfile
import csv

class ShellEmulator:
    def __init__(self, config_path):
        self.cwd = "/" # Начальная директория
        self.fs_structure = {}
        self.load_config(config_path)
        self.load_virtual_fs()

    def load_config(self, config_path):
        with open(config_path, "r") as file:
            reader = csv.reader(file)
            next(reader)
            self.archive_path = next(reader)[1]
        if not os.path.exists(self.archive_path):
            raise FileNotFoundError(f"Архив {self.archive_path} не был найден.")
    
    def load_virtual_fs(self):
        # Распоковка файловой системы в память
        self.fs_structure = {}
        with tarfile.open(self.archive_path, "r") as tar:
            for member in tar.getmembers():
                self.fs_structure[member.name] = member
        print(f"Загружена виртуальная файловая система с {len(self.fs_structure)} объектами.")
    
    def run(self):
        print("Эмулятор Shell был запущен. Введите команду.")
        while True:
            command = input(f"shell:{self.cwd}$ ").strip()
            if command == "exit":
                print("Выходе из shell.")
                break
            self.handle_command(command)
    
    def handle_command(self, command):
        parts = command.split()
        cmd, *args = parts
        if cmd == "ls":
            self.ls()
        elif cmd == "cd":
            self.cd(args)
        elif cmd == "uname":
            self.uname()
        elif cmd == "cp":
            self.cp(args)
        else:
            print(f"Неизвестная команда: {cmd}")
    
    def ls(self):
        print("\n".join(name for name in self.fs_structure if name.startswith(self.cwd)))
    
    def uname(self):
        print("Shell Emulator v1.0")
    
    def cp(self, args):
        if len(args) < 2:
            print("Укажите исходный и целевой пути.")
            return
        src, dest = args
        if src not in self.fs_structure:
            print(f"Файл {src} не найден.")
            return
        self.fs_structure[dest] = self.fs_structure[src]
        print(f"Файл {stc} скопирован в {dest}.")

if __name__ == "__main__":
    emulator = ShellEmulator("config.csv")
    emulator.run()
