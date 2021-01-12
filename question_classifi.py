#!/usr/bin/env python3
# coding: utf-8
# File: question_classifier.py
# Author: lhy<lhy_in_blcu@126.com,https://huangyong.github.io>
# Date: 18-10-4

import os
import ahocorasick

class QuestionClassifier:
    def __init__(self):
        cur_dir = '/'.join(os.path.abspath(__file__).split('/')[:-1])
        #　特征词路径
        self.poet_path = os.path.join(cur_dir, 'dict/诗人.txt')
        self.zi_path = os.path.join(cur_dir, 'dict/字.txt')
        self.hao_path = os.path.join(cur_dir, 'dict/号.txt')
        self.poemname_path = os.path.join(cur_dir, 'dict/诗歌.txt')
        self.chaodai_path = os.path.join(cur_dir, 'dict/朝代.txt')
        self.alias_path = os.path.join(cur_dir, 'dict/别名.txt')
        self.birth_place_path = os.path.join(cur_dir, 'dict/出生地.txt')
        self.country_path = os.path.join(cur_dir, 'dict/国别.txt')
        self.burial_ground_path = os.path.join(cur_dir, 'dict/墓葬地.txt')
        self.birthday_path = os.path.join(cur_dir, 'dict/生年月.txt')
        self.posthumous_title_path = os.path.join(cur_dir, 'dict/谥号.txt')
        self.language_path = os.path.join(cur_dir, 'dict/写作语言.txt')
        self.sex_path = os.path.join(cur_dir, 'dict/性别.txt')
        self.death_data_path = os.path.join(cur_dir, 'dict/卒年月.txt')
        self.other_relationship_path = os.path.join(cur_dir, 'dict/其它关系.txt')
        # 加载特征词
        self.poet_wds= [i.strip() for i in open(self.poet_path, encoding='utf-8') if i.strip()]
        self.zi_wds= [i.strip() for i in open(self.zi_path, encoding='utf-8') if i.strip()]
        self.hao_wds= [i.strip() for i in open(self.hao_path, encoding='utf-8') if i.strip()]
        self.poemname_wds= [i.strip() for i in open(self.poemname_path, encoding='utf-8') if i.strip()]
        self.chaodai_wds= [i.strip() for i in open(self.chaodai_path, encoding='utf-8') if i.strip()]
        self.alias_wds = [i.strip() for i in open(self.alias_path, encoding='UTF-8') if i.strip()]
        self.birth_place_wds = [i.strip() for i in open(self.birth_place_path, encoding='UTF-8') if i.strip()]
        self.country_wds = [i.strip() for i in open(self.country_path, encoding='UTF-8') if i.strip()]
        self.burial_ground_wds = [i.strip() for i in open(self.burial_ground_path, encoding='UTF-8') if i.strip()]
        self.birthday_wds = [i.strip() for i in open(self.birthday_path, encoding='UTF-8') if i.strip()]
        self.posthumous_title_wds = [i.strip() for i in open(self.posthumous_title_path, encoding='UTF-8') if i.strip()]
        self.language_wds = [i.strip() for i in open(self.language_path, encoding='UTF-8') if i.strip()]
        self.sex_wds = [i.strip() for i in open(self.sex_path, encoding='UTF-8') if i.strip()]
        self.death_data_wds = [i.strip() for i in open(self.death_data_path, encoding='UTF-8') if i.strip()]
        self.other_relationship_wds = [i.strip() for i in open(self.other_relationship_path, encoding='UTF-8') if i.strip()]
        self.region_wds = set(self.poet_wds+self.zi_wds+self.hao_wds+self.poemname_wds+self.chaodai_wds+self.alias_wds+self.birth_place_wds+self.country_wds+self.burial_ground_wds+self.birthday_wds+self.posthumous_title_wds+self.language_wds+self.sex_wds+self.death_data_wds+self.other_relationship_wds)
        #self.deny_words = [i.strip() for i in open(self.deny_path,encoding='UTF-8') if i.strip()]
        # 构造领域actree
        self.region_tree = self.build_actree(list(self.region_wds))
        # 构建词典
        self.wdtype_dict = self.build_wdtype_dict()
        # 问句疑问词
        self.poet_qwds = ['有谁','哪些诗人','写诗厉害的']
        self.zi_qwds = ['字是', '字为', '字什么', '是谁的字', '谁字','的字']
        self.hao_qwds = ['号是', '号为', '号什么', '谁的号', '谁号','的号']
        self.poem_qwds = ['代表作', '作品', '写了', '写的', '作者','的诗','名作']
        self.chaodai_qwds = ['朝','代', '时代', '时期','哪朝']
        self.alias_qwds = ['别名','别称','个性的称呼','称为','赞美','称号','谁是','是谁']
        self.birth_place_qwds = ['出生','哪里人','哪里的','生于哪里','孕育']
        self.country_qwds = ['国别', '国家', '国籍']
        self.introduction_qwds = ['的简介', '介绍','信息','人生经历','生平']
        self.burial_ground_qwds = ['墓葬地', '埋葬', '墓','埋']
        self.birthday_qwds = ['生于哪一年', '出生在哪一年', '出生日期', '出生年月','生日','生于何时','诞辰']
        self.content_qwds = ['正文', '内容','全文','背一下']
        self.posthumous_title_qwds = ['谥号']
        self.language_qwds = ['写作语言']
        self.sex_qwds = ['性别', '男女', '男的','女的', '男的还是女的', '男性', '女性']
        self.death_data_qwds = ['啥时候死的','何时死','卒年月', '死亡日期', '死亡时间', '何时去世','去世日期', '去世时间', '什么时候去世的','忌日']
        # self.achievement_qws = ['主要成就是', '主要成就为', '主要成就有', '有哪些主要成就']
        # self.commemoration_qws = ['后世纪念', '后世怎么纪念', '后世如何纪念', '后人纪念', '后人怎么纪念', '后世如何纪念']

        print('model init finished ......')

        return

    '''分类主函数'''
    def classify(self, question):
        data = {}
        medical_dict = self.check_medical(question)
        if not medical_dict:
            data['args']={'李白':['诗人']}
            data['question_types'] = ['poet']
            return data
        data['args'] = medical_dict
        #收集问句当中所涉及到的实体类型
        types = []
        for type_ in medical_dict.values():
            types += type_
        question_types = []

        if self.check_words(self.poet_qwds, question) :
            question_type = 'poet'
            question_types.append(question_type)
        if self.check_words(self.zi_qwds, question) and ('诗人' in types):
            question_types.append('poet_zi')
        if self.check_words(self.zi_qwds, question) and ('字' in types):
            question_types.append('zi_poet')
        if self.check_words(self.hao_qwds, question) and not self.check_words(self.posthumous_title_qwds, question) and ('诗人' in types):
            question_types.append('poet_hao')
        if self.check_words(self.hao_qwds, question) and not self.check_words(self.posthumous_title_qwds, question) and ('号' in types):
            question_types.append('hao_poet')
        if self.check_words(self.chaodai_qwds, question) and ('诗人' in types):
            question_types.append('poet_chaodai')
        if self.check_words(self.chaodai_qwds, question) and ('朝代' in types):
            question_types.append('chaodai_poet')
        if self.check_words(self.poem_qwds, question) and ('诗人' in types):
            question_types.append('poet_poemname')
        if self.check_words(self.poem_qwds, question) and ('诗歌' in types):
            question_types.append('poemname_poet')
        if self.check_words(self.alias_qwds, question) and ('诗人' in types):
            question_types.append('poet_alias')
        if self.check_words(self.alias_qwds, question) and ('别名' in types):
            question_types.append('alias_poet')
        if self.check_words(self.birth_place_qwds, question) and ('诗人' in types):
            question_types.append('poet_birth_place')
        if self.check_words(self.birth_place_qwds, question) and ('出生地' in types):
            question_types.append('birth_place_poet')
        if self.check_words(self.country_qwds, question) and ('诗人' in types):
            question_types.append('poet_country')
        if self.check_words(self.country_qwds, question) and ('国别' in types):
            question_types.append('country_poet')
        if self.check_words(self.introduction_qwds, question) and ('诗人' in types):
            question_types.append('poet_introduction')
        if self.check_words(self.burial_ground_qwds, question) and ('诗人' in types):
            question_types.append('poet_burial_ground')
        if self.check_words(self.burial_ground_qwds, question) and ('墓葬地' in types):
            question_types.append('burial_ground_poet')
        if self.check_words(self.birthday_qwds, question) and ('诗人' in types):
            question_types.append('poet_birthday')
        if self.check_words(self.birthday_qwds, question) and ('生年月' in types):
            question_types.append('birthday_poet')
        if self.check_words(self.content_qwds, question) and ('诗歌' in types):
            question_types.append('poem_content')
        if self.check_words(self.posthumous_title_qwds, question) and ('诗人' in types):
            question_types.append('poet_posthumous_title')
        if self.check_words(self.posthumous_title_qwds, question) and ('谥号' in types):
            question_types.append('posthumous_title_poet')
        if self.check_words(self.language_qwds, question) and ('诗人' in types):
            question_types.append('poet_language')
        if self.check_words(self.language_qwds, question) and ('写作语言' in types):
            question_types.append('language_poet')
        if self.check_words(self.sex_qwds, question) and ('诗人' in types):
            question_types.append('poet_sex')
        if self.check_words(self.sex_qwds, question) and ('性别' in types):
            question_types.append('sex_poet')
        if self.check_words(self.death_data_qwds, question) and ('诗人' in types):
            question_types.append('poet_death_data')
        if self.check_words(self.death_data_qwds, question) and ('卒年月' in types):
            question_types.append('death_data_poet')
        # if self.check_words(self.achievement_qws, question) and ('诗人' in types):
        #     question_types.append('poet_achievement')
        # if self.check_words(self.commemoration_qws, question) and ('诗人' in types):
        #     question_types.append('poet_commemoration')
        other_relationship = self.check_words(self.other_relationship_wds, question)
        if len(question_types) == 0 and other_relationship:
            for i in other_relationship:
                question_types.append(i)

        # 将多个分类结果进行合并处理，组装成一个字典
        data['question_types'] = question_types

        return data

    '''构造词对应的类型'''
    def build_wdtype_dict(self):
        wd_dict = dict()
        for wd in self.region_wds:
            wd_dict[wd] = []
            if wd in self.poet_wds:
                wd_dict[wd].append('诗人')
            if wd in self.zi_wds:
                wd_dict[wd].append('字')
            if wd in self.hao_wds:
                wd_dict[wd].append('号')
            if wd in self.poemname_wds:
                wd_dict[wd].append('诗歌')
            if wd in self.chaodai_wds:
                wd_dict[wd].append('朝代')
            if wd in self.alias_wds:
                wd_dict[wd].append('别名')
            if wd in self.birth_place_wds:
                wd_dict[wd].append('出生地')
            if wd in self.country_wds:
                wd_dict[wd].append('国别')
            # if wd in self.introduction_wds:
            #     wd_dict[wd].append('introduction')
            if wd in self.burial_ground_wds:
                wd_dict[wd].append('墓葬地')
            if wd in self.birthday_wds:
                wd_dict[wd].append('生年月')
            # if wd in self.content_wds:
            #     wd_dict[wd].append('content')
            if wd in self.posthumous_title_wds:
                wd_dict[wd].append('谥号')
            if wd in self.language_wds:
                wd_dict[wd].append('写作语言')
            if wd in self.sex_wds:
                wd_dict[wd].append('性别')
            if wd in self.death_data_wds:
                wd_dict[wd].append('卒年月')
            if wd in self.other_relationship_wds:
                wd_dict[wd].append('其它关系')
        return wd_dict

    '''构造actree，加速过滤'''
    def build_actree(self, wordlist):
        actree = ahocorasick.Automaton()
        for index, word in enumerate(wordlist):
            actree.add_word(word, (index, word))
        actree.make_automaton()
        print("actree:" + str(actree))
        return actree

    '''问句过滤'''
    def check_medical(self, question):
        region_wds = []
        for i in self.region_tree.iter(question):
            wd = i[1][1]
            region_wds.append(wd)
        stop_wds = []
        for wd1 in region_wds:
            for wd2 in region_wds:
                if wd1 in wd2 and wd1 != wd2:
                    stop_wds.append(wd1)
        final_wds = [i for i in region_wds if i not in stop_wds]
        final_dict = {i:self.wdtype_dict.get(i) for i in final_wds}

        return final_dict

    '''基于特征词进行分类'''
    def check_words(self, wds, sent):
        res = []
        for wd in wds:
            if wd in sent:
                res.append(wd)
        return res


if __name__ == '__main__':
    handler = QuestionClassifier()
    while 1:
        question = input('input an question:')
        data = handler.classify(question)
        print(data)