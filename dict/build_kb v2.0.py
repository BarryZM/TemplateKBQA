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
import os

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

     language_node = list(set(language_node))
     country_node = list(set(country_node))

     with open('写作语言.txt', 'w', encoding='utf-8') as f:
          for i in language_node:
               f.write(i+'\n')

     return language_node, country_node#返回去重的列表



def build_author(file_path):
     try:
          os.remove('诗歌.txt')
          os.remove('诗歌正文.txt')
          os.remove('别集.txt')
          os.remove('情感.txt')
          os.remove('题材.txt')
          os.remove('主题.txt')
          os.remove('体裁.txt')
          os.remove('译文.txt')
          os.remove('注释.txt')
          os.remove('赏析.txt')
     except FileNotFoundError:
          pass

     author_name_save = []  # 诗人姓名
     other_save = {}

     with open(file_path,'r',encoding="utf-8") as f_author:
          for author_data in f_author.readlines():
               author_data = json.loads(author_data)
               #author_name = list(author_data["author"].keys())[0]

               author_name = author_data["author"]['姓名']
               author_name_save.append(author_name)
               # 诗人节点
               author =Node('诗人', name=author_name, id=author_data["author"]['编号'][0])
               graph.create(author)
               author_data["author"].pop('编号')
               author_data["author"].pop('姓名')
               # 诗人其他属性
               for key in author_data["author"].keys():
                    # "性别": "男", "朝代": "唐", "写作语言": "中国"，国别：,
                    if key == "性别":
                         label_ = graph.nodes.match('性别', name=key).first()
                         # print("label_: ", end='')
                         # print(label_)
                         if label_ != None and len(label_) == 1:
                              graph.create(Relationship(author, "性别", label_))
                    elif key == "朝代":
                         label_ = graph.nodes.match('朝代', name=key).first()
                         if label_ != None and len(label_) == 1:
                              graph.create(Relationship(author, "朝代", label_))
                    elif key == "写作语言":
                         label_ = graph.nodes.match('写作语言', name=key).first()
                         if label_ != None and len(label_) == 1:
                              graph.create(Relationship(author, "写作语言", label_))
                    else:
                         propetry_value = author_data["author"][key]
                         if type(propetry_value) == type('') and propetry_value != '':  # 值是字符串
                              if key not in other_save:
                                   other_save[key] = []
                              other_save[key].append(propetry_value)
                              propetry = Node(key, name=propetry_value)
                              graph.create(propetry)
                              graph.create(Relationship(author, key, propetry))
                         elif type(propetry_value) != type(''):  # 值是一些字典信息，不方便直接用于对话，先不处理
                              # json.dumps(propetry_value, ensure_ascii=False)
                              for key_min in propetry_value.keys():
                                   propetry = Node(key_min, name=propetry_value[key_min])
                                   graph.create(propetry)
                                   graph.create(Relationship(author, key, propetry))
               # 诗
               build_poem(author_data["poems"], author)

     with open('诗人.txt', 'w', encoding='utf-8') as f:
          for i in author_name_save:
               f.write(i+'\n')
     for i in other_save:
          with open(i+'.txt', 'w', encoding='utf-8') as f:
               for j in other_save[i]:
                    f.write(j+'\n')


def build_poem(poems, author):
     poem_name_save = []  # 诗歌标题
     poem_content_save = []  # 诗歌正文
     poem_list_save = []  # 别集
     poem_emotion_save = []  # 情感
     poem_ticai_save = []  # 题材
     poem_theme_save = []  # 主题
     poem_form_save = []  # 体裁
     poem_trans_save = []  # 诗歌译文
     poem_analyze_save = []  # 诗歌注释
     poem_apre_save = []  # 诗歌赏析


     for poemdata in poems:
          if poemdata:
               poem_name = poemdata['标题']
               # 诗歌节点
               poem = Node('诗歌', name=poem_name, id=poemdata['编号'])
               poem_name_save.append(poemdata['标题'])
               graph.create(poem)
               graph.create(Relationship(author, '作者', poem))
               # 诗歌正文
               poem_content = Node('诗歌正文', name=poemdata['正文'])
               poem_content_save.append(poemdata['正文'])
               graph.create(poem_content)
               graph.create(Relationship(poem, '正文', poem_content))
               # 内容标签体系
               # poem_label = Node('标签', name=poemdata['标签'])
               # 别集  a if a > b else b
               poem_list = Node('别集', name=poemdata['别集'] if '别集' in poemdata.keys() else '')
               if '别集' in poemdata.keys():
                    poem_list_save.append(poemdata['别集'])
               graph.create(poem_list)
               graph.create(Relationship(poem, '别集', poem_list))
               # 情感
               poem_emotion = Node('情感', name=poemdata['情感'] if '情感' in poemdata.keys() else '')
               if '情感' in poemdata.keys():
                    poem_emotion_save.append(poemdata['情感'])
               graph.create(poem_emotion)
               graph.create(Relationship(poem, '情感', poem_emotion))
               # 题材
               poem_ticai = Node('题材', name=poemdata['题材'] if '题材' in poemdata.keys() else '')
               if '题材' in poemdata.keys():
                    poem_ticai_save.append(poemdata['题材'])
               graph.create(poem_ticai)
               graph.create(Relationship(poem, '题材', poem_ticai))
               # 主题
               poem_theme = Node('主题', name=poemdata['主题'] if '主题' in poemdata.keys() else '')
               if '主题' in poemdata.keys():
                    poem_theme_save.append(poemdata['主题'])
               graph.create(poem_theme)
               graph.create(Relationship(poem, '主题', poem_theme))

               # 体裁
               poem_form = Node('体裁', name=poemdata['体裁'] if '体裁' in poemdata.keys() else '')
               if '体裁' in poemdata.keys():
                    poem_form_save.append(poemdata['体裁'])
               graph.create(poem_form)
               graph.create(Relationship(poem, '体裁', poem_form))

               # 诗歌译文
               poem_trans = Node('译文', name=poemdata['译文'] if '译文' in poemdata.keys() else '')
               if '译文' in poemdata.keys():
                    poem_trans_save.append(poemdata['译文'])
               graph.create(poem_trans)
               graph.create(Relationship(poem, '译文', poem_trans))
               # 诗歌注释
               poem_analyze = Node('注释', name=poemdata['注释'] if '注释' in poemdata.keys() else '')
               if '注释' in poemdata.keys():
                    poem_analyze_save.append(poemdata['注释'])
               graph.create(poem_analyze)
               graph.create(Relationship(poem, '注释', poem_analyze))
               # 诗歌赏析
               poem_apre = Node('赏析', name=poemdata['赏析'] if '赏析' in poemdata.keys() else '')
               if '赏析' in poemdata.keys():
                    poem_apre_save.append(poemdata['赏析'])
               graph.create(poem_apre)
               graph.create(Relationship(poem, '赏析', poem_apre))

     with open('诗歌.txt', 'a', encoding='utf-8') as f:
          for i in poem_name_save:
               f.write(i+'\n')
     with open('诗歌正文.txt', 'a', encoding='utf-8') as f:
          for i in poem_content_save:
               f.write(i+'\n')
     with open('别集.txt', 'a', encoding='utf-8') as f:
          for i in poem_list_save:
               f.write(i+'\n')
     with open('情感.txt', 'a', encoding='utf-8') as f:
          for i in poem_emotion_save:
               f.write(i+'\n')
     with open('题材.txt', 'a', encoding='utf-8') as f:
          for i in poem_ticai_save:
               f.write(i+'\n')
     with open('主题.txt', 'a', encoding='utf-8') as f:
          for i in poem_theme_save:
               f.write(i+'\n')
     with open('体裁.txt', 'a', encoding='utf-8') as f:
          for i in poem_form_save:
               f.write(i+'\n')
     with open('译文.txt', 'a', encoding='utf-8') as f:
          for i in poem_trans_save:
               f.write(i+'\n')
     with open('注释.txt', 'a', encoding='utf-8') as f:
          for i in poem_analyze_save:
               f.write(i+'\n')
     with open('赏析.txt', 'a', encoding='utf-8') as f:
          for i in poem_apre_save:
               f.write(i+'\n')

def init_kb():
     # 连接数据库
     # 初始化固定node
     labels_node = build_poem_label("./data/poem_label")
     dynastys_node = build_author_dynasty("./data/dynasty")
     sex_node = build_author_sex("./data/sex")
     language_node,country_node = build_poem_language("./data/language")
     build_author( './data/final.json')


graph = Graph(host='localhost', username="neo4j", password="zdh3622278")
graph.delete_all()

init_kb()










