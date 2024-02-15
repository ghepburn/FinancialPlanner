# external deps
import os.path

# internal deps
from src.DataManager import DataManager
from Configs import Configs
from src.Logger import Logger


def main():
    configs = Configs()
    logger = Logger(configs)
    dataManager = DataManager(logger, configs)

    dataManager.getData()
    # client.get("Finances")
    # print("RAN GOOGLE CLIENT BRAH")

    # erase old data

    # download data
    # combine data
    # accept queries on data

    print("Done run.py")

if __name__ == "__main__":
  main()