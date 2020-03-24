import pymysql
def check_photo(email):
    conn = pymysql.connect(
        host='localhost',
        port=3306,
        user='root',
        passwd='',
        db='test',
        autocommit=True
    )
    cur = conn.cursor()
    cur.execute("select *from photo where email='"+email+"'")
    n=cur.rowcount
    photo="no"
    if n>0:
        row=cur.fetchone()
        photo=row[1]
    return photo
