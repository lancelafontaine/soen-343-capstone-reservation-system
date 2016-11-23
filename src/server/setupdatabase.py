from django.db import connection

print 'Creating and initializing database...'

with connection.cursor() as cursor:
    cursor.execute('CREATE TABLE rooms (ID INTEGER PRIMARY KEY AUTOINCREMENT, ROOMNUMBER TEXT)')
    cursor.execute("INSERT INTO rooms (ROOMNUMBER) VALUES ('H-905')")
    cursor.execute("INSERT INTO rooms (ROOMNUMBER) VALUES ('H-831')")
    cursor.execute("INSERT INTO rooms (ROOMNUMBER) VALUES ('H-747')")
    cursor.execute('CREATE TABLE users (ID INTEGER PRIMARY KEY AUTOINCREMENT, USERNAME TEXT, PASSWORD TEXT)')
    cursor.execute("INSERT INTO users (USERNAME,PASSWORD) VALUES ('testuser','testuser')")
    cursor.execute("INSERT INTO users (USERNAME,PASSWORD) VALUES ('testuser2','testuser2')")
    cursor.execute("INSERT INTO users (USERNAME,PASSWORD) VALUES ('testuser3','testuser3')")
    cursor.execute('CREATE TABLE reservations (USER_ID INT REFERENCES users(ID), ROOM_ID INT REFERENCES rooms(ID),\
            STATUS TEXT, TIMESLOT TEXT, TSP TEXT)')


print 'Database setup has been completed.'
