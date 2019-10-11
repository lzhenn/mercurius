import random
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('Agg')
class _player:
    
    def __init__(self):
        self.inifund=100
        self.fund_curve=np.array([self.inifund])

    def play_round(self):
        bet_result=random.randint(0,1)
        if bet_result:
            self.fund_curve=np.append(self.fund_curve, self.fund_curve[-1]+1)
        else:
            self.fund_curve=np.append(self.fund_curve, self.fund_curve[-1]-1)


play_round=1000


player_list=[]

for i in range(0,100):
    player_list.append(_player())
    
for itm_player in player_list:
    for i in range(0,play_round):
        itm_player.play_round()
    plt.plot(itm_player.fund_curve, '-', color='gray')

plt.savefig('../../../fig/sandbox.png')
