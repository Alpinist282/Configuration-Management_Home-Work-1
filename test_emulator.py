import unittest
from emulator import EmulatorShell


class TestEmulator(unittest.TestCase):
    def setUp(self):
        self.shell = EmulatorShell()
    
    def test_ls(self):
        self.shell.execute_command("ls /")
        self.assertTrue(True)  # Добавьте свои проверки

    def test_cd(self):
        self.shell.execute_command("cd /home")
        self.assertEqual(self.shell.current_dir, "/home")

    def test_exit(self):
        with self.assertRaises(SystemExit):
            self.shell.execute_command("exit")

    def test_uname(self):
        output = self.shell.uname()
        self.assertEqual(output, "Linux")

    def test_cp(self):
        self.shell.execute_command("cp file.txt /tmp/file.txt")
        self.assertTrue(True)  # Добавьте свои проверки

if __name__ == '__main__':
    unittest.main()