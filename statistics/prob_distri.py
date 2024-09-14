# number probability distribution
import numpy as np
from read_data import read_data as rd
from collections import Counter
import matplotlib.pyplot as plt
from scipy.stats import chi2_contingency

ROOT_DIR = '../data'

dlt_data = rd(ROOT_DIR, 'dlt_') # 大乐透 5/35+2/16
ssq_data = rd(ROOT_DIR, 'ssq_') # 双色球 6/33+1/16

dlt_red_balls = dlt_data['Red Balls'].values.flatten()
dlt_blue_balls = dlt_data['Blue Balls'].values.flatten()

ssq_red_balls = ssq_data['Red Balls'].values.flatten()
ssq_blue_ball = ssq_data['Blue Ball'].values.flatten()

dlt_red_balls = [list(map(int, balls.split(','))) for balls in dlt_red_balls]
dlt_blue_balls = [list(map(int, balls.split(','))) for balls in dlt_blue_balls]

ssq_red_balls = [list(map(int, balls.split(','))) for balls in ssq_red_balls]
ssq_blue_ball = ssq_blue_ball

# Count the frequency of each color number
dlt_red_freq = Counter([num for balls in dlt_red_balls for num in balls])
dlt_blue_freq = Counter([num for balls in dlt_blue_balls for num in balls])
ssq_red_freq = Counter([num for balls in ssq_red_balls for num in balls])
ssq_blue_freq = Counter(ssq_blue_ball)

dlt_red_freq = dict(sorted(dlt_red_freq.items(), key=lambda x: x[0]))
dlt_blue_freq = dict(sorted(dlt_blue_freq.items(), key=lambda x: x[0]))
ssq_red_freq = dict(sorted(ssq_red_freq.items(), key=lambda x: x[0]))
ssq_blue_freq = dict(sorted(ssq_blue_freq.items(), key=lambda x: x[0]))

# Distribution of red balls and blue balls
def disribution():
    plt.figure(figsize=(30, 12))
    plt.subplot(2, 2, 1)
    plt.bar(list(dlt_red_freq.keys()), list(dlt_red_freq.values()))
    plt.xticks(list(dlt_red_freq.keys()))
    plt.title("DLT Red Balls Frequency")
    plt.xlabel("Number")
    plt.ylabel("Frequency")
    for i, v in dlt_red_freq.items():
        plt.text(i, v, str(v), ha='center', va='bottom')

    plt.subplot(2, 2, 2)
    plt.bar(list(dlt_blue_freq.keys()), list(dlt_blue_freq.values()))
    plt.xticks(list(dlt_blue_freq.keys()))
    plt.title("DLT Blue Balls Frequency")
    plt.xlabel("Number")
    plt.ylabel("Frequency")
    for i, v in dlt_blue_freq.items():
        plt.text(i, v, str(v), ha='center', va='bottom')

    plt.subplot(2, 2, 3)
    plt.bar(list(ssq_red_freq.keys()), list(ssq_red_freq.values()))
    plt.xticks(list(ssq_red_freq.keys()))
    plt.title("SSQ Red Balls Frequency")
    plt.xlabel("Number")
    plt.ylabel("Frequency")
    for i, v in ssq_red_freq.items():
        plt.text(i, v, str(v), ha='center', va='bottom')

    plt.subplot(2, 2, 4)
    plt.bar(list(ssq_blue_freq.keys()), list(ssq_blue_freq.values()))
    plt.xticks(list(ssq_blue_freq.keys()))
    plt.title("SSQ Blue Ball Frequency")
    plt.xlabel("Number")
    plt.ylabel("Frequency")
    for i, v in ssq_blue_freq.items():
        plt.text(i, v, str(v), ha='center', va='bottom')

    plt.savefig('prob_distri_histogram.png')
    # plt.show()

# Chi-square test
def chi_square_test(freq, balls_type=''):
    observed_freq = list(freq.values())
    u_len = len(freq.keys())
    expected_freq = [sum(observed_freq) / u_len] * u_len
    chi2, p, dof, expected = chi2_contingency([observed_freq, expected_freq])
    print(f"\n{balls_type} 卡方统计量: {chi2}")
    print(f"p值: {p}")
    if p < 0.05:
        print("结果：拒绝独立性假设，历史中奖号码与当前号码可能存在关联。")
    else:
        print("结果：无法拒绝独立性假设，历史中奖号码与当前号码无显著关联。")
disribution()
chi_square_test(dlt_red_freq, 'DLT Red Balls')
chi_square_test(dlt_blue_freq, 'DLT Blue Balls')
chi_square_test(ssq_red_freq, 'SSQ Red Balls')
chi_square_test(ssq_blue_freq, 'SSQ Blue Ball')