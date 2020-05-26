from neo import NeoGraph
from db import Db

import pandas as pd

g = NeoGraph()

db = Db()
eng = db.create_engine()
df = pd.read_sql("""select * from hsk5k""", eng)

print(df.head())



