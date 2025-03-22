from datetime import datetime, timedelta, date
import lunarcalendar
import pandas as pd
from collections import Counter

import streamlit as st # sssssssssssss

def AllBaziCalulate(date_input,time_inputs,sex):
    def get_heavenly_earthly_year(lunar_year):
        """ Compute the Heavenly Stem and Earthly Branch for a given lunar year. """
        stem_index = (lunar_year - 4) % 10
        branch_index = (lunar_year - 4) % 12
        return heavenly_stems[stem_index], earthly_branches[branch_index]

    def get_heavenly_earthly_month(lunar_year, lunar_month, lunar_day):
        """ Compute the Heavenly Stem and Earthly Branch for a given lunar month. """
        branch_index = (lunar_month + 1) % 12  
        year_stem_index = (lunar_year - 4) % 10 
        stem_index = (year_stem_index * 2 + lunar_month) % 10 - 9


        td = find_transition_date(int(date_input.split('-')[0]),int(date_input.split('-')[1]))

        gregorian_date = datetime.strptime(td, "%Y-%m-%d")
        gregorian_date = gregorian_date + timedelta(hours=dt)
        td_lunar_date = lunarcalendar.Converter.Solar2Lunar(gregorian_date)

        if td_lunar_date.day > 15 or td_lunar_date.isleap:
            stem_index += 1
            branch_index += 1
            if stem_index > len(heavenly_stems) - 1:
                stem_index = 0
            if branch_index > len(earthly_branches) - 1:
                branch_index = 0

        return heavenly_stems[stem_index], earthly_branches[branch_index]

    def get_heavenly_earthly_day(gregorian_date):
        """ Compute the Heavenly Stem and Earthly Branch for a given day. """
        days_since_reference = (gregorian_date - reference_date).days
        stem_index = (days_since_reference) % 10  # 📌 Offset by +6 (Jia Chen, 甲辰)
        branch_index = (days_since_reference + 4) % 12  # 📌 Offset by +4
        return heavenly_stems[stem_index], earthly_branches[branch_index]

    def get_heavenly_earthly_hour(input_time,day_stem):
        def look_hr_table(day_stem,branch,idx):
            def lx(x):
                start_index = heavenly_stems.index(x)
                cyclic_list = [heavenly_stems[(start_index + i) % len(heavenly_stems)] for i in range(13)]
                cyclic_list = [cyclic_list[-1]] + cyclic_list[:-1]

                return cyclic_list

            X = []
            for x in ["Jia (甲)",'Bing (丙)','Wu (戊)','Geng (庚)','Ren (壬)']:
                X.append(lx(x))

            if day_stem in ['Jia (甲)','Ji (己)']:
                z = X[0]
            elif day_stem in ['Yi (乙)','Geng (庚)']:
                z = X[1]
            elif day_stem in ['Bing (丙)','Xin (辛)']:
                z = X[2]
            elif day_stem in ['Ding (丁)','Ren (壬)']:
                z = X[3]
            elif day_stem in ['Wu (戊)','Gui (癸)']:
                z = X[4]

            return z[idx],branch

        def get_earthly_branch_from_hour(input_time):
            """Determine the Earthly Branch (Shichen) from a given hour in 24-hour format."""
            hour = int(input_time.split(":")[0])
            shichen_table = {
    #             (23, 24): "Ye Zi", # earthly_branches[0], # "Ye Zi",
    #             (0, 1): earthly_branches[0],
                (0, 0.9): earthly_branches[0],
                (23, 24): earthly_branches[0],
                (1, 2): earthly_branches[1],
                (3, 4): earthly_branches[2],
                (5, 6): earthly_branches[3],
                (7, 8): earthly_branches[4],
                (9, 10): earthly_branches[5],
                (11, 12): earthly_branches[6],
                (13, 14): earthly_branches[7],
                (15, 16): earthly_branches[8],
                (17, 18): earthly_branches[9],
                (19, 20): earthly_branches[10],
                (21, 22): earthly_branches[11]
                
            }
            for (start, end), branch in shichen_table.items():
                if start <= hour <= end:
                    return branch
            return "Unknown"

        branch = get_earthly_branch_from_hour(input_time)
        if branch == "Ye Zi":
            idx = 0
        else:
            idx = earthly_branches.index(branch)+1

        return look_hr_table(day_stem,branch,idx)

    def get_stem_branch_for_date(date_str, time_input, dt):
        """ Convert a Gregorian date to a Lunar date and return the Heavenly Stem and Earthly Branch. """
        gregorian_date = datetime.strptime(date_str, "%Y-%m-%d")
        gregorian_date = gregorian_date + timedelta(hours=dt)
        
        lunar_date = lunarcalendar.Converter.Solar2Lunar(gregorian_date)
        year_stem, year_branch = get_heavenly_earthly_year(lunar_date.year)
        month_stem, month_branch = get_heavenly_earthly_month(lunar_date.year, lunar_date.month, lunar_date.day)
        day_stem, day_branch = get_heavenly_earthly_day(gregorian_date)
        hour_stem, hour_branch = get_heavenly_earthly_hour(time_input,day_stem)
        
        return {
            "Year" : { "stem" : year_stem , "branch" : year_branch },
            "Month" : { "stem" : month_stem , "branch" : month_branch },
            "Day" : { "stem" : day_stem , "branch" : day_branch },
            "Hour" : { "stem" : hour_stem , "branch" : hour_branch },
            "LunarDate": f"{lunar_date.year}-{lunar_date.month}-{lunar_date.day}" 
        }

    def find_luck_pillars(sex,stem_branch):
        def is_fw(sex,stem_branch_year):
            if heavenly_stems.index(stem_branch_year) % 2 == 0:
                yy = 'yang'
            else:
                yy = 'yin'

            if yy == 'yang' and sex == 'male' or yy == 'yin' and sex == 'female':
                fw = True
            else:
                fw = False
            return fw
        
        stem_branch_year = stem_branch['Year']['stem']
        is_forward = is_fw(sex,stem_branch_year)
        stem_branch_day = stem_branch['Month']

        start_index = heavenly_stems.index(stem_branch_day['stem'])
        start_branch_index = earthly_branches.index(stem_branch_day['branch'])

        if is_forward:
            print('fw')
            luck_pillars_heavenly_stems = [heavenly_stems[(start_index + i) % len(heavenly_stems)] for i in range(10)]
            luck_pillars_earthly_branches = [earthly_branches[(start_branch_index + i) % len(earthly_branches)] for i in range(10)]
        
            luck_pillars_heavenly_stems.reverse()
            luck_pillars_heavenly_stems = luck_pillars_heavenly_stems[1:]
            # luck_pillars_heavenly_stems.reverse()
            luck_pillars_earthly_branches.reverse() 
            luck_pillars_earthly_branches = luck_pillars_earthly_branches[1:]
            # luck_pillars_heavenly_stems.reverse()

        else:
            print('bw')
            luck_pillars_heavenly_stems = [heavenly_stems[(start_index - i) % len(heavenly_stems)] for i in range(10)]
            luck_pillars_earthly_branches = [earthly_branches[(start_branch_index - i) % len(earthly_branches)] for i in range(10)]

            luck_pillars_heavenly_stems.reverse()
            luck_pillars_heavenly_stems = luck_pillars_heavenly_stems[:-1]
            luck_pillars_earthly_branches.reverse() 
            luck_pillars_earthly_branches = luck_pillars_earthly_branches[:-1]
        
        start_day = find_start_day_lp(date_input,is_forward)

        print('is_forward',is_forward)
        print('luck_pillars_heavenly_stems,luck_pillars_earthly_branches,start_day',luck_pillars_heavenly_stems,luck_pillars_earthly_branches,start_day)
        
        return luck_pillars_heavenly_stems,luck_pillars_earthly_branches,start_day

    def get_polarity_element(stem):
        z = df_heavenly[df_heavenly['Heavenly Stem']==stem]
        z = dict(z.iloc[0])
        
        return {
            'stem' : stem,
            'stem_element' : z['Element']
        }

    def update_stem_branch_detail(stem_branch):
        stem_branchs = stem_branch.copy()
        for k in stem_branch:
            z = {}
            if k != 'LunarDate':
                for kk in stem_branch[k]:
                    if kk == 'stem':
                        z.update(get_polarity_element(stem_branch[k][kk]))
                    if kk == 'branch':
                        z['branch'] = stem_branch[k][kk]
                        z['branch_animal'] = df_earthly[df_earthly['Earthly Branch'] == z['branch']].iloc[0]['Animal']
                        z['branch_element'] = df_earthly[df_earthly['Earthly Branch'] == z['branch']].iloc[0]['Element']
                        z['hidden_stem'] = hidden_stems[z['branch']]
                        z['polarity'] = df_earthly[df_earthly['Earthly Branch'] == z['branch']].iloc[0]['Polarity']                 
                stem_branchs[k] = z

        return stem_branchs

    def find_10g(stem_branch,stem):
        hss = stem.split()[0]
        
        hs = stem_branch['Day']['stem']
        df_day = df_heavenly[df_heavenly['Heavenly Stem']==hs]
        ele = df_day.iloc[0]['Element']
        
        df_element_day = df_element[df_element['Self Element']==ele].reset_index(drop=True).T
        df_element_day = df_element_day.rename(columns={0: 'Element'})

        Yin = []
        Yang = []
        for index, row in df_element_day.iterrows():
            yin = df_variant[df_variant['Element']==row['Element']]['Yin Variant'].iloc[0]
            yang = df_variant[df_variant['Element']==row['Element']]['Yang Variant'].iloc[0]
            Yin.append(yin)
            Yang.append(yang)
        df_element_day['Yin'] = Yin
        df_element_day['Yang'] = Yang
        
        df_element_day = df_element_day.drop(index='Self Element')
        df_element_day[['Yin_stem', 'Yin_element']] = df_element_day['Yin'].str.split(' ', expand=True)
        df_element_day[['Yang_stem', 'Yang_element']] = df_element_day['Yang'].str.split(' ', expand=True)
        
        try:
            z = df_element_day[df_element_day['Yin_stem']==hss].index[0]
            yy = 'Yin'
        except:
            z = df_element_day[df_element_day['Yang_stem']==hss].index[0]
            yy = 'Yang'
        tg = five_factor_10gods[z]
        
        zz = df_heavenly[df_heavenly['Heavenly Stem']==stem]
        zz = dict(zz.iloc[0])

        if zz['Polarity'] == 'Yin':
            if stem_branch['Day']['polarity'] == 'Yang':
                zz = tg[1]
            else:
                zz = tg[0]
        else:
            if stem_branch['Day']['polarity'] == 'Yang':
                zz = tg[0]
            else:
                zz = tg[1]
            
        return zz

    def update_10g(stem_branch):
        for k in stem_branch:
            if k != 'LunarDate':
                stem_branch[k]['stem_10g'] = find_10g(stem_branch,stem_branch[k]['stem'])

                G = []
                E = []
                for kk in stem_branch[k]['hidden_stem']:
                    G.append(find_10g(stem_branch,kk))
                    E.append(stem_to_element(kk))
                stem_branch[k]['hidden_stem_10g'] = G
                stem_branch[k]['hidden_stem_element'] = E
        return stem_branch

    def update_lp_10g(lp):
        lps = lp.copy()
        for k in lp.keys():
            lps[k]['stem_10g'] = find_10g(stem_branch,lp[k]['stem'])

            z = []
            E = []
            for kk in lp[k]['hidden_stem']:
                z.append(find_10g(stem_branch,kk))
                E.append(stem_to_element(kk))
            lps[k]['hidden_stem_10g'] = z
            lps[k]['hidden_stem_element'] = E

        return lps

    def stem_to_element(stem):
        z = df_heavenly[df_heavenly['Heavenly Stem']==stem]
        z = dict(z.iloc[0])
        s = ''
        if z['Polarity'] == 'Yin':
            s += '-'
        else:
            s += '+'
        s += z['Element']
        return s

    def find_percen_ele(stem_branch):
        E = []
        for p in ['Year','Month','Day','Hour']:
            E += [stem_branch[p]['stem_element']]
            E += [stem_branch[p]['branch_element']]
            E += [x.replace('-','').replace('+','') for x in stem_branch[p]['hidden_stem_element']]
        count_result = dict(Counter(E))
        print('count_result',count_result)
        total_elements = len(E)
        proportion_result = {key: value / total_elements for key, value in count_result.items()}
        return proportion_result

    # transition day -----
    def find_transition_date(year,month):
        df = pd.read_csv("MonthChangeData.csv")
        y_t,m_t,d_t = year,month,int(df[df['year']==year].iloc[0][f'month_{month}'])
        
        date_str = f"{y_t}-{m_t}-{d_t}"
        formatted_date = datetime.strptime(date_str, '%Y-%m-%d').strftime('%Y-%m-%d')
        return formatted_date

    def find_diff_days(date_input,date_transition):
        date1 = datetime.strptime(date_input, "%Y-%m-%d")
        date2 = datetime.strptime(date_transition, "%Y-%m-%d")        
        difference_days = (date2 - date1).days + 1 
        
        return difference_days
        
    def find_start_day_lp(date_input,is_fw):

        [y,m,d] = [int(x) for x in date_input.split('-')]

        if is_fw: # b) If the Forward cycle is being used, then count the number of days between the person’s Day of Birth and the next monthly transition point.
            m_t = m + 1
            if m_t == 13:
                m_t = 1
                y += 1

            date_transition = find_transition_date(y,m_t)
            diff_day = find_diff_days(date_input,date_transition)

        else:  # a Reverse cycle is used, then count the number of days between the person’s Day of Birth and the nearest monthly transition point
            date_t = find_transition_date(y,m)
            if int(date_input.split('-')[-1]) > int(date_t.split('-')[-1]):
                m_t = m
            else:
                m_t = m - 1

            if m_t == 0:
                m_t = 12
                y -= 1

            date_transition = find_transition_date(y,m_t)
            print('date_transition',date_transition)
            diff_day = find_diff_days(date_transition,date_input)

        print(diff_day)
        start_day = int(diff_day/3)%10
        
        if start_day == 0:
            start_day = 9
        return start_day

    if not time_inputs:
        time_input = '12:00'
    else:
        time_input = time_inputs

    # 4 pillar and 10 gods
    dt = 0
    stem_branch = get_stem_branch_for_date(date_input,time_input,dt)
    stem_branch = update_stem_branch_detail(stem_branch)
    stem_branch = update_10g(stem_branch)

    # luckpillar, 10 gods and age-ranges
    lp = find_luck_pillars(sex,stem_branch)
    start_age = lp[-1]

    numbers = [start_age + i * 10 for i in range(9)]
    ranges = [f"{numbers[i]}-{numbers[i+1]}" for i in range(len(numbers) - 1)]

    ranges = [f"{numbers[i]}-{numbers[i+1]}" for i in range(len(numbers)-1)]
    ranges.append(f"{numbers[-1]}-{numbers[-1] + (numbers[1] - numbers[0])}")
    ranges.reverse()

    # st.write('ranges',ranges)
    # st.write('lp',lp[0])

    
    lp = {
        f'age_{ranges[i]}': {'stem': lp[0][i], 'branch': lp[1][i]} 
        for i in range(len(lp[0]))
    }
    lp = update_stem_branch_detail(lp)
    lp = update_lp_10g(lp)
    

    # percen_elements
    pe = find_percen_ele(stem_branch)

    input_data = {
        'date_input' : date_input,
        'time_input' : time_inputs,
        'sex' : sex
    }

    luck_pillars_list = [
    {"age": key.split("_")[1], **value}
    for key, value in lp.items()
    ]

    results = {
        'input_data' : input_data ,
        'four_pillars' : stem_branch,
        'luck_pillars' : luck_pillars_list,
        'percen_elements' : pe
    }

    if not time_inputs:
        results['four_pillars']['Hour'] = None

    return results

# Earthly Branches data with elements and hidden elements
earthly_data = {
    "Earthly Branch": ["Zi (子)", "Chou (丑)", "Yin (寅)", "Mao (卯)", "Chen (辰)", 
                        "Si (巳)", "Wu (午)", "Wei (未)", "Shen (申)", "You (酉)", 
                        "Xu (戌)", "Hai (亥)"],
    "Element": ["Water", "Earth", "Wood", "Wood", "Earth", 
                     "Fire", "Fire", "Earth", "Metal", "Metal", 
                     "Earth", "Water"],
    "Hidden Elements": ["None", "Metal, Water", "Fire, Earth", "None", "Wood, Water",
                         "Metal, Earth", "Earth", "Wood, Fire", "Water, Earth", "None",
                         "Fire, Metal", "Wood"],
    "Polarity": ["Yang", "Yin", "Yang", "Yin", "Yang",
                 "Yin", "Yang", "Yin", "Yang", "Yin",
                 "Yang", "Yin"],
    "Animal": ["Rat", "Ox", "Tiger", "Rabbit", "Dragon", 
                "Snake", "Horse", "Goat", "Monkey", "Rooster", 
                "Dog", "Pig"]
}

# Heavenly Stems data with elements and polarity
heavenly_data = {
    "Heavenly Stem": ["Jia (甲)", "Yi (乙)", "Bing (丙)", "Ding (丁)", "Wu (戊)", 
                       "Ji (己)", "Geng (庚)", "Xin (辛)", "Ren (壬)", "Gui (癸)"],
    "Element": ["Wood", "Wood", "Fire", "Fire", "Earth", 
                "Earth", "Metal", "Metal", "Water", "Water"],
    "Polarity": ["Yang", "Yin", "Yang", "Yin", "Yang",
                 "Yin", "Yang", "Yin", "Yang", "Yin"]
}

hidden_stems = {
    'Zi (子)': ['Gui (癸)'],
    'Chou (丑)': ['Ji (己)', 'Gui (癸)', 'Xin (辛)'],
    'Yin (寅)': ['Jia (甲)', 'Bing (丙)', 'Wu (戊)'],
    'Mao (卯)': ['Yi (乙)'],
    'Chen (辰)': ['Wu (戊)', 'Yi (乙)', 'Gui (癸)'],
    'Si (巳)': ['Bing (丙)', 'Wu (戊)', 'Geng (庚)'],
    'Wu (午)': ['Ding (丁)', 'Ji (己)'],
    'Wei (未)': ['Ji (己)', 'Ding (丁)', 'Yi (乙)'],
    'Shen (申)': ['Geng (庚)', 'Ren (壬)', 'Wu (戊)'],
    'You (酉)': ['Xin (辛)'],
    'Xu (戌)': ['Wu (戊)', 'Xin (辛)', 'Ding (丁)'],
    'Hai (亥)': ['Ren (壬)', 'Jia (甲)']
}

df_earthly = pd.DataFrame(earthly_data)
df_heavenly = pd.DataFrame(heavenly_data)

# df_element
headers = ["Self Element", "Influence Element", "Wealth Element", "Resource Element", "Output Element", "Companion Element"]
data = [
    ["Wood", "Metal", "Earth", "Water", "Fire", "Wood"],
    ["Water", "Earth", "Fire", "Metal", "Wood", "Water"],
    ["Fire", "Water", "Metal", "Wood", "Earth", "Fire"],
    ["Metal", "Fire", "Wood", "Earth", "Water", "Metal"],
    ["Earth", "Wood", "Water", "Fire", "Metal", "Earth"]
]
df_element = pd.DataFrame(data, columns=headers)

# df_variant
headers = ["Element", "Yang Variant", "Yin Variant"]
data = [
    ["Wood", "Jia Wood", "Yi Wood"],
    ["Fire", "Bing Fire", "Ding Fire"],
    ["Earth", "Wu Earth", "Ji Earth"],
    ["Metal", "Geng Metal", "Xin Metal"],
    ["Water", "Ren Water", "Gui Water"]
]
df_variant = pd.DataFrame(data, columns=headers)

five_factor_10gods = {
    'Output Element' : ['EG','HO'],
    'Wealth Element' : ['IW','DW'],
    'Influence Element' : ['7K','DO'],
    'Resource Element' : ['IR','DR'],
    'Companion Element' : ['F','RW']
}

heavenly_stems = list(df_heavenly['Heavenly Stem'])
earthly_branches = list(df_earthly['Earthly Branch'])
reference_date = datetime(1900, 1, 31)  # 📌 1900-01-31 is Jia Chen (甲辰)
dt = 0


def next_week(date_input):

    # Get list of dates from next Monday to next Sunday
    start_date = datetime.strptime(date_input, "%Y-%m-%d")
    days_ahead = 7 - start_date.weekday()  # 0 = Monday, ..., 6 = Sunday
    next_monday = start_date + timedelta(days=days_ahead)
    next_week = [(next_monday + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(7)]
    print(next_week)

    week_days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

    results_nextweek = {}
    for i,date_input in enumerate(next_week):
        time_input = "07:09"
        sex = 'male'
        result = AllBaziCalulate(date_input,time_input,sex)
        
        if i == 0:
            data = result['four_pillars']['Month']
            filtered_data = {k: data[k] for k in ['stem','branch'] if k in data}
            results_nextweek['Month'] = filtered_data
            
            data = result['four_pillars']['Year']
            filtered_data = {k: data[k] for k in ['stem','branch'] if k in data}
            results_nextweek['Year'] = filtered_data
            
        data = result['four_pillars']['Day']
        filtered_data = {k: data[k] for k in ['stem','branch'] if k in data}
        results_nextweek[date_input] = filtered_data
        results_nextweek[date_input]['day'] = week_days[i]
        
    return results_nextweek


current_date = st.text_input("current_date:", value=date.today())
results_nextweek = next_week(current_date)
st.write(results_nextweek)