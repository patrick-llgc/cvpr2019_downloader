import os
import pandas as pd

with open('assets/orals.txt', 'r') as f_in:
    files = f_in.readlines()

files = files[1:]
print(len(files))
print(files[0])

for filename in files[:1]:
    os.system('googler -n 1 "{}" arxiv.org filetype:pdf'.format(filename))
