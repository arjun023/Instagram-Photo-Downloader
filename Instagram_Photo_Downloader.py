# -*- coding: utf-8 -*-

from selenium       import webdriver
from getpass        import getpass
from urllib.request import urlretrieve
from time           import sleep
from colorama       import init, deinit, Fore
from termcolor      import colored, cprint

import os
import json
import platform
import argparse

print_red       = lambda x, y="\n" : cprint(x, "red", end=y)
print_green     = lambda x, y="\n" : cprint(x, "green", end=y)
print_magenta   = lambda x, y="\n" : cprint(x, "magenta", end=y)
print_yellow    = lambda x, y="\n" : cprint(x, "yellow", end=y)
print_cyan      = lambda x, y="\n" : cprint(x, "cyan", end=y)

def parse_args():
    parser = argparse.ArgumentParser(description="Fetch all the lectures for a Instagram")
    parser.add_argument("-u", "--username", metavar="", help="User username")
    parser.add_argument("-p", "--password", metavar="", help="User password")
    parser.add_argument("-d", "--driver",   metavar="", type=int, choices=[1,2], help="Choosen Driver. [1]PantomJS [2]Chrome")
    parser.add_argument("--path", metavar="", help="The path for saving photos.")
    global args 
    args = parser.parse_args()

def clear_screen():
    plt = platform.system()
    
    if plt == "Windows":
        os.system("cls")
    elif plt == "Linux":
        os.system("clear")

def create_config_if_not_exist():
    if not os.path.isfile("config.json"):
        try:
            data = {"username" : "", "password" : "", "path" : "pictures"}
            text = json.dumps(data)
            with open("config.json", "w") as file:
                file.write(text)
        except:
            print_red("Config file could not be created!")
            print_yellow("Try run this script as root.")
            return

def header():
    print()
    print_magenta("----------------------------------", "\n\n")
    print_magenta("### Instagram Photo Downloader ###", "\n\n")
    print_magenta("----------------------------------")
    print()

def read_json():
    if not os.path.isfile("config.json"):
        return None
    else:
        try:
            with open("config.json") as data_file:
                data = json.load(data_file)
            return data
        except:
            return None

def get_username():
    if args.username:
        return args.username
    else:
        config = read_json()
        if config and config["username"] != "":
            return config["username"]
        else:
            return input("Username : ")

def get_password():
    if args.password:
        return args.password
    else:
        config = read_json()
        if config and config["password"] != "":
            return config["password"]
        else:
            return getpass("Password : ")

def get_path():
    if args.path:
        return args.path
    else:
        config = read_json()
        if config and config["path"] != "":
            return config["path"]
        else:
            return "pictures"

def choose_driver():
    if args.driver == 1:
        driver = webdriver.PhantomJS()
        print_cyan("Driver : PhantomJS")
    elif args.driver == 2:
        driver = webdriver.Chrome()
        print_cyan("Driver : Chrome")
    else:
        config = read_json()
        if config and "driver" in config:
            _dri = config["driver"]
            if _dri == 1:
                print_cyan("Driver : PhantomJS")
                return webdriver.PhantomJS()
            elif _dri == 2:
                print_cyan("Driver : Chrome")
                return webdriver.Chrome()

        while True:
            print_cyan("CHOOSE DRIVER : [1]PhantomJS [2]Chrome")
            d_choice = input("Driver : ")

            if d_choice == "1":
                driver = webdriver.PhantomJS()
                break
            elif d_choice == "2":
                driver = webdriver.Chrome()
                break 
    return driver
    
def line():
    print_magenta("-----------------")
    
def signing_in(driver):
    while True:
        username = get_username()
        password = get_password()
        
        print_green("Logging in...")
        driver.get("https://www.instagram.com/")
        try:
            driver.find_element_by_class_name("_b93kq").click()
        except:
            pass
        
        driver.find_element_by_name("username").send_keys(username)
        driver.find_element_by_name("password").send_keys(password)
        driver.find_element_by_tag_name("button").click()
        
        sleep(4)
        try:
            driver.find_element_by_name("verificationCode")
            print_green("Username and password are correct!")
            line()
            verification = True
            break
        except:
            pass
        
        try:
            driver.find_element_by_class_name("coreSpriteSearchIcon")
            print_green("Username and password are correct!")
            line()
            verification = False
            break
        except:
            pass
    
        print_red("Your username or password is wrong. Try again!")
        line()
    
    while verification:
        try :
            code = input("The code, sent to your phone by Instagram : ")
            driver.find_element_by_name("verificationCode").clear()
            driver.find_element_by_name("verificationCode").send_keys(code)
            driver.find_element_by_tag_name("button").click()
            
            sleep(5)
            driver.find_element_by_class_name("coreSpriteSearchIcon")
            print_green("Login is successful.")
            break
        except :
            print_red("Your code is wrong. Try again!")
            line()
  
def find_photos(driver):
    username = input("Username for Photos : ")
    print_green("Getting user...")
    driver.get("https://www.instagram.com/" + username)
    
    print_green("Listing stories...")
    photo_total = int(driver.find_element_by_class_name("_fd86t").text.replace(".", ""))
    try:
        driver.find_element_by_class_name("_1cr2e").click()
    except:
        pass
    while True:
        photo_current = len(driver.find_elements_by_css_selector("._f2mse a"))
        print_cyan("> " + str(photo_current) + " photos listed.", "\r")
        if photo_current == photo_total:
            print_cyan("# " + str(photo_total) + " #", "")
            print_green(" stories listed.     ")
            break
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        
    print_green("Collecting stories...")
    imgList = driver.find_elements_by_css_selector("._f2mse a")
    imgLinks = []
    for idx, img in enumerate(imgList):
        print_cyan("> " + str(idx) + " photos collected.", "\r")
        imgLinks.append(img.get_property("href"))
    
    print_cyan("# " + str(len(imgList)) + " #", "")
    print_green(" stories found.      ")
    return imgLinks, username

def create_folder(folderName):
    if not os.path.exists(folderName):
        os.makedirs(folderName)
        print_green("User folder created!")
    else:
        print_yellow("User folder already exists!")
        
    if not os.path.exists(folderName + "/videos"):
        os.makedirs(folderName + "/videos")
    
def download_photos(driver, imgLinks, folderName):
    total = len(imgLinks)
    down = 0
    ndown = 0
    
    while True:
        print("How many stories do you want to download?")
        print_magenta("Give number ", "")
        print_cyan("-> For downloading the number of stories")
        print_magenta("Give '0'    ", "")
        print_cyan("-> For downloading all stroies")
        print_magenta("Live empty  ", "")
        print_cyan("-> For downloading last stories you do not have")
        lastStr = input("Give input : ")
        try:
            if lastStr == "":
                last = total
                just_last_photos = True
                break
            else:
                just_last_photos = False
                last = int(lastStr)
                if last > 0:
                    break
                elif last == 0:
                    last = total
                    break
                else:
                    print_red("Input cannot be negative!")
        except:
            print_red("Please give number!")
        line()
    
    print_green("Download process started!")
    done = False
    
    for idx, link in enumerate(imgLinks):
        driver.get(link)
        time = driver.find_element_by_tag_name("time").get_attribute("datetime").split("T")[0] + "_"
        
        try:
            # If page has many photos
            img_count = driver.execute_script('return window._sharedData.entry_data.PostPage[0].graphql.shortcode_media.edge_sidecar_to_children.edges.length')
            for i in range(img_count):
                is_video = driver.execute_script('return window._sharedData.entry_data.PostPage[0].graphql.shortcode_media.edge_sidecar_to_children.edges[' + str(i) +'].node.is_video')
                
                if is_video:
                    img_link = driver.execute_script('return window._sharedData.entry_data.PostPage[0].graphql.shortcode_media.edge_sidecar_to_children.edges[' + str(i) +'].node.video_url')
                else:
                    img_link = driver.execute_script('return window._sharedData.entry_data.PostPage[0].graphql.shortcode_media.edge_sidecar_to_children.edges[' + str(i) +'].node.display_url')
                
                # Create Name
                s = img_link.split("/")
                name = time + s[-1]
                
                # Download photos
                if is_video:
                    path = folderName + "/videos/" + name
                else:
                    path = folderName + "/" + name
                
                if not os.path.isfile(path):
                    urlretrieve(img_link, path)
                    down += 1
                else:
                    if just_last_photos:
                        done = True
                    ndown += 1
        except:
            try:
                # If it is a video
                img_link = driver.find_element_by_tag_name("video").get_attribute("src")
                is_video = True
            except:
                # Get Picture URL
                tag = driver.find_element_by_css_selector('meta[property="og:image"]')
                img_link = tag.get_property("content")
                is_video = False
            
            # Create Name
            s = img_link.split("/")
            name = time + s[-1]
            
            # Download photos
            if is_video:
                path = folderName + "/videos/" + name
            else:
                path = folderName + "/" + name
            
            if not os.path.isfile(path):
                urlretrieve(img_link, path)
                down += 1
            else:
                if just_last_photos:
                    done = True
                ndown += 1
        
        # Info
        print_cyan("> " + str(idx + 1) + " / " + str(last) + " stories downloaded...", "\r")
            
        # Max photo check - Break outer loop when inner loop broken
        if idx == last - 1 or done:
            print_cyan("# " + str(idx + 1) + " #", "")
            print_green(" stories downloaded.          ")
            break
    line()
    print_green("Download Completed.")
    print_green("Total found stories     : " + str(total))
    print_green("Total downloaded stories: " + str(last))
    print_green("")
    print_green("Total found photos      : " + str(down + ndown))
    print_cyan ("Total Download          : " + str(down))
    print_green("Already exists          : " + str(ndown))

def core():
    parse_args()
    create_config_if_not_exist()
    init()
    clear_screen()

    header()
    driver = choose_driver()
    line()

    signing_in(driver)
    
    while True :
        imgLinks, username = find_photos(driver)
        line()
        
        path = get_path() + "/" + username
        create_folder(path)
        line()
        
        download_photos(driver, imgLinks, path)
        line()
        
        ans = input("Use again(y/N)? : ")
        line()
        if not ans == "y":
            break
    
    input("Press any key to exit")
    driver.close()
    deinit()
    print("Closed.")
    
if __name__ == "__main__":
    core()