#################################
##### Name: Xinyu Ma
##### Uniqname: xinyuma
#################################

from bs4 import BeautifulSoup
import requests
import json
import secrets # file that contains your API key
import plotly.graph_objs as go
import sqlite3
import numpy as np
import math

CACHE_FILENAME = "final_project_cache.json"
CACHE_DICT = {}

client_key = secrets.API_KEY



class NationalSite:
    '''a national site
    Instance Attributes
    -------------------
    category: string
        the category of a national site (e.g. 'National Park', '')
        some sites have blank category.
    
    name: string
        the name of a national site (e.g. 'Isle Royale')
    address: string
        the city and state of a national site (e.g. 'Houghton, MI')
    zipcode: string
        the zip-code of a national site (e.g. '49931', '82190-0168')
    phone: string
        the phone of a national site (e.g. '(616) 319-7906', '307-344-7381')
    '''
    def __init__(self,category="no category",name="no name",address="no address",
                zipcode="no zip",phone="no phone",parkCode="no parkCode"):
        self.category = category
        self.name = name
        self.address = address
        self.zipcode = zipcode
        self.phone = phone
        self.parkCode = parkCode
    def info(self):
        return self.name + " (" + self.phone + "): " + self.address + " " + self.zipcode

def open_cache():
    ''' Opens the cache file if it exists and loads the JSON into
    the CACHE_DICT dictionary.
    if the cache file doesn't exist, creates a new cache dictionary
    
    Parameters
    ----------
    None
    
    Returns
    -------
    The opened cache: dict
    '''
    try:
        cache_file = open(CACHE_FILENAME, 'r')
        cache_contents = cache_file.read()
        cache_dict = json.loads(cache_contents)
        cache_file.close()
    except:
        cache_dict = {}
    return cache_dict


def save_cache(cache_dict):
    ''' Saves the current state of the cache to disk
    
    Parameters
    ----------
    cache_dict: dict
        The dictionary to save
    
    Returns
    -------
    None
    '''
    dumped_json_cache = json.dumps(cache_dict)
    fw = open(CACHE_FILENAME,"w")
    fw.write(dumped_json_cache)
    fw.close() 


def request_with_cache(url):
    ''' If URL in cache, retrieve the corresponding values from cache. Otherwise, connect to API again and retrieve from API.
    
    Parameters
    ----------
    url: string
        a URL
    
    Returns
    -------
    a string containing values of the URL from cache or from API
    '''
    cache_dict = open_cache()
    if url in cache_dict.keys():
        print("Using Cache")
        response = cache_dict[url]
    else:
        print("Fetching")
        response = requests.get(url).text # need to append .text, otherwise, can't save a Response object to dict
        cache_dict[url] = response # save all the text on the webpage as strings to cache_dict
        save_cache(cache_dict)
    return response


def build_state_url_dict():
    ''' Make a dictionary that maps state name to state page url from "https://www.nps.gov"
    Parameters
    ----------
    None
    Returns
    -------
    dict
        key is a state name and value is the url
        e.g. {'michigan':'https://www.nps.gov/state/mi/index.htm', ...}
    '''
    state_info = "state"
    res = {}
    ls_of_href=[]
    ls_of_state=[]
    baseurl = 'https://www.nps.gov'
    response = request_with_cache(baseurl)
    # if state_info in cache_dict.keys():
    #     print("Using cache")
    # else:
    #     print("Fetching")
    # html = requests.get('https://www.nps.gov').text
    soup = BeautifulSoup(response, 'html.parser')
    search_div = soup.find(id='HERO')
    find_ul = search_div.find(name = 'ul')
    find_li = find_ul.find_all('li')
    for k in find_li:
        x = k.find_all('a')
        ls_of_href.append(x[0]['href'])
    for li in find_li:
        ls_of_state.append(li.string.lower())
    for i in range(56):
        res[ls_of_state[i]] = baseurl + ls_of_href[i]
    return res
       

def get_site_instance(site_url):
    '''Make an instances from a national site URL.
    
    Parameters
    ----------
    site_url: string
        The URL for a national site page in nps.gov
    
    Returns
    -------
    instance
        a national site instance
    '''
    
    # html = requests.get(site_url).text
    global address1
    global address2
    global zipcode
    response = request_with_cache(site_url)
    soup = BeautifulSoup(response, 'html.parser')
    search_div = soup.find(id='HeroBanner')
    find_name = search_div.find('a') #name!
    name = find_name.string
    find_category = search_div.find('span')
    category = find_category.string #category
    search_foot = soup.find(id='ParkFooter')
    find_add = search_foot.find_all('span')
    for i in find_add:
        if i.find(itemprop="addressLocality") is not None:
            address1 = i.find(itemprop="addressLocality").string
        if i.find(itemprop="postalCode") is not None:
            zipcode = i.find(itemprop="postalCode").string.strip()
        if i.find(itemprop="addressRegion") is not None:
            address2 = i.find(itemprop="addressRegion").string
    address = address1 + ", " + address2
    find_phone = search_foot.find_all('span',itemprop="telephone")
    phone = find_phone[0].string.strip()

    parkCode = site_url.split('/')[3]
    if category == None:
        category = "no category"
    site1 = NationalSite(category,name,address,zipcode,phone,parkCode) 
    
    return site1


def get_sites_for_state(state_url):
    '''Make a list of national site instances from a state URL.
    
    Parameters
    ----------
    state_url: string
        The URL for a state page in nps.gov
    
    Returns
    -------
    list
        a list of national site instances
    '''
    ls_of_url = []
    ls_of_national_site = []
    response = request_with_cache(state_url)
    soup = BeautifulSoup(response, 'html.parser')

    search_div = soup.find_all('div', class_= 'col-md-9 col-sm-9 col-xs-12 table-cell list_left')
    for i in search_div:
        find_url = i.find_all('a')
        ls_of_url.append("https://www.nps.gov" + find_url[0]["href"]+ "index.htm")
    for each_park_url in ls_of_url:
        fetch_part2 = get_site_instance(each_park_url)
        # print("[" + str(count) + "] " + fetch_part2.info())
        ls_of_national_site.append(fetch_part2)
            # break
    return ls_of_national_site


def get_topics(site_object):
    '''Obtain API data from MapQuest API.
    
    Parameters
    ----------
    site_object: object
        an instance of a national site
    
    Returns
    -------
    dict
        a converted API return from MapQuest API
    '''
    # global flag2
    cache_dict = open_cache()

    endpoint_url = 'https://developer.nps.gov/api/v1/parks?'
    params = {"parkCode": site_object.parkCode, "api_key": client_key}
    if str(site_object.parkCode) in cache_dict:
        print("Using Cache")
        response = cache_dict[str(site_object.parkCode)]       
    else:
        print("Fetching")
        response = requests.get(endpoint_url, params=params).json()
        cache_dict[str(site_object.parkCode)] = response
        save_cache(cache_dict)
    count = 1
    print()
    # print('[name]: ' + self.name)
    print("# Topics in " + str(site_object.name + ': '),end='')
    for each_topic in response["data"][0]["topics"]:
        print('(' + str(count) + ')' + each_topic["name"]+' ',end='')
        count += 1
    print()
    print('# email-contact: ' + response['data'][0]['contacts']['emailAddresses'][0]['emailAddress'])
    print('# website: ' + response['data'][0]['directionsUrl'])
    print('# total acres: ' + str(get_park_acre(site_object.parkCode)[0][1]))
    print('# number of fire happened in past 120 years: ' + str(get_park_acre(site_object.parkCode)[0][2]))
    if get_park_acre(site_object.parkCode)[0][2] == 0:
        flag2 = 1
    return response

def get_park_acre(parkCode):
    ''' Constructs and executes SQL query to retrieve acre info from the park table.
    
    Parameters
    ----------
    park_name: string.
        The unique code(primary key) of the park.
    
    Returns
    -------
    list
        a list of tuples that represent the query result
    '''
    connection = sqlite3.connect("wildland_fire.sqlite")
    cursor = connection.cursor()
    query = '''SELECT UnitName, acres, COUNT(OBJECTID) FROM parks, fire 
                WHERE parks.parkCode = fire.Unitcode
                AND parks.parkCode LIKE ?'''
    result = cursor.execute(query,(parkCode,)).fetchall()
    connection.close() 
    return result

def get_N_plot_fire_times(parkCode):
    ''' Constructs and executes SQL query to retrieve conservation info from the fire table.
    Plot a bar chart showing the number of fire happened in every 20 years.
    
    Parameters
    ----------
    parkCode: string.
        The unicode of the park.
    
    Returns
    -------
    None
    '''
    connection = sqlite3.connect("wildland_fire.sqlite")
    cursor = connection.cursor()
    parkCode = "'" + parkCode.upper() + "'"
    query = '''SELECT count(*) from fire
                where UnitCode={}
                AND FireDiscoveryDateTime BETWEEN ? AND ? ''' .format(parkCode) # use square bracket to escape the space in column name
    ls_of_start =['1900-01-01','1920-01-02','1940-01-02','1960-01-02','1980-01-02','2000-01-02']
    ls_of_end = ['1920-01-01','1940-01-01','1960-01-01','1980-01-01','2000-01-01','2021-05-05',]
    count_result = []
    for i in range(len(ls_of_end)):    
        result = cursor.execute(query,(ls_of_start[i],ls_of_end[i])).fetchall()
        count_result.append(result)
    # print(count_result)
    query1 = '''SELECT count(*) from fire
                where FireDiscoveryDateTime BETWEEN ? AND ? ''' 
    total_count = []
    for i in range(len(ls_of_end)):
        result1 = cursor.execute(query1,(ls_of_start[i],ls_of_end[i])).fetchall()
        total_count.append(result1)

    connection.close()
    flag = []
    for i in count_result:
        flag.append(i[0][0])
    if len(set(flag)) == 1:
        print("Sorry for inconvenience, we have no fire info about this park, please back to find another one!")
        print()
    else:
        xvals = ['1900-1920','1920-1940','1940-1960','1960-1980','1980-2000','2000-2021']
        yvals = []
        yvals_avg = []
        for i in count_result:
            yvals.append(i[0][0])
        for i in total_count:
            yvals_avg.append(int(i[0][0]/298))
        fig = go.Figure()
        fig.add_trace(go.Bar(x=xvals,y=yvals,text=yvals,textposition='auto',name='park fire times',marker_color='indianred'))
        fig.add_trace(go.Bar(x=xvals,y=yvals_avg,text=yvals_avg,textposition='auto',name='avg of all parks fire times',marker_color='lightsalmon'))
        fig.update_layout(barmode='group',xaxis_tickangle=-45,title_text='Number of fire happened with interval of 20 years')
        fig.show()

def get_n_plot_fire_cause(parkCode):
    ''' Constructs and executes SQL query to retrieve conservation info from the fire table.
    Plot a pie chart showing the cause of fire.
    
    Parameters
    ----------
    parkCode: string.
        The unicode of the park.
    
    Returns
    -------
    None
    '''
    connection = sqlite3.connect("wildland_fire.sqlite")
    cursor = connection.cursor()
    parkCode = "'" + parkCode.upper() + "'"
    query2 = '''SELECT FireCause from fire, parks
                where fire.UnitCode = parks.parkCode
                AND UnitCode={}''' .format(parkCode.upper())
    result2 = cursor.execute(query2).fetchall()
    connection.close()
    if len(result2) == 0:
        print("Sorry for inconvenience, we have no fire info about this park, please back to find another one!")
        print()
    else:
        human_count = 0
        natural_count = 0
        unknown_count = 0 
        for i in result2:
            if i[0] == 'Human':
                human_count += 1
            elif i[0] == 'Natural':
                natural_count += 1
            else:
                unknown_count += 1
        labels = ['Human','Natural','Unknown']
        values = [human_count,natural_count,unknown_count]
        pie_data = go.Pie(labels = labels, values = values)
        basic_layout = go.Layout(title = "Percentage of fire cause")
        fig = go.Figure(data = pie_data, layout = basic_layout)
        fig.show()

def get_n_plot_size_class(parkCode):
    ''' Constructs and executes SQL query to retrieve conservation info from the fire table.
    Plot a scatter figure showing the size class of every fire happening.
    
    Parameters
    ----------
    parkCode: string.
        The unicode of the park.
    
    Returns
    -------
    None
    '''
    connection = sqlite3.connect("wildland_fire.sqlite")
    cursor = connection.cursor()
    parkCode = "'" + parkCode.upper() + "'"
    query3 = '''SELECT SizeClass from fire, parks
                where fire.UnitCode = parks.parkCode
                AND UnitCode={}''' .format(parkCode.upper())
    result3 = cursor.execute(query3).fetchall()
    connection.close()
    if len(result3) == 0:
        print("Sorry for inconvenience, we have no fire info about this park, please back to find another one!")
        print()
    else:
        A_count = 0
        B_count = 0
        C_count = 0 
        D_count = 0 
        E_count = 0 
        F_count = 0 
        G_count = 0 
        N_count =0
        for i in result3:
            if i[0] == 'A':
                A_count += 1
            elif i[0] == 'B':
                B_count += 1
            elif i[0] == 'C':
                C_count += 1
            elif i[0] == 'D':
                D_count += 1
            elif i[0] == 'E':
                E_count += 1
            elif i[0] == 'F':
                F_count += 1
            elif i[0] == 'G':
                G_count += 1
            else:
                N_count += 1
        xvals = ['A','B','C','D','E','F','G','N']
        yvals = [A_count,B_count,C_count,D_count,E_count,F_count,G_count,N_count]
        scatter_data = go.Scatter(x=xvals,y=yvals,mode='markers',marker={'symbol':'star','size':35})
        basic_layout=go.Layout(title="size class of fire")
        fig = go.Figure(data=scatter_data, layout = basic_layout)
        fig.show()
def get_n_plot_final_acres(parkCode):
    connection = sqlite3.connect("wildland_fire.sqlite")
    cursor = connection.cursor()
    parkCode = "'" + parkCode.upper() + "'"
    query = '''SELECT Avg(FinalAcres) from fire
                where UnitCode={}
                AND FireDiscoveryDateTime BETWEEN ? AND ? ''' .format(parkCode) # use square bracket to escape the space in column name
    ls_of_start =['1900-01-01','1920-01-02','1940-01-02','1960-01-02','1980-01-02','2000-01-02']
    ls_of_end = ['1920-01-01','1940-01-01','1960-01-01','1980-01-01','2000-01-01','2021-05-05',]
    count_result = []
    for i in range(len(ls_of_end)):    
        result = cursor.execute(query,(ls_of_start[i],ls_of_end[i])).fetchall()
        count_result.append(result)
    
    query1 ='''SELECT avg(FinalAcres) from fire, parks
                WHERE fire.UnitCode = parks.parkCode
                AND FireDiscoveryDateTime BETWEEN ? AND ? '''
    avg_acres = []
    for i in range(len(ls_of_end)):    
        result1 = cursor.execute(query1,(ls_of_start[i],ls_of_end[i])).fetchall()
        avg_acres.append(result1)
    connection.close()
    flag = []
    for i in count_result:
        flag.append(i[0][0])
    if len(set(flag)) == 1:
        print("Sorry for inconvenience, we have no fire info about this park, please back to find another one!")
        print()
    else:
        xvals = ['1900-1920','1920-1940','1940-1960','1960-1980','1980-2000','2000-2021']
        yvals = []
        yvals_avg = []
        count_result = np.array(count_result)
        for i in count_result:
            if i[0][0] == None:
                i[0][0] = 0
                yvals.append(i[0][0])
            else:
                yvals.append(math.ceil(i[0][0]))
        for i in avg_acres:
            yvals_avg.append(math.ceil(i[0][0]))
        fig = go.Figure()
        fig.add_trace(go.Bar(x=xvals,y=yvals,text=yvals,textposition='auto',name='park fire acres',marker_color='green'))
        fig.add_trace(go.Bar(x=xvals,y=yvals_avg,text=yvals_avg,textposition='auto',
                            name='Average of all parks fire acres',marker_color='blue'))
        fig.update_layout(barmode='group',xaxis_tickangle=-45,title_text='Average of fire acres happened with interval of 20 years')
        fig.show()




if __name__ == "__main__":
    flag = 0
    this_url = build_state_url_dict()
    while True:
        user_input = input("Enter a state name to see the parks (e.g. Michigan, michigan) or 'exit': ")
        if user_input == 'exit':
            break
        elif user_input.lower() not in this_url.keys():
            print("[Error] Enter proper state name")
            continue
        else:
            ls_of_instance = []
            that_url = this_url[user_input.lower()]
            ls_of_park = get_sites_for_state(that_url)
            print("----------------------------------")
            print("List of national sites in " + user_input.lower())
            print("----------------------------------")
            count = 1
            for i in ls_of_park:
                print("[" + str(count) + "] " + i.info())
                count += 1
                ls_of_instance.append(i)

            while True:
                flag2 = 0
                user_input2 = input("Choose the number for parks info or input 'exit', 'back' to turn to another park info: ")
                if user_input2.isdigit():
                    if int(user_input2) > count-1 or int(user_input2) <= 0:
                        print("[Error] Invalid input")
                        print()
                        print("-------------------------------")
                    else:
                        site_object = ls_of_instance[int(user_input2)-1]                    
                        get_topics(site_object)
                        print()
                        while True:
                            user_input3 = input("Please enter the fire plot you wanna look at or 'exit' or 'back'.\
                                \n(A.Number of fire happened B.Fire cause C.Fire size class D.Fire final acres): ")
                            
                            if user_input3 == 'A' or user_input3 == 'a':
                                get_N_plot_fire_times(site_object.parkCode)
                            elif user_input3 == 'B' or user_input3 == 'b':
                                get_n_plot_fire_cause(site_object.parkCode)
                            elif user_input3 == 'C' or user_input3 == 'c':
                                get_n_plot_size_class(site_object.parkCode)
                            elif user_input3 == 'D' or user_input3 == 'd':
                                get_n_plot_final_acres(site_object.parkCode)
                            elif user_input3 == 'exit':
                                flag = 1
                                break
                            elif user_input3 == 'back':
                                break
                            else:
                                print()
                                print("invalid input. Please enter A,B,C,D,'exit','back'")
                                print("-------------------------------")
                    if flag == 1:
                        break
                elif user_input2 == "back":
                    break
                elif user_input2 == "exit":
                    flag = 1
                    break
                else:
                    print("[Error] Invalid input")
                    print()
                    print("-------------------------------")
                
        if flag == 1:
            break