# ruff: noqa: F403, F405
# region imports
from AlgorithmImports import *
# endregion


class LiveCommandsTestAlgorithm(QCAlgorithm):

    def initialize(self):
        self.add_command(MyCommand)

    def on_command(self, data):
        self.log(f'Generic command. data.text: {data.text}')


class MyCommand(Command):
    text = None
    number = None
    parameters = {}

    def run(self, algorithm):
        parameters = {kvp.key: kvp.value for kvp in self.parameters}
        algorithm.log(f"Encapsulated command. text: {self.text}; number: {self.number}; parameters: {parameters}")
        return True
