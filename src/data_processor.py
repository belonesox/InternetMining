from BeautifulSoup import BeautifulSoup
import pickle

users = {}
users_marks = {}

def parse_data(number):
    xlsname = form_xls_name(number)
    xlsfile = open(xlsname)
    soup = BeautifulSoup(''.join(xlsfile.read()))
    xlsfile.close()
    table = soup.find('table')
 
    rows = table.findAll('tr')
    marks = []
    for tr in rows:
        marks.append([])
        cols = tr.findAll('td')
        for td in cols:
            text = td.contents[0] if td.contents else ''
            text = text.contents[0] if hasattr(text,"contents") \
                                    and text.contents else text
            text = str(text)
            marks[-1].append(text)
        
    marks=marks[1:]
    marks = [(row[0] if row[0]!='' else row[1] \
              , int(row[8]) if row[8]!='-' else 0) for row in marks]
    return marks
    

def form_xls_name(number):
    return "../data/"+str(number)+".xls"

def dump_users_marks():
    global users_marks
    pickle_file = open("../data/users_marks",'w')
    pickle.dump(users_marks, pickle_file)
    pickle_file.close()

def recover_users():
    global users
    pickle_file = open("../data/users",'r')
    users = pickle.load(pickle_file)
    pickle_file.close()   

def process_users():
    recover_users()
    for number in users.keys():
        users_marks[number] = parse_data(number)
        print len(users_marks[number])
        dump_users_marks()
        
process_users()
    
