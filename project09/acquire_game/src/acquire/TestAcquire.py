from AutomatedDriver import AutomatedPlayer
from AutomatedDriver import AutomatedDriver
from tabulate import tabulate
class TestStats:
    def __init__(self,NumTimes):
        
        self.stats = {
            "ordered":0,
            "largest-alpha":0,
            "smallest-anti":0,
            "random":0
        }
        self.num = NumTimes
    def run(self):
        for i in range(self.num):
            player1 = AutomatedPlayer("ordered", "ordered")
            player2 = AutomatedPlayer("largest-alpha", "largest-alpha")
            player3 = AutomatedPlayer("smallest-anti", "smallest-anti")
            player4 = AutomatedPlayer("random", "random")
            playerList = [player1, player2, player3, player4]
        
            driver = AutomatedDriver(playerList)
            flag = True
            while flag:
                response = driver.gameOver()
                if response[0]:
                    flag = False
                else:
                    driver.play()
                    driver.buy()
            # winner = driver.computeWinner().name
            self.stats[driver.computeWinner().name]+=1
        self.printStats()
    def printStats(self):
        with open("result-100.txt","w") as file:
            file.write(str("While we run tests we can see that the players who goes third or fourth have better chances of winning and in general random strategy proves most successfull if every other strategies are compared at a given place. Below given are the stats when we run the game 100 times.\n"))
            file.write(str(self.stats))


if __name__ == "__main__":
    TestStats(100).run()