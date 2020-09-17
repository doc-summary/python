# retrieves various dictionaries for use with atb.py
# uses requests lib (pip install requests)

import requests
import zipfile
import os
from io import BytesIO

def get_cedict(ret='sf'):
    with requests.Session() as sess:
        resp = sess.get('https://www.mdbg.net/chinese/export/cedict/cedict_1_0_ts_utf-8_mdbg.zip')

        f = BytesIO()

        with f:
            f.write(resp.content)

            with zipfile.ZipFile(f, 'r') as z:
                z.extractall()

    with open('cedict_ts.u8', 'r') as f:
        all_wds = [l.strip().split('/') for l in f.readlines()]
        lf = [wd.split()[0].strip() for wd in all_wds[1:]]
        sf = [wd.split()[1].strip() for wd in all_wds[1:]]
        
    if ret == 'sf':
        return sf
    elif ret == 'lf':
        return lf
    elif ret == 'all':
        return all_wds[1:]
    else:
        return False
