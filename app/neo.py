from py2neo import Graph, Node, Relationship
import os
from tqdm import tqdm

NEO4J_USER = os.environ['NEO4J_USER']
NEO4J_PASSWORD = os.environ['NEO4J_PASS']
NEO4J_HOST = os.environ['NEO4J_HOST']


class NeoGraph:
    def __init__(self):
        self.g = Graph(host=NEO4J_HOST, user= NEO4J_USER, password = NEO4J_PASSWORD)

    def truncate(self):
        """Remove all nodes in the graph"""
        print("----- Truncating graph -----")
        tx = self.g.begin()
        result = tx.run('MATCH (n) DETACH DELETE n')
        tx.commit()
        return result

    def add_characters(self, character_list):
        print("----- Adding chars -----")
        tx = self.g.begin()
        for x in tqdm(character_list, total = len(character_list)):
            n = Node("Character", strokes = x)
            tx.create(n)
        tx.commit()
        self.g.run("CREATE INDEX ON :Character(strokes)")
        print("----- Done -----")

    def create_links(self, df):
        print("----- Linking two character words -----")
        for _, x in tqdm(df.iterrows(), total=df.shape[0]):
            words = f"MATCH (s1:Character {{strokes:\'{x['c1']}\'}}),(s2:Character {{strokes:\'{x['c2']}\'}}) CREATE (s1)-[:WORD {{ characters: \'{x['characters']}\' , pinyin: \'{x['pinyin']}\', english: \'{x['english']}\' }}]->(s2)"
            self.g.run(words)
        print("----- Done -----")