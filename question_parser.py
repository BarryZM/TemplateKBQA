#!/usr/bin/env python3
# coding: utf-8
# File: question_parser.py
# Author: lhy<lhy_in_blcu@126.com,https://huangyong.github.io>
# Date: 18-10-4

class QuestionPaser:

    '''构建实体节点'''
    def build_entitydict(self, args):
        entity_dict = {}
        for arg, types in args.items():
            for type in types:
                if type not in entity_dict:
                    entity_dict[type] = [arg]
                else:
                    entity_dict[type].append(arg)

        return entity_dict

    '''解析主函数'''
    def parser_main(self, res_classify):
        args = res_classify['args']
        entity_dict = self.build_entitydict(args)
        question_types = res_classify['question_types']
        sqls = []
        for question_type in question_types:
            sql_ = {}
            sql_['question_type'] = question_type
            sql = []
            if question_type == 'poet_zi':
                sql = self.sql_transfer(question_type, entity_dict.get('诗人'))
            elif question_type == 'zi_poet':
                sql = self.sql_transfer(question_type, entity_dict.get('字'))
            elif question_type == 'poet_hao':
                sql = self.sql_transfer(question_type, entity_dict.get('诗人'))
            elif question_type == 'hao_poet':
                sql = self.sql_transfer(question_type, entity_dict.get('号'))
            elif question_type == 'poet_chaodai':
                sql = self.sql_transfer(question_type, entity_dict.get('诗人'))
            elif question_type == 'chaodai_poet':
                sql = self.sql_transfer(question_type, entity_dict.get('朝代'))
            elif question_type == 'poet_poemname':
                sql = self.sql_transfer(question_type, entity_dict.get('诗人'))
            elif question_type == 'poemname_poet':
                sql = self.sql_transfer(question_type, entity_dict.get('诗歌'))
            elif question_type == 'poet_alias':
                sql = self.sql_transfer(question_type, entity_dict.get('诗人'))
            elif question_type == 'alias_poet':
                sql = self.sql_transfer(question_type, entity_dict.get('别名'))
            elif question_type == 'poet_birth_place':
                sql = self.sql_transfer(question_type, entity_dict.get('诗人'))
            elif question_type == 'birth_place_poet':
                sql = self.sql_transfer(question_type, entity_dict.get('出生地'))
            elif question_type == 'poet_country':
                sql = self.sql_transfer(question_type, entity_dict.get('诗人'))
            elif question_type == 'country_poet':
                sql = self.sql_transfer(question_type, entity_dict.get('国别'))
            elif question_type == 'poet_introduction':
                sql = self.sql_transfer(question_type, entity_dict.get('诗人'))
            elif question_type == 'poet_burial_ground':
                sql = self.sql_transfer(question_type, entity_dict.get('诗人'))
            elif question_type == 'burial_ground_poet':
                sql = self.sql_transfer(question_type, entity_dict.get('墓葬地'))
            elif question_type == 'poet_birthday':
                sql = self.sql_transfer(question_type, entity_dict.get('诗人'))
            elif question_type == 'birthday_poet':
                sql = self.sql_transfer(question_type, entity_dict.get('生年月'))
            elif question_type == 'poem_content':
                sql = self.sql_transfer(question_type, entity_dict.get('诗歌'))
            elif question_type == 'poet_posthumous_title':
                sql = self.sql_transfer(question_type, entity_dict.get('诗人'))
            elif question_type == 'posthumous_title_poet':
                sql = self.sql_transfer(question_type, entity_dict.get('谥号'))
            elif question_type == 'poet_language':
                sql = self.sql_transfer(question_type, entity_dict.get('诗人'))
            elif question_type == 'language_poet':
                sql = self.sql_transfer(question_type, entity_dict.get('写作语言'))
            elif question_type == 'poet_sex':
                sql = self.sql_transfer(question_type, entity_dict.get('诗人'))
            elif question_type == 'sex_poet':
                sql = self.sql_transfer(question_type, entity_dict.get('性别'))
            elif question_type == 'poet_death_data':
                sql = self.sql_transfer(question_type, entity_dict.get('诗人'))
            elif question_type == 'death_data_poet':
                sql = self.sql_transfer(question_type, entity_dict.get('卒年月'))
            # elif question_type == 'poet_achievement':
            #     sql = self.sql_transfer(question_type, entity_dict.get('诗人'))
            # elif question_type == 'poet_commemoration':
            #     sql = self.sql_transfer(question_type, entity_dict.get('诗人'))
            else:
                sql = self.sql_transfer(question_type, args)

            if sql:
                sql_['sql'] = sql

                sqls.append(sql_)

        return sqls

    '''针对不同的问题，分开进行处理'''
    def sql_transfer(self, question_type, entities):
        if not entities:
            return []
        print('question_type: ', question_type)

        # 查询语句
        sql = []
        if question_type == 'poet_zi':
            sql = ["MATCH (m:诗人)-[r:字]->(n:字) where m.name = '{0}' return m.name,n.name".format(i) for i in entities]
        elif question_type == 'zi_poet':
            sql = ["MATCH (m:诗人)-[r:字]->(n:字) where n.name = '{0}' return n.name,m.name".format(i) for i in entities]
        elif question_type == 'poet_hao':
            sql = ["MATCH (m:诗人)-[r:号]->(n:号) where m.name = '{0}' return m.name,n.name".format(i) for i in entities]
        elif question_type == 'hao_poet':
            sql = ["MATCH (m:诗人)-[r:号]->(n:号) where n.name = '{0}' return n.name,m.name".format(i) for i in entities]
        elif question_type == 'poet_chaodai':
            sql = ["MATCH (m:诗人)-[r:朝代]->(n:朝代) where m.name = '{0}' return m.name,n.name".format(i) for i in entities]
        elif question_type == 'chaodai_poet':
            sql = ["MATCH (m:诗人)-[r:朝代]->(n:朝代) where n.name = '{0}' return n.name,m.name".format(i) for i in entities]
        elif question_type == 'poet_poemname':
            sql = ["MATCH (m:诗人)-[r:作者]->(n:诗歌) where m.name = '{0}' return m.name,n.name".format(i) for i in entities]
        elif question_type == 'poemname_poet':
            sql = ["MATCH (m:诗人)-[r:作者]->(n:诗歌) where n.name = '{0}' return m.name,n.name".format(i) for i in entities]
        elif question_type == 'poet_alias':
            sql = ["MATCH (m:诗人)-[r:别名]->(n:别名) where m.name = '{0}' return m.name,n.name".format(i) for i in entities]
        elif question_type == 'alias_poet':
            sql = ["MATCH (m:诗人)-[r:别名]->(n:别名) where n.name = '{0}' return n.name,m.name".format(i) for i in entities]
        elif question_type == 'poet_birth_place':
            sql = ["MATCH (m:诗人)-[r:出生地]->(n:出生地) where m.name = '{0}' return m.name,n.name".format(i) for i in entities]
        elif question_type == 'birth_place_poet':
            sql = ["MATCH (m:诗人)-[r:出生地]->(n:出生地) where n.name = '{0}' return n.name,m.name".format(i) for i in entities]
        elif question_type == 'poet_country':
            sql = ["MATCH (m:诗人)-[r:国别]->(n:国别) where m.name = '{0}' return m.name,n.name".format(i) for i in entities]
        elif question_type == 'country_poet':
            sql = ["MATCH (m:诗人)-[r:国别]->(n:国别) where n.name = '{0}' return n.name,m.name".format(i) for i in entities]
        elif question_type == 'poet_introduction':
            sql = ["MATCH (m:诗人)-[r:简介]->(n:简介) where m.name = '{0}' return m.name,n.name".format(i) for i in entities]
        elif question_type == 'poet_burial_ground':
            sql = ["MATCH (m:诗人)-[r:墓葬地]->(n:墓葬地) where m.name = '{0}' return m.name,n.name".format(i) for i in entities]
        elif question_type == 'burial_ground_poet':
            sql = ["MATCH (m:诗人)-[r:墓葬地]->(n:墓葬地) where n.name = '{0}' return n.name,m.name".format(i) for i in entities]
        elif question_type == 'poet_birthday':
            sql = ["MATCH (m:诗人)-[r:生年月]->(n:生年月) where m.name = '{0}' return m.name,n.name".format(i) for i in entities]
        elif question_type == 'birthday_poet':
            sql = ["MATCH (m:诗人)-[r:生年月]->(n:生年月) where n.name = '{0}' return n.name,m.name".format(i) for i in entities]
        elif question_type == 'poem_content':
            sql = ["MATCH (m:诗歌)-[r:正文]->(n:诗歌正文) where m.name = '{0}' return m.name,n.name".format(i) for i in entities]
        elif question_type == 'poet_posthumous_title':
            sql = ["MATCH (m:诗人)-[r:谥号]->(n:谥号) where m.name = '{0}' return m.name,n.name".format(i) for i in entities]
        elif question_type == 'posthumous_title_poet':
            sql = ["MATCH (m:诗人)-[r:谥号]->(n:谥号) where n.name = '{0}' return n.name,m.name".format(i) for i in entities]
        elif question_type == 'poet_language':
            sql = ["MATCH (m:诗人)-[r:写作语言]->(n:写作语言) where m.name = '{0}' return m.name,n.name".format(i) for i in entities]
        elif question_type == 'language_poet':
            sql = ["MATCH (m:诗人)-[r:写作语言]->(n:写作语言) where n.name = '{0}' return n.name,m.name".format(i) for i in entities]
        elif question_type == 'poet_sex':
            sql = ["MATCH (m:诗人)-[r:性别]->(n:性别) where m.name = '{0}' return m.name,n.name".format(i) for i in entities]
        elif question_type == 'sex_poet':
            sql = ["MATCH (m:诗人)-[r:性别]->(n:性别) where n.name = '{0}' return n.name,m.name".format(i) for i in entities]
        elif question_type == 'poet_death_data':
            sql = ["MATCH (m:诗人)-[r:卒年月]->(n:卒年月) where m.name = '{0}' return m.name,n.name".format(i) for i in entities]
        elif question_type == 'death_data_poet':
            sql = ["MATCH (m:诗人)-[r:卒年月]->(n:卒年月) where n.name = '{0}' return n.name,m.name".format(i) for i in entities]
        # elif question_type == 'poet_achievement':
        #     sql = ["MATCH (m:诗人)-[r:主要成就]->(n:主要成就) where m.name = '{0}' return m.name,n.name".format(i) for i in entities]
        # elif question_type == 'poet_commemoration':
        #     sql = ["MATCH (m:诗人)-[r:后世纪念]->(n:后世纪念) where m.name = '{0}' return m.name,n.name".format(i) for i in entities]
        else:
            for key in entities.keys():
                sql.append("MATCH (m:"+entities[key][0]+")-[r:"+question_type+"]->(n:"+question_type+") where m.name = '{0}' return m.name,n.name".format(key))  # TODO: 这里默认每个实体只属于一种类型
                sql.append("MATCH (m:"+question_type+")-[r:"+question_type+"]->(n:"+entities[key][0]+") where n.name = '{0}' return n.name,m.name".format(key))

        return sql



if __name__ == '__main__':
    handler = QuestionPaser()
