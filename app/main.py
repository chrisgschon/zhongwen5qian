from neo import NeoGraph
from db import Db

import pandas as pd

g = NeoGraph()

db = Db()
eng = db.create_engine()
df = pd.read_sql("""select * from words""", eng)

df['len'] = df['characters'].apply(lambda x: len(list(x)))
df['c1'] = df['characters'].apply(lambda x: list(x)[0])
df['c2'] = df['characters'].apply(lambda x: list(x)[1] if len(x) >= 2 else None)
df['p1'] = df['pinyin'].apply(lambda x: x.split(' ')[0])
df['p2'] = df['pinyin'].apply(lambda x: x.split(' ')[1] if ' ' in x else None)
df['english'] = df['english'].apply(lambda x: x.replace("'", "\\'"))
df['english_short'] = df['english'].apply(lambda x: x.split(';')[0])
df['descr'] = df.apply(lambda x: f"""{x['pinyin']} | {x['english_short']}""",axis = 1)

helper = []
chars = []
for i, c in df.iterrows():
    for h, p in zip(list(c['characters']), c['pinyin'].split(' ')):
        helper.append(f'{h} : {p}')
        chars.append(h)

truncate = True

if truncate:
    g.truncate()

g.add_characters(list(set(chars)), df)

g.create_links(df[df['len'] == 2])



