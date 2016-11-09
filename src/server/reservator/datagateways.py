from django.db import connection

# Warning: Django is set to AUTOCOMMIT mode unless otherwise specified.
class ReservationTDG:

    def __init__(self):
        pass
    
    def insert(self, username, roomNumber, timeslot, status, timestamp):
        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO reservations (USER_ID,ROOM_ID,\
                    STATUS,TIMESLOT,TIMESTAMP) VALUES ((SELECT ID from users WHERE USERNAME=%s),\
                    (SELECT ID from rooms WHERE ROOMNUMBER=%s),%s,%s,%s)", [username,roomNumber,status,timeslot,timestamp])

    def delete(self, username, roomNumber, timeslot):
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM reservations WHERE USER_ID=(SELECT ID from users WHERE USERNAME=%s) \
                    AND ROOM_ID=(SELECT ID from rooms WHERE ROOMNUMBER=%s) \
                    AND TIMESLOT=%s", [username,roomNumber,timeslot])

    def update(self, username, roomNumber, timeslot, timestamp):
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM reservations WHERE USER_ID=(SELECT ID from users WHERE USERNAME=%s) \
                    AND ROOM_ID=(SELECT ID from rooms WHERE ROOMNUMBER=%s) \
                    AND TIMESLOT=%s", [username,roomNumber,timeslot])

    def find(self, username, roomNumber, timeslot, timestamp):
        with connection.cursor() as cursor:
            cursor.execute("SELECT FROM reservations WHERE USER_ID=(SELECT ID from users WHERE USERNAME=%s) \
                    AND ROOM_ID=(SELECT ID from rooms WHERE ROOMNUMBER=%s) \
                    AND TIMESLOT=%s", [username,roomNumber,timeslot])


