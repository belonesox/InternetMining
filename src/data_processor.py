from BeautifulSoup import BeautifulSoup
import pickle, os

users = {}
users_marks = []

#all data in downloaded files is represented
#in a table HTML format, so we need to parse it
def parse_data(number):
    xlsname = form_xls_name(number)
    xlsfile = open(xlsname)
    soup = BeautifulSoup(''.join(xlsfile.read()))
    xlsfile.close()
    table = soup.find('table')
 
    rows = table.findAll('tr')
    marks = []
    for tr in rows:
        #adding new row
        marks.append([])
        cols = tr.findAll('td')
        for td in cols:
            #avoiding extra tags in movie titles
            text = td.contents[0] if td.contents else ''
            text = text.contents[0] if hasattr(text,"contents") \
                                    and text.contents else text
            text = str(text)
            marks[-1].append(text)
    
    #deleting table's head    
    marks=marks[1:]
    #this magic generates the list that will be smth like that
    #("Movie Title(on russian or in original) YEAR", mark (or 0 if u just watched it)
    # 0 - russian title
    # 1 - native title
    # 2 - year
    # 8 - mark (could be '-')
    marks = [((row[0] if row[0]!='' else row[1]) + " " + row[2] \
              , int(row[8]) if row[8]!='-' else 0) for row in marks]
    return marks
    

def form_xls_name(number):
    return "../data/"+str(number)+".xls"

#dump data that represents users we've already process
def dump_users_marks():
    global users_marks
    pickle_file = open("../data/marks/users_proceeded",'w')
    pickle.dump(users_marks, pickle_file)
    pickle_file.close()

#load all users list
def recover_users():
    global users
    pickle_file = open("../data/users",'r')
    users = pickle.load(pickle_file)
    pickle_file.close()

def recover_users_marks():
    global users_marks
    if not os.path.exists("../data/marks/users_proceeded"): return
    pickle_file = open("../data/marks/users_proceeded",'r')
    users_marks = pickle.load(pickle_file)
    pickle_file.close()  

#store users marks data
def dump_users_data(number):
    pickle_file = open("../data/marks/"+str(number),'w')
    pickle.dump(parse_data(number), pickle_file)
    pickle_file.close()

def process_users():
    recover_users()
    recover_users_marks()
    a = set(users)
    b = set(users_marks)
    #dealing with not processed users
    c = a - b
    print "Start"
    for number in c:
        try:
            dump_users_data(number)
            users_marks.append(number)
            print len(users_marks)
            dump_users_marks()
        except: print "bad user"
        
process_users()
    
