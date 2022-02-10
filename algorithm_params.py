import configparser


class AlgoParams:
    def __init__(self, filename):
        config = configparser.ConfigParser()
        config.read(filename)
        self.MIN_X = int(config["AlgorithmParams"]["MIN_X"])
        self.MIN_Y = int(config["AlgorithmParams"]["MIN_Y"])
        self.MAX_X = int(config["AlgorithmParams"]["MAX_X"])
        self.MAX_Y = int(config["AlgorithmParams"]["MAX_Y"])
        self.C = float(config["AlgorithmParams"]["C"])
        self.GENERATION_RATIO = float(config["AlgorithmParams"]["GENERATION_RATIO"])
        self.N_INIT = int(config["AlgorithmParams"]["N_INIT"])
        self.N_S = int(config["AlgorithmParams"]["N_S"])
        self.N_P = int(config["AlgorithmParams"]["N_P"])
        self.F = float(config["AlgorithmParams"]["F"])
        self.EPS = float(config["AlgorithmParams"]["EPS"])
        self.DIGITS_COUNT = int(config["AlgorithmParams"]["DIGITS_COUNT"])
        self.k = int(config["AlgorithmParams"]["k"])
        self.m = float(config["AlgorithmParams"]["m"])
        self.c_h = float(config["AlgorithmParams"]["c_h"])



params = AlgoParams("generalization_settings.ini")
