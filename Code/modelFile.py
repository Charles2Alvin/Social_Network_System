import pymysql
import time
class Model:
    def __init__(self):
        self.user = "root"
        self.dbname = "SocialNetwork"
        self.passwd = "123456"

    def connect2db(self):
        self.conn = pymysql.connect(
            host="localhost", port=3306, user=self.user, passwd=self.passwd, db=self.dbname)

    def checkemail(self, email):
        cursor = self.conn.cursor()
        sql = "select * from user where email = %s"
        param = [email]
        try:
            cursor.execute(sql, param)
            result = cursor.fetchall()
            if len(result) == 0:
                return True
            else: return False
            self.conn.commit()
        except pymysql.Error:
            print("Error!")
            self.conn.rollback()

    def signup(self, name, gender, date, mail, addr, password):
        cursor = self.conn.cursor()
        sql = "Insert into user" \
              "(name, gender, birth, email, address, passwd)" \
              "values " \
              "(%s, %s, %s, %s, %s, %s);"
        param = [name, gender, date, mail, addr, password]
        try:
            cursor.execute(sql, param)
            self.conn.commit()
        except pymysql.Error:
            print("Error!")
            self.conn.rollback()

    def signin(self, email, usrpass):
        cursor = self.conn.cursor()
        sql = "select passwd from user where email = %s"
        param = [email]
        try:
            cursor.execute(sql, param)
            result = cursor.fetchall()
            if len(result) == 0:
                return 1
            else:
                realpass = result[0][0]
                if realpass == usrpass:
                    return 2
                else:
                    return 3
            self.conn.commit()
        except pymysql.Error:
            print("Error!")
            self.conn.rollback()

    def fetch_journal_time(self, usrMail, Time):
        cursor = self.conn.cursor()
        sql = "select content from journal where email = %s and publish_time = %s"
        param = [usrMail, Time]
        try:
            cursor.execute(sql, param)
            result = cursor.fetchall()
            if result != ():
                return result[0]
            else:
                return ()
            self.conn.commit()
        except pymysql.Error:
            print("Error!")
            self.conn.rollback()

    def update_journal(self, usrMail, body, time):
        cursor = self.conn.cursor()
        sql = "update journal set content = %s where email = %s and publish_time = %s;"
        param = [usrMail, body, time]
        try:
            cursor.execute(sql, param)
            self.conn.commit()
            return 0
        except pymysql.Error:
            print("Error!")
            self.conn.rollback()

    def get_fri_journal(self, usrMail):
        cursor = self.conn.cursor()
        sql = "select user.name, user.email, title, content, journal.publish_time from journal, user where journal.email in ( select fri_email from friend where usr_email = %s) and user.email = journal.email;"
        param = [usrMail]
        try:
            cursor.execute(sql, param)
            result = cursor.fetchall()
            if result != ():
                return result
            else:
                return ()
            self.conn.commit()
        except pymysql.Error:
            print("Error!")
            self.conn.rollback()

    def usrinfo(self, email):
        cursor = self.conn.cursor()
        sql = "select * from user where email = %s"
        param = [email]
        try:
            cursor.execute(sql, param)
            result = cursor.fetchall()
            if result != ():
                return result[0]
            else:
                return ()
            self.conn.commit()
        except pymysql.Error:
            print("Error!")
            self.conn.rollback()

    def add_edu_work(self, Email, Level, School, Degree, Startdate, Enddate):
        cursor = self.conn.cursor()
        params = [Email, Level, School, Degree, Startdate, Enddate]
        for i in range(len(params)):
            if params[i] == '' or params[i] == 'None':
                params[i] = 'null'
            else: params[i] = '"'+str(params[i])+'"'
        sql = "insert into edu_experience " \
              "(email, level, school, degree, start_date, end_date) " \
              "values ({}, {}, {}, {}, {}, {})".format(
            params[0], params[1], params[2], params[3], params[4], params[5])
        try:
            cursor.execute(sql)
            self.conn.commit()
            return 0
        except pymysql.Error:
            print("Error!")
            self.conn.rollback()

    def update_edu_exp(self, Email, Level, School, Degree, Start_date, End_date):
        cursor = self.conn.cursor()
        params = [School, Degree, Start_date, End_date, Email, Level]
        for i in range(len(params)):
            if params[i] == '' or params[i] == 'None':
                params[i] = 'null'
            else: params[i] = '"'+str(params[i])+'"'
        sql = "update edu_experience " \
              "set school = {}, degree = {}, start_date = {}, end_date = {} " \
              "where email = {} and level = {};".format(
            params[0], params[1], params[2], params[3], params[4], params[5])
        try:
            cursor.execute(sql)
            self.conn.commit()
            return 0
        except pymysql.Error:
            print("Error!")
            self.conn.rollback()

    def update_work_exp(self, Email, Workplace, Title, Startdate, Enddate):
        cursor = self.conn.cursor()
        params = [Startdate, Enddate, Email, Workplace, Title]
        for i in range(len(params)):
            if params[i] == '' or params[i] == 'None':
                params[i] = 'null'
            else: params[i] = '"'+str(params[i])+'"'
        sql = "update work_experience " \
              "set start_date = {}, end_date = {} " \
              "where email = {} and workplace = {} and title = {};".format(
            params[0], params[1], params[2], params[3], params[4])
        try:
            cursor.execute(sql)
            self.conn.commit()
            return 0
        except pymysql.Error:
            print("Error!")
            self.conn.rollback()

    def updatePortrait(self, Email, Path):
        cursor = self.conn.cursor()
        params = [Path, Email]
        sql = "update user set portrait = %s where email = %s"
        try:
            cursor.execute(sql, params)
            self.conn.commit()
        except pymysql.Error:
            print("Error!")
            self.conn.rollback()

    def addJournal(self, Email, Title, Body, Time):
        cursor = self.conn.cursor()
        params = [Email, Title, Body, Time]
        sql = "insert into journal " \
              "(email, title, content, publish_time) " \
              "values (%s, %s, %s, %s)"
        try:
            cursor.execute(sql, params)
            self.conn.commit()
            return 0
        except pymysql.Error:
            print("Error!")
            self.conn.rollback()

    def add_work_exp(self, Email, Workplace, Title, Startdate, Enddate):
        cursor = self.conn.cursor()
        params = [Email, Workplace, Title, Startdate, Enddate]
        for i in range(len(params)):
            if params[i] == '' or params[i] == 'None':
                params[i] = 'null'
            else: params[i] = '"'+str(params[i])+'"'
        sql = "insert into work_experience " \
              "(email, workplace, title, start_date, end_date) " \
              "values ({}, {}, {}, {}, {})".format(
            params[0], params[1], params[2], params[3], params[4])
        try:
            cursor.execute(sql)
            self.conn.commit()
            return 0
        except pymysql.Error:
            print("Error!")
            self.conn.rollback()

    def delete_edu_exp(self, Email, Level):
        cursor = self.conn.cursor()
        sql = "delete from edu_experience where email = %s and level = %s;"
        param = [Email, Level]
        try:
            cursor.execute(sql, param)
            self.conn.commit()
        except pymysql.Error:
            print("Error!")
            self.conn.rollback()

    def delete_work_exp(self, Email, Workplace, Title):
        cursor = self.conn.cursor()
        sql = "delete from work_experience where email = %s and workplace = %s and title = %s"
        param = [Email, Workplace, Title]
        try:
            cursor.execute(sql, param)
            self.conn.commit()
        except pymysql.Error:
            print("Error!")
            self.conn.rollback()

    def show_edu_exp(self, Email):
        cursor = self.conn.cursor()
        sql = "select * from edu_experience where email = %s"
        param = [Email]
        try:
            cursor.execute(sql, param)
            return cursor.fetchall()
            self.conn.commit()
        except pymysql.Error:
            print("Error!")
            self.conn.rollback()

    def show_work_exp(self, Email):
        cursor = self.conn.cursor()
        sql = "select * from work_experience where email = %s"
        param = [Email]
        try:
            cursor.execute(sql, param)
            return cursor.fetchall()
            self.conn.commit()
        except pymysql.Error:
            print("Error!")
            self.conn.rollback()

    def modifyinfo(self, Name, Gender, Birth, Address, Email):
        cursor = self.conn.cursor()
        sql = "update user set name = %s, gender = %s, " \
              "birth = %s, address = %s where email = %s;"
        param = [Name, Gender, Birth, Address, Email]
        try:
            cursor.execute(sql, param)
            print("Successful modification")
            self.conn.commit()
            return 0
        except pymysql.Error:
            print("Error!")
            self.conn.rollback()

    def deleteJournal(self, Email, Time):
        cursor = self.conn.cursor()
        sql = "delete from journal " \
              "where email = %s and publish_time = %s"
        param = [Email, Time]
        try:
            cursor.execute(sql, param)
            self.conn.commit()
        except pymysql.Error:
            print("Error!")
            self.conn.rollback()

    def updateGrp(self, UserMail, FriMail, GrpName):
        cursor = self.conn.cursor()
        sql = "update friend " \
              "set group_name = %s " \
              "where usr_email = %s and fri_email = %s;"
        param = [GrpName, UserMail, FriMail]
        try:
            cursor.execute(sql, param)
            self.conn.commit()
        except pymysql.Error:
            print("Error!")
            self.conn.rollback()

    def addGrp(self, usr_email, GrpName):
        cursor = self.conn.cursor()
        sql = "insert into friend " \
              "(usr_email, fri_email, group_name) " \
              "values " \
              "(%s,'无', %s);"
        param = [usr_email, GrpName]
        try:
            cursor.execute(sql, param)
            result = cursor.fetchall()
            self.conn.commit()
            return result
        except pymysql.Error:
            print("Error!")
            self.conn.rollback()

    def existGrp(self, GrpName):
        cursor = self.conn.cursor()
        sql = "select *" \
              "from friend " \
              "where group_name = %s;"
        param = [GrpName]
        try:
            cursor.execute(sql, param)
            result = cursor.fetchall()
            self.conn.commit()
            return result
        except pymysql.Error:
            print("Error!")
            self.conn.rollback()

    # 把指定分组的好友都改成默认分组的
    def chGrp(self, usrMail, GrpName):
        cursor = self.conn.cursor()
        # 先确认一下这个分组是否存在
        sql1 = "select * from friend where usr_email = %s and group_name = %s;"
        param1 = [usrMail, GrpName]
        sql2 = "update friend set group_name = %s where usr_email = %s and " \
               "fri_email in (select fri_email from (select fri_email from friend " \
               "where usr_email = %s and group_name = %s)as T);"
        param2 = ["默认分组", usrMail, usrMail, GrpName]
        try:
            cursor.execute(sql1, param1)
            result = cursor.fetchall()
            if len(result) == 0:    # 说明分组不存在
                return 1
            cursor.execute(sql2, param2)
            self.conn.commit()
            return 0

        except pymysql.Error:
            print("Error!")
            self.conn.rollback()

    def findGrp(self, userMail, friMail):
        cursor = self.conn.cursor()
        sql = "select group_name " \
              "from friend " \
              "where usr_email = %s and fri_email = %s;"
        param = [userMail, friMail]
        try:
            cursor.execute(sql, param)
            result = cursor.fetchall()
            self.conn.commit()
            return result
        except pymysql.Error:
            print("Error!")
            self.conn.rollback()

    def addFriend(self, userMail, friMail):
        cursor = self.conn.cursor()
        sql = "insert into friend (usr_email, fri_email) values (%s, %s)"
        param = [userMail, friMail]
        try:
            cursor.execute(sql, param)
            self.conn.commit()
        except pymysql.Error:
            print("Error!")
            self.conn.rollback()

    def deleteFriend(self, userMail, friMail):
        cursor = self.conn.cursor()
        sql = "delete from friend " \
              "where usr_email = %s and fri_email = %s;"
        param = [userMail, friMail]
        try:
            cursor.execute(sql, param)
            self.conn.commit()
        except pymysql.Error:
            print("Error!")
            self.conn.rollback()

    def showfriends(self, Email):
        cursor = self.conn.cursor()
        sql = "select * " \
              "from friend " \
              "where usr_email = %s" \
              "order by group_name ASC;"
        param = [Email]
        try:
            cursor.execute(sql, param)
            result = cursor.fetchall()
            self.conn.commit()
            return result
        except pymysql.Error:
            print("Error!")
            self.conn.rollback()

    def fetch_journal(self, Email):
        cursor = self.conn.cursor()
        sql = "select * " \
              "from journal " \
              "where email = %s" \
              "order by publish_time DESC;"
        param = [Email]
        try:
            cursor.execute(sql, param)
            result = cursor.fetchall()
            self.conn.commit()
            return result
        except pymysql.Error:
            print("Error!")
            self.conn.rollback()

    def addComment(self):
        cursor = self.conn.cursor()
        sql = "insert into"
        param = [Email, Time]
        try:
            cursor.execute(sql, param)
            result = cursor.fetchall()
            self.conn.commit()
            return result
        except pymysql.Error:
            print("Error!")
            self.conn.rollback()

    def fetchSchool(self):
        cursor = self.conn.cursor()
        sql = "select school from edu_experience group by school"
        try:
            cursor.execute(sql)
            result = cursor.fetchall()
            self.conn.commit()
            return result
        except pymysql.Error:
            print("Error!")
            self.conn.rollback()

    def showView(self):
        cursor = self.conn.cursor()
        sql = "select * from summary"
        try:
            cursor.execute(sql)
            result = cursor.fetchall()
            self.conn.commit()
            return result
        except pymysql.Error:
            print("Error!")
            self.conn.rollback()

    def fetch_comment(self, Email, Time):
        cursor = self.conn.cursor()
        sql = "select * " \
              "from comment " \
              "where to_email = %s and to_time = %s" \
              "order by reply_time DESC;"
        param = [Email, Time]
        try:
            cursor.execute(sql, param)
            result = cursor.fetchall()
            self.conn.commit()
            return result
        except pymysql.Error:
            print("Error!")
            self.conn.rollback()


model = Model()
model.connect2db()
result = model.showView()
print(result)
result2= model.fetchSchool()
print(result2)