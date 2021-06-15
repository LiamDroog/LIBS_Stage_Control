import tkinter as tk
from StageClass import TwoAxisStage


class StageLauncher:
    def __init__(self):
        # Stuff for launching stage
        pass


if __name__ == '__main__':
    TwoAxisStage('COM4', 115200, 'Config/startup.txt').start()
    #StageLauncher()
