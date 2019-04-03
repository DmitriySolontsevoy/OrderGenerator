from Executer.MainApp import MainApp
import os.path


if __name__ == "__main__":
    inst = MainApp(os.path.dirname(__file__))

    inst.prep()
    inst.exec()
    inst.report()
    inst.free()
