import sqlite3

db = "skills_test_practice.db"

def connect_to_db():
    conn = sqlite3.connect(db)
    conn.row_factory = sqlite3.Row
    return conn

def create_table_user():
    with connect_to_db() as conn:
        conn.execute('CREATE TABLE IF NOT EXISTS user (user_id INTEGER PRIMARY KEY AUTOINCREMENT, firstname TEXT, lastname TEXT, email TEXT, username TEXT, password TEXT, isAdmin BOOLEAN);')
        conn.commit()

def create_table_event():
    with connect_to_db() as conn:
        conn.execute('CREATE TABLE IF NOT EXISTS event (event_id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, description TEXT, date DATE, time TIME)')
        conn.commit()

def create_table_user_event():
    with connect_to_db() as conn:
        conn.execute('CREATE TABLE IF NOT EXISTS user_event (event_id INTEGER, user_id INTEGER, PRIMARY KEY(event_id, user_id), FOREIGN KEY (user_id) REFERENCES user(user_id), FOREIGN KEY (event_id) REFERENCES event(event_id));')
        conn.commit()

def get_all_users():
    with connect_to_db() as conn:
        users = conn.execute('SELECT * FROM user').fetchall()
        users = [dict(user) for user in users]
        return users

def get_one_user(user_id):
    with connect_to_db() as conn:
        user = conn.execute('SELECT * FROM user WHERE user_id = ?', (user_id,)).fetchone()
        user = dict(user)
        return user
    
def get_all_events():
    with connect_to_db() as conn:
        events = conn.execute('SELECT * FROM event').fetchall()
        events = [dict(event) for event in events]
        return events

def get_one_event(event_id):
    with connect_to_db() as conn:
        event = conn.execute('SELECT * FROM event WHERE event_id = ?', (event_id,)).fetchone()
        event = dict(event)
        return event

def get_all_user_events(user_id):
    with connect_to_db() as conn:
        user_events = conn.execute('SELECT * from event e JOIN user_event ue ON e.event_id = ue.event_id WHERE user_id = ?', (user_id,)).fetchall()
        user_events = [dict(user_event) for user_event in user_events]
        return user_events

def get_one_user_event(event_id, user_id):
    with connect_to_db() as conn:
        user_event = conn.execute('SELECT * FROM  event e JOIN user_event ui ON e.event_id = ue.event_id WHERE user_id = ? AND event_id = ?', (user_id, event_id)).fetchone()
        user_event = dict(user_event)
        return user_event

def add_user(firstname, lastname, email, username, password):
    with connect_to_db() as conn:
        user_count = conn.execute('SELECT COUNT(*) FROM user').fetchone()[0]
        isAdmin = False
        if user_count == 0:
            isAdmin = True
            
        conn.execute('INSERT INTO user (firstname, lastname, email, username, password, isAdmin) VALUES (?,?,?,?,?,?)', (firstname, lastname, email, username, password, isAdmin))
        conn.commit()
            

def add_event(title, description, date, time):
    with connect_to_db() as conn:
        conn.execute('INSERT INTO event (title, description, date, time) VALUES (?,?,?,?)', (title, description, date, time))
        conn.commit()

def add_user_event(event_id, user_id):
    with connect_to_db() as conn:
        conn.execute('INSERT INTO user_event (event_id, user_id) VALUES (?,?)', (event_id, user_id))
        conn.commit() 

def login(username, password):
    with connect_to_db() as conn:
        user = conn.execute('SELECT * FROM user WHERE username = ? AND password = ?', (username, password)).fetchone()
        return user
    
def search(search_query):
    with connect_to_db() as conn:
        search_query = f"%{search_query.lower()}%"
        users = conn.execute('''
                             SELECT * FROM user 
                             WHERE LOWER(firstname || ' ' || lastname) LIKE ?
                             ''', (search_query,)).fetchall()
        users = [dict(user) for user in users]
        return users
            
def update_user(user_id, firstname, lastname, email, username, password):
    with connect_to_db() as conn:
        conn.execute('UPDATE user SET firstname = ?, lastname = ?, email = ?, username = ?, password = ? WHERE user_id = ?', (firstname, lastname, email, username, password, user_id))
        conn.commit()

def delete_user(user_id):
    with connect_to_db() as conn:
        conn.execute('DELETE FROM user WHERE user_id = ?', (user_id,))
        conn.commit()

if __name__ == "__main__":
    print(get_all_users())
    # print(search("ja"))
    # print(get_one_user("4"))
    # update_user("3","Christina", "Diamante", "christinadiamante113@gmail.com","bynib", "123")
    # print(get_one_user("3"))
    # delete_user("2")
    # print(login("bynib", "123"))
    # pass