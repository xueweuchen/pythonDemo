import numpy as np
import matplotlib.pyplot as plt
from translate import translate


if __name__ == "__main__":
    name_list = list()
    two_list = list()
    three_list = list()
    score_list = list()
    with open('table.csv', mode = 'r', encoding = 'utf8') as fin:
        line = fin.readline().strip()
        while line:
            stat = line.split(',')
            name_list.append(stat[0])
            score_list.append(float(stat[1]))
            two_list.append(float(stat[2]))
            three_list.append(float(stat[3]))
            line = fin.readline().strip()
        
    two_array = np.array(two_list)*100
    three_array = np.array(three_list)*100
    score_array = np.array(score_list)*100
    min_score = min(score_array)
    max_score = max(score_array)
    score_array = (score_array - min_score)/(max_score - min_score)*600 + 1
    # area = np.pi * (15 * np.random.rand(N))**2 # 0 to 15 point radiuses
    
    fig, ax = plt.subplots()
    ax.scatter(two_array, three_array, s=score_array, alpha=0.5)
    ax.set_title('Top 50 scorers in NBA 13-14 season')
    ax.set_xlabel('Field goal percentage (%)')
    ax.set_ylabel('Three-point field goal percentage (%)')
    for i in range(0, len(name_list)):
        trans_name = translate(name_list[i])
        ax.text(two_array[i], three_array[i], trans_name, fontsize=8)    
    plt.show()
