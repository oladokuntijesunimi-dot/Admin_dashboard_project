import os
from dotenv import load_dotenv
import mysql.connector
from mysql.connector import Error
import random
import string
import datetime

#load_dotenv(r"C:\Users\USER\Desktop\Flask\.env")

#db_password = os.environ.get('db_password')
#print(db_password)

try:
    connection = mysql.connector.connect(host = 'localhost',
                                        username = 'root',
                                        password = 'symplyteejay',
                                        database ='evoting_db')
    print(f"Connection to the Database was successful")

except Error as err:
    connection = None
    print(err)


def generate_id():
    first3chars = random.sample(string.ascii_uppercase,3)
    digits = random.sample(string.digits, 5)
    last2chars = random.sample(string.ascii_uppercase,2)
    id_ = first3chars + digits + last2chars
    return ''.join(id_)
print(generate_id())

def register_voter( fullname, age, gender, address, phonenumber, email):
    query ="""
    insert into voters(voting_id, fullname, age, gender, address, phonenumber, email)
    values (%s,%s,%s,%s,%s,%s,%s)
    """
    voting_id = generate_id()
    try:
        cursor = connection.cursor()
        cursor.execute(query,(voting_id, fullname, age, gender, address, phonenumber, email))
        connection.commit()
        message = f"Registration complete {voting_id}"
    except Error as err:
        print(err)
        message = 'Registration failed'
    return message


#print(register_voter('Teejay',19, 'M', 'Ibadan,nigeria','09136916789','oladokuntijesunimi@gmail.com'))

def register_party(party_id, party_name):
    query = """
    insert into party (party_id, party_name)
    values (%s, %s)
    """
    try:
        cursor = connection.cursor()
        cursor.execute(query, (party_id,party_name))
        connection.commit()
        message = f'{party_name} registered successfully'
    except Error as err:
        print(err)
        message = "Party Registration failed"

    return message
#register_party('PDP','Peoples Democratic party')
#register_party('APC','All Progressive Congress')
#register_party('Kowa','Kowa party')

def register_posts(post_name):
    query = """
    insert into posts (post_name)
    values (%s)
    """
    try:
        cursor = connection.cursor()
        cursor.execute(query, (post_name,))
        connection.commit()
        message = f'{post_name} Post has been registered successfully'
    except Error as err:
        print(err)
        message = "Post Registration failed"

    return message

#register_posts('Presidential')
#register_posts('Governorship')

def register_contestants(fullname,age,gender,party_id,post_id,address,email):
    query = """
    insert into contestants(contestant_id, fullname,age,gender,party_id,post_id,address,email)
    values (%s,%s,%s,%s,%s,%s,%s,%s)
    """
    contestant_id = generate_id()

    try:
        cursor = connection.cursor()
        cursor.execute(query,(contestant_id,fullname,age,gender,party_id,post_id,address,email))
        connection.commit()
        message = f"{contestant_id} Registration complete"
    except Error as err:
        print(err)
        message = 'registration failed'
    return message

def get_posts():
    query = """
    select * from posts
    """
    try:
        cursor = connection.cursor(buffered = True)
        cursor.execute(query)
        result = cursor.fetchall()
        
    except Error as err:
        print(err)
        result = "Unable to retrieve post"
    return result

def get_parties():
    query = """
    select * from party
    """
    try:
        cursor = connection.cursor(buffered = True)
        cursor.execute(query)
        result = cursor.fetchall()
        
    except Error as err:
        print(err)
        result = "Unable to retrieve parties"
    return result
#print(get_posts())
#print(get_parties())

def vote(contestant_id, post_id):
    query="""
    insert into results (post_id,contestant_id, voting_time)
    values (%s,%s,%s)
    """
    voting_time = datetime.datetime.now().strftime('%H:%M')
    try:
        cursor = connection.cursor()
        cursor.execute(query, (post_id, contestant_id, voting_time))
        connection.commit()
        message = "Vote recorded successfully"
    
    except Error as err:
        print(err)
        message = "Unable to register vote"
    return message

vote('UWA05784GF',2)
vote('UWA05784GF',1)
vote('MGL45018OK',1)
