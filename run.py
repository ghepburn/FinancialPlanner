# external deps
import os.path

# internal deps
from src.DataManager import DataManager
from Configs import Configs
from src.Logger import Logger


def main():
    logger = Logger()
    configs = Configs(logger)
    # dataManager = DataManager(logger, configs)

    # dataManager.deleteData()
    # dataManager.createDirectory()
    # dataManager.downloadData()
    # client.get("Finances")
    # print("RAN GOOGLE CLIENT BRAH")

    # erase old data

    # download data
    # combine data
    # accept queries on data

    print("Done run.py")

if __name__ == "__main__":
  main()