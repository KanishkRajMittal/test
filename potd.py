import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from bs4 import BeautifulSoup
import requests
import datetime
import pytz
from time import sleep
from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from datetime import date
from bs4 import BeautifulSoup
import requests
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore


count=1

def keep_numeric_digits(input_string):
    return ''.join(char for char in input_string if char.isdigit())



def leetcode(handle):
    d={}
    d["Handle"]=handle
    url = "https://leetcode.com/"+handle+"/"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')

    # community stats
    community_stats=soup.find_all(class_='flex items-center space-x-2 text-[14px]')
    views=community_stats[0].text
    for i in range(len(views)):
        if views[i].isdigit():
            break;
    views=views[i:]
    solution=community_stats[1].text
    for i in range(len(solution)):
        if solution[i].isdigit():
            break;
    solution=solution[i:]
    Discuss=community_stats[2].text
    for i in range(len(Discuss)):
        if Discuss[i].isdigit():
            break;
    Discuss=Discuss[i:]
    Reputation=community_stats[3].text
    for i in range(len(Reputation)):
        if Reputation[i].isdigit():
            break;
    Reputation=Reputation[i:]
    d["Community_Stats"]={"Views":views,"Solution":solution,"Discuss":Discuss,"Reputation":Reputation}

    #Ratings and stuff
    rating = soup.find(class_='text-label-1 dark:text-dark-label-1 flex items-center text-2xl').text
    global_rank_contest_attempted = soup.find_all(class_='text-label-1 dark:text-dark-label-1 font-medium leading-[22px]')
    # rating_percentile = soup.find('div', {'class': 'text-label-1 dark:text-dark-label-1 text-2xl'}).text
    no_ques_solve = soup.find(class_='text-[24px] font-medium text-label-1 dark:text-dark-label-1').text
    type_ques_solve=soup.find_all(class_='mr-[5px] text-base font-medium leading-[20px] text-label-1 dark:text-dark-label-1')
    no_of_badges=soup.find(class_='text-label-1 dark:text-dark-label-1 mt-1.5 text-2xl leading-[18px]').text

    no_easy_ques_solve=int(type_ques_solve[0].text)
    no_med_ques_solve=int(type_ques_solve[1].text)
    no_diff_ques_solve=int(type_ques_solve[2].text)

    global_rank_contest = global_rank_contest_attempted[0].text
    contest_attempted = int(global_rank_contest_attempted[1].text)

    d["Current_Rating"]=rating
    d["Global_Rank_In_Contest"] = global_rank_contest
    d["Contest_Attempted"] =contest_attempted
    # print("Rating Precentile = ",rating_percentile)
    d["Number_Of_Ques_solved"] = no_ques_solve
    d["Easy_Ques_Solved"]=no_easy_ques_solve
    d["Medium_Ques_Solved"]= no_med_ques_solve
    d["Difficult_Ques_Solved"] = no_diff_ques_solve
    d["Number_Of_Badges"]= no_of_badges
    return d

def codeforces(handle):
    d={}
    d["Handle"]=handle
    url='https://codeforces.com/api/user.info?handles='+handle
    response=requests.get(url)

    if response.status_code != 200:
        raise print('User not Found')

    profile=response.json()["result"][0]
    contributions=profile["contribution"]
    rating=profile["rating"]
    No_of_friends=profile["friendOfCount"]
    Rank=profile["rank"]
    max_rating=profile["maxRating"]
    max_rank=profile["maxRank"]

    d["Number_Of_Contributions"]=contributions
    d["Current_Rating"]=rating
    d["Number_Of_Friends"]=No_of_friends
    d["Current_Rank"]=Rank
    d["Max_Rating"]=max_rating
    d["Max_Rank"]=max_rank

    url="https://codeforces.com/profile/"+handle
    response=requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    problem_solved=soup.find_all(class_='_UserActivityFrame_counterValue')
    No_of_ques_solve=problem_solved[0].text
    max_streak=problem_solved[3].text
    d["Number_Of_Ques_solved"] = keep_numeric_digits(No_of_ques_solve)
    d["Max_Streak"]=max_streak
    return d


def gfg(handle):
    url = "https://auth.geeksforgeeks.org/user/"+handle+"/?utm_source=geeksforgeeks&utm_medium=my_profile&utm_campaign=auth_user"
    response=requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    # rank=soup.find(class_='rankNum').text
    POTD_streak=soup.find(class_='streakCnt tooltipped').text
    Institute=soup.find(class_='basic_details_data').text
    score_card=soup.find_all(class_='score_card_value')
    Coding_score=score_card[0].text
    problem_solved=score_card[1].text
    monthly_coding_score=score_card[2].text

    # Find the tabs containing the number of questions for each difficulty
    tabs = soup.find_all('li', class_='tab')
    # Create a dictionary to store the count for each difficulty
    difficulty_count = {'easy': 0, 'medium': 0, 'hard': 0}
    for tab in tabs:
        # Extract the difficulty level and count from the 'href' attribute
        difficulty = tab.find('a')['href'].replace('#', '')
        count = int(tab.find('a').text.split('(')[1].split(')')[0])
        # Update the dictionary with the count for the corresponding difficulty
        difficulty_count[difficulty] = count
    
    d={}
    d["Handle"]=handle
    # d["Rank"]=rank
    d["POTD_Streak"]=POTD_streak
    d["Institute"]=Institute
    d["Coding_Score"]=Coding_score
    d["Problem_Solved"]=problem_solved
    d["Monthly_Coding_Score"]=monthly_coding_score
    d["Easy_Ques_Solved"]=difficulty_count["easy"]
    d["Medium_Ques_Solved"]= difficulty_count['medium']
    d["Hard_Ques_Solved"] = difficulty_count['hard']

    return d



def get_current_day():
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    current_day_index = datetime.datetime.today().weekday()
    current_day = days[current_day_index]
    return str(current_day)

def get_current_time():
    ist = pytz.timezone('Asia/Kolkata')  # Set the time zone to IST
    current_time_ist = datetime.datetime.now(ist).time()
    formatted_time = current_time_ist.strftime('%H:%M:%S')
    return str(formatted_time)

def get_upcoming_day_date(day_name,time):
    if(get_current_day()==day_name and get_current_time()<time):
        return datetime.date.today()
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    # Get the current date
    current_date = datetime.date.today()
    # Calculate the days until the next occurrence of the specified day
    days_until_next_day = (current_date.weekday() - days.index(day_name)) % 7
    # Calculate the date of the upcoming day
    upcoming_date = current_date + datetime.timedelta(days=(7 - days_until_next_day))
    return upcoming_date

    


def extract_info(problem_description):
    # Find the indices of key phrases
    problem_statement_index = problem_description.find("Problem Statement")
    examples_index = problem_description.find("Example")
    constraints_index = problem_description.find("Constraints")
    your_task_index = problem_description.find("Your Task")

    # Extract the corresponding sections using string slicing
    problem_statement = problem_description[problem_statement_index + len("Problem Statement"):examples_index].strip()
    examples_section = problem_description[examples_index + len("Examples"):constraints_index].strip()
    your_task = problem_description[your_task_index + len("Your Task"):constraints_index].strip()
    constraints = problem_description[constraints_index + len("Constraints"):].strip()

    # Convert examples_section to a dictionary
    # examples_dict = {}
    # examples_list = examples_section.split("\n")
    # current_example = ""
    # for line in examples_list:
    #     line = line.strip()
    #     if line.startswith("Example"):
    #         current_example = line
    #         examples_dict[current_example] = {"Input": {}, "Output": "", "Explanation": ""}
    #     elif line.startswith("Input:"):
    #         examples_dict[current_example]["Input"] = eval(line[len("Input:"):].strip())
    #     elif line.startswith("Output:"):
    #         examples_dict[current_example]["Output"] = eval(line[len("Output:"):].strip())
    #     elif line.startswith("Explanation:"):
    #         examples_dict[current_example]["Explanation"] = line[len("Explanation:"):].strip()

    # Create the final dictionary

    problem_statement=problem_statement.replace("\n","@!")
    examples_section=examples_section.replace("\n","@!")
    constraints=constraints.replace("\n","@!")
    your_task=your_task.replace("\n","@!")
    problem_dict = {
        "Problem Statement": problem_statement,
        "Examples": examples_section,
        "Constraints": constraints+"@! Your Task: "+your_task
        # "Your Task": your_task
    }
    return problem_dict


def codeforces_ques():
    url=" https://codeforces.com/api/contest.list?gym=false"
    response=requests.get(url)

    if response.json()["status"] != "OK":
        raise print('User not Found')
    d={}
    profile=response.json()["result"]


def codeforces_contest():
    url=" https://codeforces.com/api/contest.list?gym=false"
    response=requests.get(url)

    if response.json()["status"] != "OK":
        raise print('User not Found')
    d={}
    profile=response.json()["result"]
    global count
    for contest in profile[0:5]:
        # d["c_id"]=contest["id"]
        c_name=contest["name"]
        # d["c_duration"]=contest["durationSeconds"]/3600
        timestamp=contest["startTimeSeconds"]
        start_time_utc = datetime.datetime.utcfromtimestamp(timestamp)
        ist = pytz.timezone('Asia/Kolkata')
        start_time_ist = start_time_utc.replace(tzinfo=pytz.utc).astimezone(ist)
        formatted_start_time = start_time_ist.strftime('%Y-%m-%d %H:%M:%S')
        date=str(start_time_ist.date())
        time=str(start_time_ist.time())
        d[str(count)]={"Name":c_name,"Platform":"Codeforces","Date":date,"Time":time}
        count=count+1
    return d
    # db.collection("contests").document("contests").set(d)

def leetcode_contest():
    url="https://leetcode.com/contest/"
    response=requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    d={}
    global count
    name=soup.find_all(class_='transition-colors group-hover:text-blue-s dark:group-hover:text-dark-blue-s')
    c_name=name[0].text
    c_date=str(get_upcoming_day_date("Sunday","08:00:00"))
    c_time="08:00:00"
    d[str(count)]={"Name":c_name,"Platform":"Leetcode","Date":c_date,"Time":c_time}
    count=count+1



    c_name=name[1].text
    c_date=str(get_upcoming_day_date("Saturday","20:00:00"))
    c_time="20:00:00"
    d[str(count)]={"Name":c_name,"Platform":"Leetcode","Date":c_date,"Time":c_time}
    count=count+1
    return d
    # db.collection("contests").document("contests").set(d)

def gfg_contest():
    url="https://practice.geeksforgeeks.org/events/rec/gfg-weekly-coding-contest"
    response=requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    d={}
    global count
    c_name=soup.find(class_='sofia-pro events_upcomingEventDescTxt__xgvgK').text
    c_date=str(get_upcoming_day_date("Sunday","19:00:00"))
    c_time="19:00:00"
    d[str(count)]={"Name":c_name,"Platform":"GeeksForGeeks","Date":c_date,"Time":c_time}
    count=count+1
    return d
    # db.collection("contests").document("contests").set(d)
    # d[c_name]={"c_date":c_date,"c_time":c_time}
    # db.collection("contest").document("gfg").set(d)

def contest_update():
    dict1 = leetcode_contest()
    dict2 = codeforces_contest()
    dict3 = gfg_contest()

    # Merge dictionaries using {**d1, **d2, **d3} syntax
    d = {**dict1, **dict2, **dict3}
    db.collection("contests").document("contests").set(d)

def user_update():   
    users = db.collection("users").get()
    for user in users:
        gmail=user.id
        prof=user.to_dict()
        dic={}
        if "leetcode" in prof:
            l_handle=prof['leetcode']["Handle"]
            dic["leetcode"]=leetcode(l_handle)
        if "codeforces" in prof:
            c_handle=prof['codeforces']["Handle"]
            dic["codeforces"]=codeforces(c_handle)
        if "gfg" in prof:
            gfg_handle=prof['gfg']["Handle"]
            dic["gfg"]=gfg(gfg_handle)
        db.collection("users").document(gmail).update(dic)




cred = credentials.Certificate("credentials.json")
firebase_admin.initialize_app(cred)
db=firestore.client() 
user_update()
contest_update()
POTD_update()
