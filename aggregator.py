# -*- coding: utf-8 -*-
import sys, re
from datetime import datetime
import dateutil.relativedelta



def main():
    #formating
    users_list = [] 
    formating_users_list = []
    temp = 0
    
    #reading file
    list_lines = [] #all lines as elements of the list
    
    #commit counter
    list_unique_commits = []
    list_all_commits = []

    reading_file(list_lines) 

    one_user_commits_counter(list_unique_commits, list_all_commits, list_lines)
    
    
def reading_file(lines):
    
    with open(sys.argv[1]) as f: #reading file
        for line in f: #creating list
            lines.append(line) 
    f.close()

def one_user_commits_counter(unique_commits_list, all_commits_list, lines_list):
    com_count_list = [] #commits list
    all_coms_count = 0 #all commits count

    #everyone commit in the individual list. All commints are in the main commit list
    for line in lines_list: 
        if (line != '--\n'): #if not '--' 
            unique_commits_list.append(line)
            if line == lines_list[-1]: #for revno:1
                all_commits_list.append(unique_commits_list)
                unique_commits_list = []
        else:
            all_commits_list.append(unique_commits_list) 
            unique_commits_list = []

    #comms count
    for com_list in all_commits_list: 
        for com in com_list:
            if re.search('revno:', com) and (com not in com_count_list):
                com_count_list.append(com)
    all_coms_count = int(len(com_count_list)) 
    
    #creating dicts
    users_and_commits_and_timestamp = []

    triple_list = [] #committer and commit list

    #committer and commit couples list creating
    for com_list in all_commits_list: 
        for com in com_list:
            last = com_list[-1] #end of com_list
            if re.search('revno:', com) and (com not in unique_commits_list):
                unique_commits_list.append(com.replace('revno: ','').replace('\n', ''))
                break
            if (re.search('revno:', com))==None and com == last:
                unique_commits_list.append('commit wasn`t found')

        for com in com_list:
            last = com_list[-1] #end of com_list
            if re.search('committer:', com) and (com not in unique_commits_list):
                unique_commits_list.append(com.replace('committer: ','').replace('\n', ''))
                break
            if (re.search('committer:', com))== None and com == last:
                unique_commits_list.append('committer wasn`t found')
        
        for com in com_list:
            last = com_list[-1] #end of com_list
            if re.search('timestamp:', com) and (com not in unique_commits_list):
                com = com.replace('timestamp: ', '').replace(r'\n', '')
                com = str(com[:-6])
                #print len(com)
                com = datetime.strptime(com, '%a %Y-%m-%d %H:%M:%S ')
                unique_commits_list.append(com)
                break
            if (re.search('timestamp:', com))== None and com == last:
                unique_commits_list.append('timestamp wasn`t found')


        triple_list.append(unique_commits_list)
        unique_commits_list = []
    
    #committer and commit couples dict creating
    for triple in triple_list:
        users_and_commits_and_timestamp.append(triple)
    
    triple_list = [] #deleting data
    

    #all users list creating
    all_users_list = []
    for triple in users_and_commits_and_timestamp:
        if triple[1] not in all_users_list:
            all_users_list.append(triple[1])
    
           
    #TASK 1 all time commits dict for everyone user
    result_counts_dict = {}
    coms_count = 0
    for user in all_users_list:
        for com_list in all_commits_list:
            for com in com_list:
                if re.search('committer:', com):
                    if com.replace('committer: ','').replace('\n', '') == user:
                        
                        coms_count += 1
        result_counts_dict.update({user : coms_count})
        coms_count = 0

    #console output
    for key in result_counts_dict.keys():
        for value in result_counts_dict.values():
            if result_counts_dict[key]==value:
                print 'Коммитер', key, 'закоммитил за всё время', value, 'раз\n'
                print 'Процент от общего количества коммитов составляет: ', value*100/all_coms_count, '%\n'
                print '------------------------------------------------------\n'
               
    #file output
    f = open('result_first_task.txt','w')
    for key in result_counts_dict.keys():
        for value in result_counts_dict.values():
            if result_counts_dict[key]==value:
                f.writelines('Коммитер '+ str(key) +' закоммитил за всё время ' + str(value) +' раз\n')
                f.writelines('Процент от общего количества коммитов составляет: ' + str(value*100/all_coms_count)+ '%\n')
                f.writelines('------------------------------------------------------\n')
    f.close()

    #all users list
    f = open('all_users_list.txt','w')
    for user in all_users_list:
        f.writelines(user + '\n')
    f.close()

    #TASK 2 for everything year
    year_coms_counter = 0 #for everyone user
    years_list = [] #list of all years
    result_years_list = []
    unique_year_committers_list = [] #all users dicts for one year
    unique_year_committers_dict = {} #dict for everyone user
    
    #unique years
    for unique in users_and_commits_and_timestamp:
        if (unique[2] == 'timestamp wasn`t found'):
            pass 
        elif unique[2].year not in years_list:
            years_list.append(unique[2].year)

    years_list = sorted(years_list)

    #commits formated
    formated_commits_list = []
    for com in com_count_list:
        formated_commits_list.append(com.replace('revno: ','').replace('\n', ''))

    for select_year in years_list:
        #print select_year
        for committer in result_counts_dict.keys():
            for value in users_and_commits_and_timestamp:
                if value[1] == committer:
                    if value[2] != 'timestamp wasn`t found': 
                        if value[2].year == select_year:
                            year_coms_counter += 1
                            if value[1] not in unique_year_committers_dict:
                                unique_year_committers_dict.update({value[1] : year_coms_counter})
                                                                
                            else:
                                unique_year_committers_dict[value[1]] = year_coms_counter
                    else: without_timestamp = value[0]                                
            year_coms_counter = 0
                            
              
        unique_year_committers_list.append(unique_year_committers_dict)       
        unique_year_committers_dict = {}
        unique_year_committers_list.append(select_year) #last element
        result_years_list.append(unique_year_committers_list)
        unique_year_committers_list = []              
    
    #commits count for everthing year
    commits_for_everything_year = {}
    sum_commits = 0

    for year in result_years_list:
        for value in year[0].values():
            sum_commits+=value
        commits_for_everything_year.update({year[1] : sum_commits})    
    #print (commits_for_everything_year)
    
    #console output
    for dict_or_year in result_years_list:
        for key, value in dict_or_year[0].items():
            if dict_or_year[0][key] == value:
                print 'Коммитер ', key, ' закоммитил за ', dict_or_year[1], '-ый год ', value, ' раз\n'
                print 'Процент от общего количества коммитов составляет: ', value*100/commits_for_everything_year[dict_or_year[1]], '%\n'
                print '------------------------------------------------------\n'

    #file output
    f = open('result_second_task.txt','w')
    for dict_or_year in result_years_list:
        for key, value in dict_or_year[0].items():
            if dict_or_year[0][key] == value:
                f.writelines('Коммитер '+ str(key)+ ' закоммитил за '+ str(dict_or_year[1]) + '-ый год '+ str(value) + ' раз\n')
                f.writelines('Процент от общего количества коммитов составляет: '+ str(value*100/commits_for_everything_year[dict_or_year[1]])+ '%\n')
                f.writelines('------------------------------------------------------\n')
    f.close()
    # print result_years_list
    #print 'Commit ', without_timestamp, ' without timestamp'

    #TASK 3 for last 3 months
    users_and_commits_and_timestamp_last_three_month = []

    last_commit_date = None # last commit date
    triple = users_and_commits_and_timestamp[0]
    last_commit_date = triple[2]
    
    three_months_ago = last_commit_date - dateutil.relativedelta.relativedelta(months=3)

    #Three months ago
    for index in range(0, len(users_and_commits_and_timestamp)):
        for triple in users_and_commits_and_timestamp:            
            if triple[2] == three_months_ago:
                break
            else:
                if users_and_commits_and_timestamp[index] == triple:
                    temp_triple = users_and_commits_and_timestamp[index+1]
                    if (triple[2].day - three_months_ago.day) <= (three_months_ago.day - temp_triple[2].day) and three_months_ago.month == triple[2].month and three_months_ago.year == triple[2].year:
                        three_months_ago = triple[2]
                        break
                    
    #creating formated triples list
    for triple in users_and_commits_and_timestamp:
        if triple[2] == three_months_ago:
            users_and_commits_and_timestamp_last_three_month.append(triple)
            break
        else: 
            if triple[2] != three_months_ago:
                users_and_commits_and_timestamp_last_three_month.append(triple)
                   
    #print users_and_commits_and_timestamp_last_three_month


    #TASK 3
    result_three_months_dict = {}
    three_months_coms_counter = 0 #for everyone user
    
    unique_three_months_committers_list = [] #all users dicts for one year
    unique_three_months_committers_dict = {} #dict for everyone user

    
        
    for committer in result_counts_dict.keys():
        for value in users_and_commits_and_timestamp_last_three_month:
            if value[1] == committer:
                if value[2] != 'timestamp wasn`t found': 
                    three_months_coms_counter += 1
                    if value[1] not in unique_three_months_committers_dict:
                        unique_three_months_committers_dict.update({value[1] : three_months_coms_counter})
                                                                
                    else:
                        unique_three_months_committers_dict[value[1]] = three_months_coms_counter
                else: without_timestamp = value[0]                                
        three_months_coms_counter = 0
                            
              
    unique_three_months_committers_list.append(unique_three_months_committers_dict)       
    
   
    result_three_months_dict = unique_three_months_committers_dict
    unique_three_months_committers_dict = {}
    unique_three_months_committers_list = []

    #output console
    three_month_sum_commits = 0
    for value in result_three_months_dict.values():
        three_month_sum_commits += value
    for key in result_three_months_dict.keys():
        print 'Коммитер ', key, ' закоммитил за последние 3 месяца ', result_three_months_dict[key] , ' раз\n'
        print 'Процент от общего количества коммитов составляет: ', result_three_months_dict[key]*100/three_month_sum_commits, '%\n'
        print '------------------------------------------------------\n'

    #output file
    f = open('result_third_task', 'w')
    for key in result_three_months_dict.keys():
        f.writelines('Коммитер '+ str(key)+ ' закоммитил за последние 3 месяца ' + str(result_three_months_dict[key]) + ' раз\n')
        f.writelines('Процент от общего количества коммитов составляет: '+ str(result_three_months_dict[key]*100/three_month_sum_commits) + '%\n')
        f.writelines('------------------------------------------------------\n')
    f.close()    
if __name__ == '__main__':
    main()
