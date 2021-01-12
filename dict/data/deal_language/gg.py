import re
with open('./language000', "r", encoding="utf-8") as file_00:
    with open('./language', "a+", encoding='UTF-8') as file:
        for i in file_00.readlines():
            if len(i)>10:
                lan = i.strip().split('->')
                lan_0 = lan[0].replace('\xa0', '').strip()
                lan_1 = lan[1].replace('\xa0', '').strip()
                lan_2 = lan[2].replace('\xa0', '').strip()
                lan_3 = lan[3].replace('\xa0', '').strip()

                p1 = re.compile(r'[(](.*?)[)]', re.S)  # 最小匹配

                county_EN = re.findall(p1, lan_2)
                if len(county_EN) == 1:
                    county_EN = county_EN[0]
                else:
                    county_EN = str('')
                county_CN = re.findall(p1, lan_3)
                if len(county_CN) == 1:
                    county_CN = county_CN[0]
                else:
                    county_CN=str('')

                if '(' in lan_2:
                    lan_2 = lan_2.split('(')[0].strip()

                if '(' in lan_3:
                    lan_3 = lan_3.split('(')[0].strip()

                if '_' in lan_0:
                    lan_0_0 = lan_0.split('_')[0]
                    lan_0_1 = lan_0.split('_')[1]
                else:
                    lan_0_0 = lan_0
                    lan_0_1 = ""
                file.writelines(lan_0_0 + ',' + lan_0_1 + ',' + lan_1 + ','+str(county_EN) + ','+county_CN + ','+lan_2 + ','+lan_3 + ','+'\n')
