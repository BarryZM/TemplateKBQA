#!/usr/bin/env python3
# coding: utf-8
# File: answer_search.py
# Author: lhy<lhy_in_blcu@126.com,https://huangyong.github.io>
# Date: 18-10-5

from py2neo import Graph
import random

class AnswerSearcher:
    def __init__(self):
        self.g = Graph(
            "http://localhost:7474",
            user="neo4j",
            password="zdh3622278")
        self.num_limit = 20

    '''执行cypher查询，并返回相应结果'''

    def search_main(self, sqls):
        final_answers = []
        for sql_ in sqls:
            question_type = sql_['question_type']
            queries = sql_['sql']
            answers = []
            for query in queries:
                print("query: ", query)
                ress = self.g.run(query).data()
                answers += ress
            print("answers: ", answers)
            final_answer = self.answer_prettify(question_type, answers)
            if final_answer:
                final_answers.append(final_answer)
        return final_answers

    '''根据对应的qustion_type，调用相应的回复模板'''

    def answer_prettify(self, question_type, answers):
        final_answer = []
        if not answers:
            return ''
        if question_type == 'poet':
            desc = [i['m.name'] for i in answers]
            final_answer = '有{0}'.format('；'.join(list(set(desc))[:self.num_limit]))
        elif question_type == 'poet_zi' :
            desc = [i['m.name'] for i in answers]
            subject = answers[0]['n.name']
            final_answer.append( '{1}的字是{0}'.format(subject, '；'.join(list(set(desc))[:self.num_limit])))
            final_answer.append('{1}字{0}'.format(subject, '；'.join(list(set(desc))[:self.num_limit])))
            final_answer.append('让我告诉你，{1}字{0}'.format(subject, '；'.join(list(set(desc))[:self.num_limit])))
            final_answer.append('当然知道啦，{1}字{0}'.format(subject, '；'.join(list(set(desc))[:self.num_limit])))
            final_answer.append('满足你！{1}的字是{0}哦~'.format(subject, '；'.join(list(set(desc))[:self.num_limit])))
        elif question_type == 'zi_poet':
            desc = [i['m.name'] for i in answers]
            subject = answers[0]['n.name']
            final_answer.append('{1}呀'.format(subject, '；'.join(list(set(desc))[:self.num_limit])))
            final_answer.append('是{1}的字呀'.format(subject, '；'.join(list(set(desc))[:self.num_limit])))
            final_answer.append('是{1}的！'.format(subject, '；'.join(list(set(desc))[:self.num_limit])))
            final_answer.append('{0}是{1}的字'.format(subject, '；'.join(list(set(desc))[:self.num_limit])))
            final_answer.append('大诗人{1}的字是{0}'.format(subject, '；'.join(list(set(desc))[:self.num_limit])))
            final_answer.append('除了{1}还有谁'.format(subject, '；'.join(list(set(desc))[:self.num_limit])))
        elif question_type == 'poet_hao' :
            desc = [i['m.name'] for i in answers]
            subject = answers[0]['n.name']
            final_answer.append( '号{0}'.format(subject, '；'.join(list(set(desc))[:self.num_limit])))
            final_answer.append( '是{0}'.format(subject, '；'.join(list(set(desc))[:self.num_limit])))
            final_answer.append('好的，{1}的号是{0}'.format(subject, '；'.join(list(set(desc))[:self.num_limit])))
            final_answer.append('这我知道，是{0}'.format(subject, '；'.join(list(set(desc))[:self.num_limit])))
            final_answer.append( '{1}号{0}'.format(subject, '；'.join(list(set(desc))[:self.num_limit])))
        elif question_type == 'hao_poet':
            desc = [i['m.name'] for i in answers]
            subject = answers[0]['n.name']
            final_answer.append( '{1}！'.format(subject, '；'.join(list(set(desc))[:self.num_limit])))
            final_answer.append( '是{1}的{0}'.format(subject, '；'.join(list(set(desc))[:self.num_limit])))
            final_answer.append('{1}！{1}！{1}！重要的事说三遍！'.format(subject, '；'.join(list(set(desc))[:self.num_limit])))
            final_answer.append('这不是{1}的号吗？'.format(subject, '；'.join(list(set(desc))[:self.num_limit])))
            final_answer.append( '{1}大诗人'.format(subject, '；'.join(list(set(desc))[:self.num_limit])))
            final_answer.append('{1}的号是{0}'.format(subject, '；'.join(list(set(desc))[:self.num_limit])))
        elif question_type == 'poet_poemname':
            desc = [i['m.name'] for i in answers]
            subject = answers[0]['n.name']
            final_answer.append('他的诗太多了，我想你肯定听过《{0}》'.format(subject, '；'.join(list(set(desc))[:self.num_limit])))
            final_answer.append('让我想想，有《{0}》......'.format(subject, '；'.join(list(set(desc))[:self.num_limit])))
            final_answer.append('有《{0}》还有好多呢，他的诗我都说不完'.format(subject, '；'.join(list(set(desc))[:self.num_limit])))
            final_answer.append('《{0}》是他写的'.format(subject, '；'.join(list(set(desc))[:self.num_limit])))
            final_answer.append('有很多，比如《{0}》'.format(subject, '；'.join(list(set(desc))[:self.num_limit])))
            final_answer.append('他写了《{0}》'.format(subject, '；'.join(list(set(desc))[:self.num_limit])))
            final_answer.append('有啊，比如《{0}》'.format(subject, '；'.join(list(set(desc))[:self.num_limit])))
        elif question_type == 'poemname_poet':
            desc = [i['m.name'] for i in answers]
            subject = answers[0]['n.name']
            final_answer.append('{1}写的'.format(subject, '；'.join(list(set(desc))[:self.num_limit])))
            final_answer.append('是{1}的代表作'.format(subject, '；'.join(list(set(desc))[:self.num_limit])))
            final_answer.append('是{1}的名作'.format(subject, '；'.join(list(set(desc))[:self.num_limit])))
            final_answer.append('这首诗是{1}的作品'.format(subject, '；'.join(list(set(desc))[:self.num_limit])))
        elif question_type == 'poet_chaodai':
            desc = [i['m.name'] for i in answers]
            subject = answers[0]['n.name']
            final_answer.append('{{0}时期'.format(subject, '；'.join(list(set(desc))[:self.num_limit])))
            final_answer.append('{1}属于{0}这个时代'.format(subject, '；'.join(list(set(desc))[:self.num_limit])))
            final_answer.append('{1}是{0}人'.format(subject, '；'.join(list(set(desc))[:self.num_limit])))
            final_answer.append('{1}生活在{0}这个时代'.format(subject, '；'.join(list(set(desc))[:self.num_limit])))
            final_answer.append('{1}是{0}的大诗人'.format(subject, '；'.join(list(set(desc))[:self.num_limit])))
        elif question_type == 'chaodai_poet':
            desc = [i['m.name'] for i in answers]
            subject = answers[0]['n.name']
            final_answer.append('{0}的诗人有{1}，还有很多我就不一一列举了'.format(subject, '；'.join(list(set(desc))[:self.num_limit])))
            final_answer.append('{1}都是{0}这个时代'.format(subject, '；'.join(list(set(desc))[:self.num_limit])))
            final_answer.append('恩好的，{0}的诗人有{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit])))
            final_answer.append('{1}是{0}的代表诗人'.format(subject, '；'.join(list(set(desc))[:self.num_limit])))
            final_answer.append('我知道的有{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit])))
        elif question_type == 'poet_alias':
            desc = [i['m.name'] for i in answers]
            subject = answers[0]['n.name']
            final_answer.append( '是{0}'.format(subject, '；'.join(list(set(desc))[:self.num_limit])))
            final_answer.append('{1}的别名是{0}'.format(subject, '；'.join(list(set(desc))[:self.num_limit])))
            final_answer.append('{0}是他的一个别名'.format(subject, '；'.join(list(set(desc))[:self.num_limit])))
            final_answer.append('大家会称他为{0}'.format(subject, '；'.join(list(set(desc))[:self.num_limit])))
        elif question_type == 'alias_poet':
            desc = [i['m.name'] for i in answers]
            subject = answers[0]['n.name']
            final_answer.append( '是{1}的别名呀'.format(subject, '；'.join(list(set(desc))[:self.num_limit])))
            final_answer.append('{1}的别名是{0}'.format(subject, '；'.join(list(set(desc))[:self.num_limit])))
            final_answer.append('大诗人{1}}'.format(subject, '；'.join(list(set(desc))[:self.num_limit])))
            final_answer.append('除了{1}，没有人能配得上'.format(subject, '；'.join(list(set(desc))[:self.num_limit])))
            final_answer.append('{1}是{0}'.format(subject, '；'.join(list(set(desc))[:self.num_limit])))
        elif question_type == 'poet_birth_place':
            desc = [i['m.name'] for i in answers]
            subject = answers[0]['n.name']
            final_answer.append('{1}的出生地是{0}'.format(subject, '；'.join(list(set(desc))[:self.num_limit])))
            final_answer.append('他在{0}出生的'.format(subject, '；'.join(list(set(desc))[:self.num_limit])))
            final_answer.append('{1}是{0}人'.format(subject, '；'.join(list(set(desc))[:self.num_limit])))
            final_answer.append('他是在{0}这个地方出生的'.format(subject, '；'.join(list(set(desc))[:self.num_limit])))
            final_answer.append('他生于{0}'.format(subject, '；'.join(list(set(desc))[:self.num_limit])))
        elif question_type == 'birth_place_poet':
            desc = [i['m.name'] for i in answers]
            subject = answers[0]['n.name']
            final_answer.append('{1}的出生地是{0}'.format(subject, '；'.join(list(set(desc))[:self.num_limit])))
            final_answer.append('{1}是{0}的'.format(subject, '；'.join(list(set(desc))[:self.num_limit])))
            final_answer.append('{1}出生于{0}'.format(subject, '；'.join(list(set(desc))[:self.num_limit])))
            final_answer.append('在{0}出生的有{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit])))
            final_answer.append('{1}是在{0}出生的'.format(subject, '；'.join(list(set(desc))[:self.num_limit])))
            final_answer.append('{1}是{0}人'.format(subject, '；'.join(list(set(desc))[:self.num_limit])))
        elif question_type == 'poet_country' or question_type == 'country_poet':
            desc = [i['m.name'] for i in answers]
            subject = answers[0]['n.name']
            final_answer = '{1}的国别是{0}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))
        elif question_type == 'poet_introduction':
            desc = [i['m.name'] for i in answers]
            subject = answers[0]['n.name']
            final_answer = '{0}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))
        elif question_type == 'poet_burial_ground':
            desc = [i['m.name'] for i in answers]
            subject = answers[0]['n.name']
            final_answer.append('{1}的墓葬地为{0}'.format(subject, '；'.join(list(set(desc))[:self.num_limit])))
            final_answer.append('{1}的墓在{0}'.format(subject, '；'.join(list(set(desc))[:self.num_limit])))
            final_answer.append('他被葬在了{0}'.format(subject, '；'.join(list(set(desc))[:self.num_limit])))
            final_answer.append('他的墓地在{0}'.format(subject, '；'.join(list(set(desc))[:self.num_limit])))
        elif question_type == 'burial_ground_poet':
            desc = [i['m.name'] for i in answers]
            subject = answers[0]['n.name']
            final_answer.append('有{1}诗人呀'.format(subject, '；'.join(list(set(desc))[:self.num_limit])))
            final_answer.append('可以去{1}的墓地，非常有名'.format(subject, '；'.join(list(set(desc))[:self.num_limit])))
            final_answer.append('有{1}等'.format(subject, '；'.join(list(set(desc))[:self.num_limit])))
        elif question_type == 'poet_birthday':
            desc = [i['m.name'] for i in answers]
            subject = answers[0]['n.name']
            final_answer.append( '他的生日是{0}'.format(subject, '；'.join(list(set(desc))[:self.num_limit])))
            final_answer.append('出生于{0}年'.format(subject, '；'.join(list(set(desc))[:self.num_limit])))
            final_answer.append('生于{0}年'.format(subject, '；'.join(list(set(desc))[:self.num_limit])))
            final_answer.append('{1}的出生年月为{0}'.format(subject, '；'.join(list(set(desc))[:self.num_limit])))
        elif question_type == 'birthday_poet':
            desc = [i['m.name'] for i in answers]
            subject = answers[0]['n.name']
            final_answer.append( '{1}的出生年月为{0}'.format(subject, '；'.join(list(set(desc))[:self.num_limit])))
            final_answer.append('{1}，{1}的生日为{0}'.format(subject, '；'.join(list(set(desc))[:self.num_limit])))
            final_answer.append('生于{0}的诗人有{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit])))
            final_answer.append('{1}的出生年月为{0}'.format(subject, '；'.join(list(set(desc))[:self.num_limit])))
        elif question_type == 'poem_content':
            desc = [i['m.name'] for i in answers]
            subject = answers[0]['n.name']
            final_answer.append('{1}的正文为：{0}'.format(subject, '；'.join(list(set(desc))[:self.num_limit])))
            final_answer.append('我给你读一遍,{0}'.format(subject, '；'.join(list(set(desc))[:self.num_limit])))
            final_answer.append('你是在考我吗，难不到我的:{0}'.format(subject, '；'.join(list(set(desc))[:self.num_limit])))
            final_answer.append('好的，听好了,{0}'.format(subject, '；'.join(list(set(desc))[:self.num_limit])))
        elif question_type == 'poet_posthumous_title':
            desc = [i['m.name'] for i in answers]
            subject = answers[0]['n.name']
            final_answer.append('{1}的谥号为{0}'.format(subject, '；'.join(list(set(desc))[:self.num_limit])))
            final_answer.append('这个我知道，{1}的谥号是{0}'.format(subject, '；'.join(list(set(desc))[:self.num_limit])))
            final_answer.append('我想想，哦哦，{1}的谥号为{0}'.format(subject, '；'.join(list(set(desc))[:self.num_limit])))
        elif question_type == 'posthumous_title_poet':
            desc = [i['m.name'] for i in answers]
            subject = answers[0]['n.name']
            final_answer.append('{1}的谥号为{0}'.format(subject, '；'.join(list(set(desc))[:self.num_limit])))
            final_answer.append('谥号是{0}的有{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit])))
        elif question_type == 'poet_language' or question_type == 'language_poet':
            desc = [i['m.name'] for i in answers]
            subject = answers[0]['n.name']
            final_answer = '{1}的写作语言为{0}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))
        elif question_type == 'poet_sex':
            desc = [i['m.name'] for i in answers]
            subject = answers[0]['n.name']
            final_answer.append('{1}的性别为{0}'.format(subject, '；'.join(list(set(desc))[:self.num_limit])))
            final_answer.append('{1}是个{0}诗人'.format(subject, '；'.join(list(set(desc))[:self.num_limit])))
        elif question_type == 'sex_poet':
            desc = [i['m.name'] for i in answers]
            subject = answers[0]['n.name']
            final_answer.append('著名的{0}诗人有{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit])))
            final_answer.append('{1}都是著名的{0}诗人'.format(subject, '；'.join(list(set(desc))[:self.num_limit])))
        elif question_type == 'poet_death_data':
            desc = [i['m.name'] for i in answers]
            subject = answers[0]['n.name']
            final_answer.append('{1}的卒年月为{0}'.format(subject, '；'.join(list(set(desc))[:self.num_limit])))
            final_answer.append('{1}是{0}去世的'.format(subject, '；'.join(list(set(desc))[:self.num_limit])))
        elif question_type == 'death_data_poet':
            desc = [i['m.name'] for i in answers]
            subject = answers[0]['n.name']
            final_answer.append('{1}的卒年月为{0}'.format(subject, '；'.join(list(set(desc))[:self.num_limit])))
            final_answer.append('有{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit])))
        # elif question_type == 'poet_achievement':
        #     desc = [i['m.name'] for i in answers]
        #     subject = answers[0]['n.name']
        #     final_answer = '{1}的主要成就为{0}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))
        # elif question_type == 'poet_commemoration':
        #     desc = [i['m.name'] for i in answers]
        #     subject = answers[0]['n.name']
        #     final_answer = '{1}的后世纪念为{0}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))
        else:
            desc = [i['m.name'] for i in answers]
            subject = answers[0]['n.name']
            print('subject: ', subject)
            print('desc: ', desc)
            final_answer = '{0}的'.format('；'.join(list(set(desc))[:self.num_limit])) + question_type + '为{0}'.format(
                subject)
        l = len(final_answer)
        i = random.randint(0,l-1)
        return final_answer[i]


if __name__ == '__main__':
    searcher = AnswerSearcher()