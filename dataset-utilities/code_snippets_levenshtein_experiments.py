#!/usr/bin/python3.8
"""This script contains some code snippets used as an example for coding with Levenshtein library.

File is divided by "# %%" marker, which was also used
    for vscode inside run with jupyter functions.

The first example shows how to compute Word Error using jiwer library,

The second example exports simple chart from given wer data.

Author: Vojtěch Vlach
Contact: xvlach22@vutbr.cz
"""

# %%
import jiwer
import Levenshtein
import numpy as np


def Levenshtein_list(orig: list, diff: list):
    # Count Levenshtein distance but on list of strings
    cer_list = []

    for orig, diff in zip(in_orig, in_diff):
        distance = Levenshtein.distance(orig, diff)
        cer_list.append(distance)
        print(distance)
    return np.mean(cer_list)


in_orig = ['g/4 b/6 b/ g/4 b/6 b/7 3/8 8/4 NR1/8 #/1 ',
           'g/4 b/6 b/ g/4 b/6 b/7 3/8 8/4 NR1/8 #/1 ']
in_diff = ['g/4 b/6 b/ g/4 b/6 b/7 3/8 8/4 NR1/8 #/1 ',
           'asdf asdf ']

print(f'wer: {jiwer.wer(in_orig, in_diff) * 100:.2f} %')

for orig, diff in zip(in_orig, in_diff):
    print(f'wer_ones: {jiwer.wer(orig, diff) * 100:.2f} %')
    print(f'{len(orig)}')

dist = Levenshtein_list(in_orig, in_diff)
# dist = Levenshtein.distance(in_orig[0], in_diff[0])
print(f'Levenshtein: ({dist}) {dist / len(in_orig[0]) * 100:.2f} %')



# %%  Export chart img from wer data

import numpy as np
import matplotlib.pyplot as plt


iterations_1 = [0, 500, 1000, 1500, 1750, 2000, 2250, 2500, 2750, 3000, 3250, 3500, 3750, 4250, 4500, 4750, 5000, 5500, 6000, 6500, 7000, 7500, 8000, 8500, 9000, 9500, 10000, 10500, 11000, 11500, 12000, 12500, 13000, 13500, 14000, 14500, 15000, 15500, 16000, 16500, 17000, 17500, 18000, 18500, 19000, 19500, 20000, 20500, 21000, 21500, 22000, 22500, 23000, 23500, 24000, 24500, 25000, 25500, 26000, 26500, 27000, 27500, 28000, 28500, 29000, 29500, 30000, 30500, 31000, 31500, 32000, 32500, 33000, 33500, 34000, 34500, 35000, 35500, 36000, 36500, 37000, 37500, 38000, 38500, 39000, 39500, 40000, 40500, 41000]
wers_1 = [100, 96.64373216982716, 30.54874979023326, 22.35945628461151, 21.027017956032893, 23.611344185265985, 16.38697768081893, 18.93438496392012, 16.73770766907199, 14.900151032052358, 14.900151032052358, 31.42977009565363, 13.960396039603962, 13.812720255076355, 13.624769256586674, 14.395032723611346, 14.562846115119987, 13.544218828662528, 14.645074676959222, 15.719080382614534, 13.592884712200034, 13.438496392012084, 11.74022486994462, 13.458633998993118, 12.283940258432622, 26.108407450914584, 13.215304581305586, 13.136432287296525, 12.31414666890418, 16.910555462325895, 16.56989427756335, 10.886054707165632, 11.258600436314818, 16.088269843933546, 15.601611008558484, 14.259103876489343, 15.180399395871792, 12.329249874139956, 13.992280583990603, 15.749286793086087, 11.795603289142473, 11.958382278905857, 11.636180567209262, 11.317335123342842, 12.332606141970128, 15.056217486155395, 10.998489679476423, 16.229233092800804, 11.07904010740057, 11.673099513341164, 11.423057559993287, 15.395200537002854, 13.339486491021985, 10.587346870280248, 16.84175197180735, 19.217989595569726, 13.99899311965095, 13.760698103708677, 14.208759859036752, 16.098338647424065, 13.94193656653801, 29.69457962745427, 16.063097835207248, 16.984393354589695, 13.507299882530626, 13.831179728142306, 12.095989259942943, 12.799127370364156, 15.536163785870114, 14.26078201040443, 18.237959389159254, 13.839570397717738, 12.606141970129217, 10.83571068971304, 11.339150864238965, 10.612518879006545, 18.852156402080887, 12.038932706830005, 12.377915757677464, 13.34619902668233, 9.713039100520222, 10.30542037254573, 9.791911394529283, 11.770431280416178, 11.015271018627287, 12.831011914750798, 10.182916596744422, 13.493874811209935, 10.909548581976841]

plt.title('Training VGG with agnostic encoding')
plt.plot(np.array(iterations_1), np.array(wers_1))
# plt.plot(np.array(iterations_2), np.array(wers_2))
plt.xlabel('Iteration')
plt.ylabel('Symbol error rate [%]')

plt.savefig('SAgnostic Symbol Error.png')

# %% Check if gts equal

import os

# os.listdir('../../../experiments/230213_Semantic_original/checkpoints/detective_tst_ground_truth')

path = '../../../experiments/230213_Semantic_original/checkpoints/detective_tst_ground_truth'
checkp_gt_path = os.path.join(path, 'checkpoint_gt.sort')
orig_gt_path = os.path.join(path, 'orig_gt.sort')

with open(checkp_gt_path, 'r') as f:
    check_gt = f.read()

with open(orig_gt_path, 'r') as f:
    orig_gt = f.read()


orig_gt = orig_gt.replace('\t', ' ')

with open(orig_gt_path + '.spaces', 'w+') as f:
    f.write(orig_gt)

