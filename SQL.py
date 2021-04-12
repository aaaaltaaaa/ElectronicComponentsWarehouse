import pathlib
import sqlite3
inventoryAlertValue = 5

def insertInStorage(conn,data):
    cur=conn.cursor()
    insert='insert into electronicComponents ' \
           'values (?,?,?,?,?,?,?,?,?)'
    cur.execute(insert,data)
    conn.commit()
    cur.close()

def loadData(conn):
    data=[(1,'电动机1','电动机',1,2,1,100,10,'这是第一种电动机'),(2,'电动机2','电动机',2,4,1,100,10,'这是第二种电动机'),(3,'电阻1','电阻',1,1,1,10,100,'这是第一种电阻'),(4,'电阻2','电阻',2,2,1,10,100,'这是第二种电阻')]
    cur = conn.cursor()
    insert = 'insert into electronicComponents ' \
             'values (?,?,?,?,?,?,?,?,?)'
    cur.executemany(insert, data)
    conn.commit()
    cur.close()

def init(db_filename):
    path = pathlib.Path(db_filename)

    if(not path.exists()):
        try:
            conn = sqlite3.connect(db_filename)
        except sqlite3.Error as e:
            print(e)
            return
        cur = conn.cursor()
        creatElectronicComponentsTable ='create table electronicComponents(' \
              'no integer,' \
              'name text,' \
              'type text,' \
              'resistance integer,' \
              'nominalVoltage integer,' \
              'nominalCurrent integer,' \
              'price integer,' \
              'quantity integer,' \
              'info text,' \
              'primary key(no))'

        createRecordTable= 'create table record(' \
             'rno integer,' \
             'cno integer, ' \
             'quantity integer,' \
             'date datetime, ' \
             'primary key(rno autoincrement),' \
             'foreign key(cno) references electronicComponents(no))'
        creatIndex='create index time on record(date)'
        cur.execute(creatElectronicComponentsTable)
        cur.execute(createRecordTable)
        cur.execute(creatIndex)
        loadData(conn)
        cur.close()
    else:
        conn = sqlite3.connect(db_filename)
    return conn

def updateStorage(conn,data):
    cur=conn.cursor()
    update='update electronicComponents set quantity = quantity + ?  where no = ?'
    cur.execute(update,data)
    conn.commit()
    cur.close()

def insertRecord(conn, data):
    cur = conn.cursor()
    insert = 'insert into record(cno,quantity,date) ' \
             'values (?,?,datetime("now"))'
    cur.execute(insert, data)
    conn.commit()
    cur.close()

def checkInventory(conn,data):
    cur = conn.cursor()
    select = 'select  quantity ' \
             'from electronicComponents ' \
             'where no = ? '
    res = cur.execute(select, data)
    conn.commit()
    cur.close()
    if (res[0]<=inventoryAlertValue):
        return True
    else:
        return False

def update(conn,data):
    updateStorage(conn,(data[1],data[0]))
    insertRecord(conn, (data[0], data[1]))
    res=checkInventory(conn,(data[0],))


def getByType(conn,data):
    cur = conn.cursor()
    select = 'select * ' \
             'from electronicComponents ' \
             'where type = ?'
    cur.execute(select, data)
    res=cur.fetchall()
    cur.close()
    return res

def getByNo(conn,data):
    cur = conn.cursor()
    select = 'select * ' \
             'from electronicComponents ' \
             'where no = ? '
    cur.execute(select, data)
    res = cur.fetchall()
    cur.close()
    return res

def getInventoryValue():
    cur = conn.cursor()
    select = 'select sum(quantity*price) ' \
             'from electronicComponents '
    cur.execute(select)
    res = cur.fetchall()
    cur.close()
    return res

def monthlyConsumption(conn):
    cur = conn.cursor()
    select = 'select cno, sum(record.quantity), strftime("%Y-%m",date) ' \
             'from (select * from record where quantity>0) as record '\
             'group by cno, strftime("%Y-%m",date)'
    cur.execute(select)
    res = cur.fetchall()
    cur.close()
    return res

def weekConsumption(conn):
    cur = conn.cursor()
    select = 'select cno, sum(record.quantity), strftime("%Y-%W",date) ' \
             'from (select * from record where quantity>0) as record ' \
             'group by cno, strftime("%Y-%W",date)'
    cur.execute(select)
    res = cur.fetchall()
    cur.close()
    return res

def getOutboundComponentsValuePerMonth(conn):
    cur = conn.cursor()
    select = 'select sum(record.quantity*electronicComponents.price), strftime("%Y-%m",date) ' \
             'from (select * from record where quantity>0) as record left join electronicComponents ' \
             'on record.cno  = electronicComponents.no ' \
             'group by strftime("%Y-%m-%w",date) '
    cur.execute(select)
    res = cur.fetchall()
    cur.close()
    return res

if __name__ == '__main__':
    conn=init('electronicComponents.db')
    res=weekConsumption(conn)
    print(res)
    conn.close()
