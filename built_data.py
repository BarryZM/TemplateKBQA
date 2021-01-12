import py2neo
import json
from py2neo import Graph, Node, Relationship, PropertyDict, NodeMatcher
graph = Graph("http://localhost:7474", username="neo4j", password='zdh3622278')

def build_author(file_path):
    with open(file_path, 'r', encoding="utf-8") as f_author:
        for author_data in f_author.readlines():
            author_data = json.loads(author_data)
            # author_name = list(author_data["author"].keys())[0]
            author_name = author_data["writer"]['姓名']
            author_zi = author_data["writer"]['字']
            author_hao = author_data["writer"]['号']
            author_tname = author_data["writer"]['别称']
            author_time = author_data["writer"]['所属朝代']
            author_poem = author_data["writer"]['代表作']
            author_intro = author_data["writer"]['评价']
            # 诗人节点
            author = Node('writer', name=author_name)
            zi  = Node('zi', name=author_zi)
            hao = Node('hao', name=author_hao)
            time = Node('time', name=author_time)
            tname =  Node('tname',name=author_tname)
            poem = Node('poem', name=author_poem)
            intro = Node('intro', name=author_intro)
            graph.create(author)
            graph.create(zi)
            graph.create(hao)
            graph.create(time)
            graph.create(tname)
            graph.create(poem)
            graph.create(intro)

            # 诗人其他属性
            for key in author_data["writer"].keys():
                if key == "字":
                    #label_ = graph.nodes.match('tname', name=key).first()
                    #print(label_)
                    graph.create(Relationship(author, "字", zi))
                if key == "号":
                    graph.create(Relationship(author, "号", hao))
                if key == "别称":
                    graph.create(Relationship(author, "别称", tname))
                if key == "所属朝代":
                    graph.create(Relationship(author, "所属朝代", time))
                if key == "代表作":
                    graph.create(Relationship(author, "代表作", poem))
                if key == "评价":
                    graph.create(Relationship(author, "评价", intro))

build_author( 'data.json')