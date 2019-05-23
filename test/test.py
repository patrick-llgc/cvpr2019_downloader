# from google import google
# search_results = google.search("SoDeep: a Sorting Deep net to learn ranking loss surrogates", num_page=1)
# print(search_results)


# with open('papers/log', 'r') as f_in:
#     lines = f_in.readlines()
#
#
# lines = [x.strip() for x in lines if '%|' not in x]
# print(lines)
#
# with open('papers/lognew', 'w') as f_out:
#     for line in lines:
#         f_out.write(line + '\n')
#
with open('papers/lognew', 'r') as f_in:
    lines = [x.strip() for x in f_in.readlines()]

url_list = []
for i in range(len(lines) // 3):
    if '] ' in lines[i*3 + 2]:
        url_list.append({
            'title': lines[i*3].replace(' arxiv.org', ''),
            'url': lines[i*3+1],
            'url_title': lines[i*3 + 2].split('] ')[1]
        })
# print(url_list[100])

from fuzzywuzzy import fuzz

valid_url_list = []
for data in url_list:
    str1 = data['title'].lower()
    str2 = data['url_title'].lower()
    ratio = fuzz.ratio(str1, str2)
    # need manual screening to get this threshold
    if ratio < 70:
        # print('score', ratio)
        # print(str1)
        # print(str2)
        # print('-=-=')
        continue
    else:
        valid_url_list.append(data)


print(len(valid_url_list))
from utils.scrape import download
from tqdm import tqdm
with open('assets/available_papers_05222019.md', 'w') as f_out:
    f_out.write('# CVPR2019 papers on Arxiv (as of 05222019)\n')
    for data in tqdm(valid_url_list[:]):
        url = data['url'].replace('abs', 'pdf') + '.pdf'
        filename = 'papers/' + data['title'] + '.pdf'
        print(url)
        print(filename)
        f_out.write('- [{}]({})\n'.format(data['title'], url))

        # download(url, filename)