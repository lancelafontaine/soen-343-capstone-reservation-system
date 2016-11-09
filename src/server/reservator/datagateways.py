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

    def getNumOfReservations(self, username, timeslot):
        with connection.cursor() as cursor:
            cursor.execute("SELECT COUNT(TIMESLOT) FROM reservations WHERE USER_ID=(SELECT ID from users WHERE USERNAME=%s)\
             AND strftime('%W', TIMESLOT)=strftime('%W', %s)", [username, timeslot])
            count = int(cursor.fetchone()[0])
        return count

    def find(self, username, roomNumber, timeslot):
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM reservations WHERE USER_ID=(SELECT ID from users WHERE USERNAME=%s) \
                    AND ROOM_ID=(SELECT ID from rooms WHERE ROOMNUMBER=%s) \
                    AND TIMESLOT=%s", [username,roomNumber,timeslot])
            row = cursor.fetchone()
        return row

    def findNextPendingReservation(self, roomNumber, timeslot):
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM reservations WHERE TSP=(SELECT min(TSP) FROM reservations WHERE STATUS='pending' \
            AND ROOM_ID=(SELECT ID from rooms WHERE ROOMNUMBER=%s) AND TIMESLOT=%s)", [roomNumber, timeslot])
            row = cursor.fetchone()
        return row

    def setFilled(self, username, roomNumber, timeslot):
        with connection.cursor() as cursor:
            cursor.execute("UPDATE reservations SET STATUS='filled' WHERE USER_ID=(SELECT ID from users WHERE USERNAME=%s) \
                    AND ROOM_ID=(SELECT ID from rooms WHERE ROOMNUMBER=%s) \
                    AND TIMESLOT=%s", [username,roomNumber,timeslot])

    def getFilledCount(self, roomNumber, timeslot):
        with connection.cursor() as cursor:
            cursor.execute("SELECT COUNT(1) FROM reservations WHERE ROOM_ID=(SELECT ID from rooms WHERE ROOMNUMBER=%s) \
                    AND TIMESLOT=%s AND STATUS='filled'", [roomNumber, timeslot])
            count = int(cursor.fetchone()[0])
        return count

    def getReservationCount(self, username, roomNumber, timeslot):
        with connection.cursor() as cursor:
            cursor.execute("SELECT COUNT(1) FROM reservations WHERE USER_ID=(SELECT ID from users WHERE USERNAME=%s) \
                    AND ROOM_ID=(SELECT ID from rooms WHERE ROOMNUMBER=%s) \
                    AND TIMESLOT=%s", [username,roomNumber,timeslot])
            count = int(cursor.fetchone()[0])
        return count

    def getReservations(self, roomNumber, startTimeslot):
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM reservations WHERE ROOM_ID=(SELECT ID from rooms WHERE ROOMNUMBER=%s)  \
                           AND strftime('%W', TIMESLOT)=strftime('%W', %s) \
                           AND STATUS='filled' ORDER BY TIMESLOT ASC", [roomNumber, startTimeslot])
            rows = cursor.fetchall()
        return rows
