from read_data import read_data as rd
from collections import Counter
import matplotlib.pyplot as plt
from scipy.stats import chi2_contingency

ROOT_DIR = '../data'

pb_data = rd(ROOT_DIR, 'Powerball_') # Powerball USA 5/59+1/35

pb_red_balls = pb_data.iloc[:, 2:7].values.flatten()
pb_blue_balls = pb_data.iloc[:,7].values.flatten()

pb_red_freq = Counter(pb_red_balls)
pb_blue_freq = Counter(pb_blue_balls)

def disribution():
    plt.figure(figsize=(30, 12))
    plt.subplot(2, 2, 1)
    plt.bar(list(pb_red_freq.keys()), list(pb_red_freq.values()))
    plt.xticks(list(pb_red_freq.keys()))
    plt.title("PB Red Balls Frequency")
    plt.xlabel("Number")
    plt.ylabel("Frequency")
    for i, v in pb_red_freq.items():
        plt.text(i, v, str(v), ha='center', va='bottom')

    plt.subplot(2, 2, 2)
    plt.bar(list(pb_blue_freq.keys()), list(pb_blue_freq.values()))
    plt.xticks(list(pb_blue_freq.keys()))
    plt.title("PB Blue Balls Frequency")
    plt.xlabel("Number")
    plt.ylabel("Frequency")
    for i, v in pb_blue_freq.items():
        plt.text(i, v, str(v), ha='center', va='bottom')

    plt.savefig('powerball_prob_distri_histogram.png')
    # plt.show()

#  Chi-square test
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
chi_square_test(pb_red_freq, 'PowerBall Red Balls')
chi_square_test(pb_blue_freq, 'PowerBall Blue Balls')