# -&- coding: utf-8 -*-

"""
@TIme   : 2019/8/1 21:01
@Author : zm
@File   :build_kb v2.0.py
"""
# -*- coding: utf-8 -*-
######################################################################
#
# 构建诗歌图谱入库neo4j
#
# @build_kb 1.0.py
#
######################################################################

import py2neo
from py2neo import Graph, Node, Relationship, PropertyDict, NodeMatcher
import json

print(py2neo.__version__)



# 朝代  性别 语言 诗歌标签 固定


def build_poem_label(file_path):
     # node 标签  label
     labels_node = []
     with open(file_path, "r", encoding='UTF-8') as f_lable:
          # 读取csv文件，返回的是迭代类型
          for poem_label in f_lable.readlines():
               if poem_label != '':
                    labels_node.append(poem_label.strip('\n'))
                    graph.create(Node('风格', name=poem_label.strip('\n')))

     return list(set(labels_node))#返回去重的列表


def build_author_dynasty(file_path):
     # node 标签  dynasty
     dynastys_node = []
     with open(file_path, "r", encoding='UTF-8') as f_dynasty:
          for dynasty in f_dynasty.readlines():
               if dynasty != '':
                    dynastys_node.append(dynasty.strip('\n'))
                    graph.create(Node('朝代', name=dynasty.strip('\n')))
     return list(set(dynastys_node))#返回去重的列表

def build_author_sex(file_path):
     # node 标签  sex
     sex_node = []
     with open(file_path, "r", encoding='UTF-8') as f_sex:
          # 读取csv文件，返回的是迭代类型
          for sex in f_sex.readlines():
               if sex != '':
                    sex = sex.strip('\n')
                    sex_node.append(sex)
                    graph.create(Node('性别', name=sex))
     return list(set(sex_node))#返回去重的列表

def build_poem_language(file_path):
     # 语言码,国家码,语言，国家EN，国家CN，语言EN，语言CN  取最后一项 语言C
     # node 标签  language
     language_node = []
     country_node = []
     with open(file_path, "r", encoding='UTF-8') as f_language:
          # 读取csv文件，返回的是迭代类型
          for language in f_language.readlines():
               language = language.split(',')
               if len(language) == 8:
                    language_node.append(language[6])
                    country_node.append(language[4])
                    graph.create(Node('写作语言', name=language[6]))
                    graph.create(Node('国别', name=language[4]))

     return list(set(language_node)),list(set(country_node)) #返回去重的列表



def build_author(file_path):

     with open(file_path,'r',encoding="utf-8") as f_author:
          for author_data in f_author.readlines():
               author_data = json.loads(author_data)
               #author_name = list(author_data["author"].keys())[0]

               author_name = author_data["author"]['姓名']
               # 诗人节点
               author =Node('诗人', name=author_name, id=author_data["author"]['编号'][0])
               graph.create(author)
               author_data["author"].pop('编号')
               author_data["author"].pop('姓名')

               # 诗人其他属性
               for key in author_data["author"].keys():
                    # "性别": "男", "朝代": "唐", "写作语言": "中国"，国别：,
                    if key == "性别":
                         label_ = graph.nodes.match('性别', name=author_data["author"][key]).first()
                         if label_ != None and len(label_) == 1:
                              graph.create(Relationship(author, "性别", label_))
                    elif key == "朝代":
                         label_ = graph.nodes.match('朝代', name=author_data["author"][key]).first()
                         if label_ != None and len(label_) == 1:
                              graph.create(Relationship(author, "朝代", label_))
                    elif key == "写作语言":
                         label_ = graph.nodes.match('写作语言', name=author_data["author"][key]).first()
                         if label_ != None and len(label_) == 1:
                              graph.create(Relationship(author, "写作语言", label_))
                    else:
                         propetry_value = author_data["author"][key]
                         if type(propetry_value) == type('') and propetry_value != '':
                              propetry = Node(key, name=propetry_value)
                              graph.create(propetry)
                              graph.create(Relationship(author, key, propetry))
                         elif type(propetry_value) != type(''):
                              # json.dumps(propetry_value, ensure_ascii=False)
                              for key_min in propetry_value.keys():
                                   propetry = Node(key, name=propetry_value[key_min])
                                   graph.create(propetry)
                                   graph.create(Relationship(author, key, propetry))


               # 诗
               build_poem(author_data["poems"], author)


def build_poem(poems,author):
     for poemdata in poems:
          if poemdata:
               poem_name = poemdata['标题']
               # 诗歌节点
               poem = Node('诗歌', name=poem_name, id=poemdata['编号'])
               graph.create(poem)
               graph.create(Relationship(author, '作者', poem))
               # 诗歌正文
               poem_content = Node('诗歌正文', name=poemdata['正文'])
               graph.create(poem_content)
               graph.create(Relationship(poem, '正文', poem_content))
               # 内容标签体系
               # poem_label = Node('标签', name=poemdata['标签'])
               # 别集  a if a > b else b
               poem_list = Node('别集', name=poemdata['别集'] if '别集' in poemdata.keys() else '')
               graph.create(poem_list)
               graph.create(Relationship(poem, '别集', poem_list))
               # 情感
               poem_emotion = Node('情感', name=poemdata['情感'] if '情感' in poemdata.keys() else '')
               graph.create(poem_emotion)
               graph.create(Relationship(poem, '情感', poem_emotion))
               # 题材
               poem_ticai = Node('题材', name=poemdata['题材'] if '题材' in poemdata.keys() else '')
               graph.create(poem_ticai)
               graph.create(Relationship(poem, '题材', poem_ticai))
               # 主题
               poem_theme = Node('主题', name=poemdata['主题'] if '主题' in poemdata.keys() else '')
               graph.create(poem_theme)
               graph.create(Relationship(poem, '主题', poem_theme))

               # 体裁
               poem_form = Node('体裁', name=poemdata['体裁'] if '体裁' in poemdata.keys() else '')
               graph.create(poem_form)
               graph.create(Relationship(poem, '体裁', poem_form))

               # 诗歌译文
               poem_trans = Node('译文', name=poemdata['译文'] if '译文' in poemdata.keys() else '')
               graph.create(poem_trans)
               graph.create(Relationship(poem, '译文', poem_trans))
               # 诗歌注释
               poem_analyze = Node('注释', name=poemdata['注释'] if '注释' in poemdata.keys() else '')
               graph.create(poem_analyze)
               graph.create(Relationship(poem, '注释', poem_analyze))
               # 诗歌赏析
               poem_apre = Node('赏析', name=poemdata['赏析'] if '赏析' in poemdata.keys() else '')
               graph.create(poem_apre)
               graph.create(Relationship(poem, '赏析', poem_apre))

def init_kb():
     # 连接数据库
     # 初始化固定node
     labels_node = build_poem_label("../data/poem_label")
     dynastys_node = build_author_dynasty("../data/dynasty")
     sex_node = build_author_sex("../data/sex")
     language_node,country_node = build_poem_language("../data/language")
     build_author( '../data/final.json')


graph = Graph(host='localhost', username="neo4j", password="zdh3622278")
graph.delete_all()

init_kb()










