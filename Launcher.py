from Executer.MainApp import MainApp


if __name__ == "__main__":
    inst = MainApp()

    inst.prep()
    inst.launch()
    inst.report()
    inst.free()
