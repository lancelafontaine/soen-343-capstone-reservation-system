from django.db import connection

print 'Start'
with connection.cursor() as cursor:
    cursor.execute('CREATE TABLE stocks (ID INT PRIMARY KEY, SYMBOL TEXT, QTY REAL)')
    cursor.execute("INSERT INTO stocks (SYMBOL,QTY) VALUES ('GOOGL', 100)")
    cursor.execute("INSERT INTO stocks (SYMBOL,QTY) VALUES ('MSFT', 50)")
print 'Done'
