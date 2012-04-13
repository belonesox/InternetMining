# -*- coding: cp1251 -*-
import urllib2, cookielib, re, pickle
opener = None
cookieJar = None
users = {}

XLS_PREFIX = "http://www.kinopoisk.ru/level/79/user/"
XLS_POSTFIX = "/votes/list/export/xls/"
FRIENDS_PREFIX = "http://www.kinopoisk.ru/level/77/friends/"

#kinopoisk.ru is a real douchebag and locking bots   
#so we are need to pretend the Opera 9 and catch his cookies
def init_opener():  
    global cookieJar, opener
    cookieJar = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookieJar))
    req = form_request('http://www.kinopoisk.ru/level/30')
    opener.open(req)
    
def form_request(url):
    req = urllib2.Request(url)
    #pretending to be an Opera 9 browser
    req.add_header('User-Agent', 'Opera/9')
    return req

#forming URL to get users marks by his number
def form_xls_url(number):
    return XLS_PREFIX+str(number)+XLS_POSTFIX

#forming URL to get users friends by his number
def form_friends_url(number):
    return FRIENDS_PREFIX+str(number)+"/perpage/1000"

def get_users_friends(number):
    req = form_request(form_friends_url(number))
    page = opener.open(req)
    #regular expression for finding links on user profiles
    #and getting users name and number from it 
    pat = re.compile(r'<a href="/level/79/user/([0-9]{0,7})/">(.*?)</a>', re.MULTILINE)
    f = pat.findall(page.read())
    result_list = [(int(a), b) for (a, b) in f]
    return result_list

#dumping users dictionary in a pickle format into "users" file
def dump_users():
    global users
    pickle_file = open("../data/users",'w')
    pickle.dump(users, pickle_file)
    pickle_file.close()
    
def recover_users():
    global users
    pickle_file = open("../data/users",'r')
    users = pickle.load(pickle_file)
    pickle_file.close()        

def process_user(name, number):
    #remember users dictionary
    global users
    #adding this particular user as viewed
    #using his number as a key
    users[number] = name
    #just for watching on the progress
    print users
    dump_users()
    req = form_request(form_xls_url(number))
    page = opener.open(req)
    
    #saving user marks into "number".xls file
    file_xls = open("../data/"+str(number)+".xls", 'w')
    file_xls.write(page.read())
    file_xls.close()
    
    for friend_number, friend in get_users_friends(number):
        #if this user is not viewed yet
        if not users.has_key(friend_number): 
            try: process_user(friend, friend_number)
            except: print "Bad user finded \""+friend+"\"" #this user haven't got any marks
    
def start_processing():
    #just starting with myself
    process_user("-SiN-", 515222)

if __name__=="__main__":        
    init_opener()
    start_processing()
    