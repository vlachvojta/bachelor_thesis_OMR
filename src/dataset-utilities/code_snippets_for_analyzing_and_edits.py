"""This script contains some code snippets used in the process of creting new datasets.

File is divided by "# %%" marker, which was also used
    for vscode inside run with jupyter functions.

Author: Vojtěch Vlach
Contact: xvlach22@vutbr.cz
"""

# %% Import basic libraries and shared Common library.

import numpy as np
import matplotlib.pyplot as plt
import re
import os
import sys

sys.path.append(os.path.join('..', 'dataset-utilities'))
from common import Common  # noqa: E402

# %% Clean file from extra zeros

folder = '../../../datasets/deploy/musescore/mashup_115k_with_hard_old'

# file = os.path.join(folder, 'data.SSemantic')
# file = os.path.join(folder, 'data.SSemantic.trn')
file = os.path.join(folder, 'data.SSemantic.tst')

label_lines = re.split(r'\n', Common.read_file(file))

new_label_lines = []

for line in label_lines:
    if not line:
        continue

    id, labels, _ = re.split(r'"', line)

    try:
        stave_id, zeros, _, _ = re.split(r'\s+', id)
        new_label_lines.append(f'{stave_id} {zeros} "{labels}"')
    except ValueError:
        new_label_lines.append(line)
        print(new_label_lines[-1])


output = '\n'.join(new_label_lines)
Common.write_to_file(output, f'{file}-corrected')


# %% Get image size (only widths) form all images in folder, print the first 100.

import imagesize


folder = ('../../../datasets/musescore-poly-mashup-2/6_copied_pairs_concat_all_images_but_labels_without_high_dense_41_odd_corrected')
files = [os.path.join(folder, f) for f in os.listdir(folder) if f.endswith('png')]

print(f'loaded {len(files)} images')
lens = [(f, imagesize.get(f)[0]) for f in files[:100]]
print(lens)

# %% Load lable lines from file, get labels lens and print sorted by label lens.

files = ['../../../datasets/deploy/musescore/mashup_115k_with_hard/data_hard.SSemantic.tst',
         '../../../datasets/deploy/musescore/mashup_115k_with_hard/data.SSemantic.trn',
         '../../../datasets/deploy/musescore/mashup_115k_with_hard/data.SSemantic.tst']
label_lines = []
for file in files:
    label_lines += re.split(r'\n', Common.read_file(file))

print(f'loaded {len(label_lines)} label lines')

lens = [len(line) for line in label_lines]

symbols = []

for line in label_lines:
    symbols += re.split(r'\+', line)
# len(symbols)

lens = [len(line) for line in label_lines]
print(f'MAX len of line: {max(lens)}')

sorted_lines = sorted(label_lines, key=lambda x: len(x), reverse=True)
sorted_tuples = [(re.split(r'\s+', line)[0], len(line)) for line in sorted_lines]
sorted_lens = [len(line) for line in sorted_lines]

print('Sorted tuples:')
print(sorted_tuples[:100])

plt.hist(lens, bins=30)
plt.title('Histogram počtu znaků GT ve všech sadách.')
plt.xlabel('Počet znaků v řádku GT')
plt.ylabel('')
plt.yscale('log')

plt.show()

# %% Count the number of each symbol in list. Print the first 100 most frequent symbols.
count_dict = {}
for element in symbols:
    if element in count_dict:
        count_dict[element] += 1
    else:
        count_dict[element] = 1

len(count_dict)

sorted_dict = sorted(count_dict.items(), key=lambda x: x[1], reverse=True)

print(len(sorted_dict))
sorted_dict[:100]


# %%
files = {"1003231_p01a": [12, 13], "1014031_p01": [11, 15], "1014031_p01a": [11, 14], }
# files_20 = [f for f, v in files.items() if abs(v[0] - v[1])]

for file in files:
    # file_mscz = re.split(r'\_', file)[0]
    # print(f'{file_mscz}.mscz')
    print(f'{file}.musicxml')

# %% Read lines from a files

file_trn = '../../../datasets/musescore-poly-sub-pip45/7_lmdb_images_new_new_label_format/labels.ssemantic.trn'
file_tst = '../../../datasets/musescore-poly-sub-pip45/7_lmdb_images_new_new_label_format/labels.ssemantic.tst'

data = Common.read_file(file_trn)
lines = re.split(r'\n', data)

data = Common.read_file(file_tst)
lines += re.split(r'\n', data)

# %% Get stats about lines

line_lens = np.array([len(line) for line in lines])  # if len(line) >= 600])
print(np.max(line_lens))
print(np.mean(line_lens))
print(np.min(line_lens))

# # plt.hist([diff for diff in diffs if diff <= 20], bins=10)
plt.hist(line_lens, bins=20)
plt.show()

print(len(line_lens))
for line in lines:
    if len(line) >= 600:
        print(line)


# %% extra short lines
for line in lines:
    if len(line) < 50:
        print(line)


# %% just some sort trying

listos = ['asdf/afaf', 'asdf/zzz', 'dddd/sdf']
print(f'sorted: {sorted(listos)}')

listos_pairs = []
for element in listos:
    dirs = os.path.dirname(element)
    system_id = os.path.basename(element)
    listos_pairs.append((dirs, system_id))

print(listos_pairs)
# print(sorted(listos_pairs, key=lambda list_pair: expression))
listos_pairs.sort(key=lambda x: x[1])
sorted_listos = [os.path.join(dir, file) for dir, file in listos_pairs]

print(sorted_listos)


# %% Count 999 overflow parts

# folder = 'D:/OneDrive - Vysoké učení technické v Brně/skola/BP/datasets/musescore-poly-mashup-2/6_copied_pairs_concat_all_images_but_labels_without_high_dense_41_odd_corrected/'
folder = '../../../datasets/musescore-poly-mashup-2/6_copied_pairs_concat_all_images_but_labels_without_high_dense_41_odd_corrected/'
files = os.listdir(folder)

len(files)

# overflow_999 = [file for file in file if re.match(r'\d+_p\d+_s\d{2}', file)][:100]
overflow_999 = [file for file in files if re.match(r'\d+_p\d+\S?_s\d{4}\S*', file)]

print(len(overflow_999))
overflow_999_parts = set([re.split(r'_', file)[0] for file in overflow_999])

print(overflow_999_parts)
