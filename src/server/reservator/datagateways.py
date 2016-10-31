from django.db import connection

# Warning: Django is set to AUTOCOMMIT mode unless otherwise specified.
class ReservationTDG:
    
    def insert(username, roomNumber, status, timeslot, timestamp):
        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO reservations (USER_ID,ROOM_ID,\
                    STATUS,TIMESLOT,TIMESTAMP) VALUES (SELECT ID from users WHERE USERNAME=%s,\
                    SELECT ID from rooms WHERE ROOMNUMBER=%s,%s,%s,%s)", [username,roomNumber,status,timeslot,timestamp])

    def delete(username, roomNumber, timeslot):
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM reservations (USER_ID,ROOM_ID,\
                    STATUS,TIMESLOT,TIMESTAMP) VALUES (SELECT ID from users WHERE USERNAME=%s,\
                    SELECT ID from rooms WHERE ROOMNUMBER=%s,%s)", [username,roomNumber,timeslot])

    def update(username, roomNumber, timeslot, timestamp):
        pass

    def find(username, roomNumber, timeslot, timestamp):
        pass


