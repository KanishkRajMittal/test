
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

from selenium.webdriver.chrome.options import Options




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
    problem_dict = {
        "Problem Statement": problem_statement,
        "Examples": examples_section,
        "Constraints": constraints+"\n Your Task: "+your_task
        # "Your Task": your_task
    }
    return problem_dict



def leetcode_potd():
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    driver = webdriver.Chrome(options=chrome_options)
    driver.get("https://leetcode.com/problemset/all/")
    sleep(3)

    # Click on the "Solve problem" button
    daily_ques = driver.find_element(By.XPATH, '(//div[@class="truncate"])[1]')
    daily_ques.click()

    sleep(2)
    driver.switch_to.window(driver.window_handles[0])
    # print(driver.current_url)

    title = driver.find_element(By.XPATH, "//div[@class='flex h-full items-center']").text
    ques = driver.find_element(By.XPATH, '(//p)[1]').text+driver.find_element(By.XPATH, '(//p)[2]').text
    ex1 = driver.find_element(By.XPATH, '(//pre)[1]').text
    ex2 = driver.find_element(By.XPATH, '(//pre)[2]').text
    constraints = driver.find_element(By.XPATH, '(//ul)[2]').text

    data = {"LeetCode": {"title":title,"Problem Statement": ques, "Examples": ex1+"\n"+ex2,
                    "Constraints": constraints}}
    return data


def gfg_potd():
    # Create a webdriver instance
    # Create a webdriver instance
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    driver = webdriver.Chrome(options=chrome_options)

    # Navigate to the link
    driver.get("https://www.geeksforgeeks.org/problem-of-the-day")
    sleep(5)

    # Click on the "Solve problem" button using JavaScript
    solve_button = driver.find_element(
        By.XPATH, '//button[@class="ui button problemOfTheDay_POTDCntBtn__SSQfX"]')
    driver.execute_script("arguments[0].click();", solve_button)
    sleep(1)
    driver.switch_to.window(driver.window_handles[1])
    s = driver.current_url


    attributes = driver.find_element(
        By.XPATH, '(//div)[@class="problems_problem_content__Xm_eO"]').text
    # print(attributes)

    # Close the browser
    driver.quit()
    # Extract information and print the dictionary
    attributes="Problem Statement"+attributes
    result_dict = extract_info(attributes)
    d={}
    d["GeeksForGeeks"]=result_dict
    return d



def codeforces_ques():
    url=" https://codeforces.com/api/contest.list?gym=false"
    response=requests.get(url)

    if response.json()["status"] != "OK":
        raise print('User not Found')
    d={}
    profile=response.json()["result"]

cred = credentials.Certificate("/home/kanishk/Desktop/Python/firebase/credentials.json")
firebase_admin.initialize_app(cred)
db=firestore.client() 
dict1 = leetcode_potd()
# dict2 = codeforces_ques()
dict3 = gfg_potd()

# Merge dictionaries using {**d1, **d2, **d3} syntax
d = {**dict1,**dict3}

db.collection("questions").document("POTD").set(d)
