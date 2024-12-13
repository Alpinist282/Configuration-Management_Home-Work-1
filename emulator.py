import os
import sys
import tarfile
from io import BytesIO
from pathlib import Path
from typing import List

class EmulatorShell:
    def __init__(self):
        self.current_dir = "/"
        self.vfs_root = None
        self.load_vfs()
    
    def load_vfs(self):
        """Загрузка виртуальной файловой системы."""
        with open("config.csv") as f:
            vfs_path = f.read().strip()  # Предполагаем, что путь к файлу VFS находится в первой строке CSV-файла
        
        if not os.path.exists(vfs_path):
            print(f"Файл {vfs_path} не найден.")
            sys.exit(1)
        
        try:
            self.vfs_root = tarfile.open(vfs_path, 'r')
        except Exception as e:
            print(f"Произошла ошибка при открытии архива: {e}")
            sys.exit(1)
    
    def execute_command(self, command: str):
        args = command.split()
        cmd_name = args[0]
        
        if cmd_name == "ls":
            self.ls(args[1:])
        elif cmd_name == "cd":
            self.cd(args[1])
        elif cmd_name == "exit":
            self.exit()
        elif cmd_name == "uname":
            self.uname()
        elif cmd_name == "cp":
            self.cp(args[1], args[2])
        else:
            print(f"Неизвестная команда: {cmd_name}")
    
    def ls(self, paths: List[str]):
        """Вывод содержимого директории."""
        for path in paths:
            members = self.vfs_root.getmembers(path)
            for member in members:
                print(member.name)
    
    def cd(self, dir: str):
        """Переход в другую директорию."""
        if dir.startswith("/"):
            self.current_dir = dir
        else:
            self.current_dir += "/" + dir
        print(f"Текущая директория: {self.current_dir}")
    
    def exit(self):
        """Выход из эмулятора."""
        print("Выход из эмулятора...")
        sys.exit(0)

    def uname(self):
        """Вывод информации об операционной системе."""
        print("Linux")
    
    def cp(self, source: str, dest: str):
        """Копирование файлов."""
        if not self.vfs_root.getmember(source):
            print(f"Файл {source} не существует.")
            return
        
        if not self.vfs_root.getmember(dest):
            print(f"Директория назначения {dest} не существует.")
            return
        
        # Здесь должна быть логика копирования внутри VFS
        print(f"Копируем {source} в {dest}")


if __name__ == "__main__":
    shell = EmulatorShell()
    while True:
        command = input(f"{shell.current_dir}> ")
        shell.execute_command(command)