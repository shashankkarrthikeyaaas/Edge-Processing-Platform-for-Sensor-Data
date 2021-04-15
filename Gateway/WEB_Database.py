# Importing required libraries
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Float, insert, update, delete, DateTime

# WEB Database class
# Used for REST API authentication
class WEB_Database:
    def __init__(self, database_name="Default_Users.db"):
        # List of Table Objects to be created
        self.__engine = create_engine('sqlite:///' + database_name, echo=False)
        self.__meta = MetaData()
        self.__Users = Table(
            'Users', self.__meta,
            Column('id', Integer, primary_key=True),
            Column('Name', String),
            Column('Username', String),
            Column('Password', String)
        )
        self.__Configuration = Table(
            'Configuration', self.__meta,
            Column('id', Integer, primary_key=True),
            Column('Serial_Number', String),
            Column('Updated',String,default="Yes"),
            Column('Time_Interval', Integer, default=1000)
        )
        self.__E_Mail = Table(
            'E-Mail',self.__meta,
            Column('id', Integer, primary_key=True),
            Column('Serial_Number', String),
            Column('E_Mail', String, default=1000),
        )
        self.__Config= Table(
            'Config',self.__meta,
            Column('id', Integer, primary_key=True),
            Column('Serial_Number', String),
            Column('Time_Interval', Integer, default=10000),
        )


    def create_table(self):
        self.__meta.create_all(self.__engine)

    def insert_time_config(self,sno,time):
        sno=str(sno).upper()
        time=int(time)
        db_connection = self.__engine.connect()
        query = self.__Config.select().where((self.__Config.c.Serial_Number == sno))
        row = db_connection.execute(query)
        no_el=len(list(row))
        print(no_el)
        if no_el == 0:
            db_connection = self.__engine.connect()
            query = self.__Config.insert().values({'Serial_Number':sno,'Time_Interval':time})
            db_connection.execute(query)
        else:
            db_connection = self.__engine.connect()
            query = self.__Config.update().where((self.__Config.c.Serial_Number == sno )).values({'Time_Interval': time})
            db_connection.execute(query)

    def ret_config_list(self):
        db_connection = self.__engine.connect()
        query = self.__Config.select()
        return_list=list()
        for row in db_connection.execute(query):
            return_list.append(row)
        query=self.__Config.delete()
        db_connection.execute(query)
        return(return_list)


    def insert_configuration(self,insert_val):
        # Insert into Configuration
        sno=insert_val['Serial_Number']
        sno=str(sno)
        insert_val['Serial_Number']=sno
        db_connection = self.__engine.connect()
        query = self.__Configuration.select().where((self.__Configuration.c.Serial_Number == insert_val['Serial_Number']))
        print(insert_val['Serial_Number'])
        # print(insert_val['Serial_Number'],insert_val['Country_Code'],insert_val['Phone_Number'])
        row = db_connection.execute(query)
        no_el=len(list(row))
        print(no_el)
        if no_el == 0:
            db_connection = self.__engine.connect()
            query = self.__Configuration.insert().values(insert_val)
            db_connection.execute(query)
        else:
            # if Time Intreval Field is present
            print(insert_val)
            db_connection = self.__engine.connect()
            query = self.__Configuration.update().where((self.__Configuration.c.Serial_Number == insert_val['Serial_Number'])).values({'Time_Interval': insert_val['Time_Interval'] , 'Updated':"Yes"})
            db_connection.execute(query)

    def del_configuration_sno(self,sno):
        db_connection = self.__engine.connect()
        query = self.__Configuration.select().where(self.__Configuration.c.Serial_Number == sno)
        return_list = [i for i in db_connection.execute(query)]
        if len(list(return_list)) == 0:
            return 0
        else:
            query = self.__Configuration.delete().where(self.__Configuration.c.Serial_Number == sno)
            db_connection.execute(query)
            return 1

    def push_info(self):
        db_connection = self.__engine.connect()
        query=self.__Configuration.select().where(self.__Configuration.c.Updated =="Yes")
        row_list=list()
        for row in db_connection.execute(query):
            row_list.append(row)
        query=self.__Configuration.update().where(self.__Configuration.c.Updated =="Yes").values({'Updated':"No"})
        db_connection.execute(query)
        return row_list

    def insert_configuration_email(self, insert_val):
        # Insert into Configuration
        sno = insert_val['Serial_Number']
        sno = str(sno)
        insert_val['Serial_Number'] = sno
        db_connection = self.__engine.connect()
        query = self.__E_Mail.select().where(
            (self.__E_Mail.c.Serial_Number == insert_val['Serial_Number']))
        # print(insert_val['Serial_Number'],insert_val['Country_Code'],insert_val['Phone_Number'])
        row = db_connection.execute(query)
        no_el = len(list(row))
        if no_el == 0:
            db_connection = self.__engine.connect()
            query = self.__E_Mail.insert().values(insert_val)
            db_connection.execute(query)
        else:
            db_connection = self.__engine.connect()
            query = self.__E_Mail.update().where((self.__E_Mail.c.Serial_Number == insert_val['Serial_Number'])).values({'E_Mail': insert_val['E_Mail']})
            db_connection.execute(query)


    def get_configuration_email_sno(self,sno):
        db_connection = self.__engine.connect()
        query = self.__E_Mail.select().where(self.__E_Mail.c.Serial_Number == sno)
        return_list = [i for i in db_connection.execute(query)]
        if len(list(return_list))==0 :
            return 0
        else:
            return return_list


    def del_configuration_email(self,sno,email):
        db_connection = self.__engine.connect()
        query = self.__E_Mail.select().where((self.__E_Mail.c.Serial_Number == sno)&(self.__E_Mail.c.E_Mail == email))
        return_list = [i for i in db_connection.execute(query)]
        if len(list(return_list)) == 0:
            return 0
        else:
            query = self.__E_Mail.delete().where((self.__E_Mail.c.Serial_Number == sno)&(self.__E_Mail.c.E_Mail == email))
            db_connection.execute(query)
            return 1

    def del_configuration_email_sno(self,sno):
        db_connection = self.__engine.connect()
        query = self.__E_Mail.select().where((self.__E_Mail.c.Serial_Number == sno))
        return_list = [i for i in db_connection.execute(query)]
        if len(list(return_list)) == 0:
            return 0
        else:
            query = self.__E_Mail.delete().where((self.__E_Mail.c.Serial_Number == sno))
            db_connection.execute(query)
            return 1



    def insert_value(self, name, username, password):
        username=str(username).upper()
        password=str(password).upper()
        db_connection = self.__engine.connect()
        query = self.__Users.select().where(self.__Users.c.Username == username)
        row = db_connection.execute(query)
        if len(list(row)) == 0:
            query = self.__Users.insert().values({'Username': username, 'Password': password, 'Name': name})
            db_connection.execute(query)
            return 1
        else:
            return 0

    def delete_value(self, username):
        username=str(username).upper()
        db_connection = self.__engine.connect()
        query = self.__Users.select().where(self.__Users.c.Username == username)
        row = db_connection.execute(query)
        if len(list(row)) == 0:
            return 0
        else:
            query = self.__Users.delete().where(self.__Users.c.Username == username)
            db_connection.execute(query)
            return 1

    def update_value(self, username, password):
        username=str(username).upper()
        db_connection = self.__engine.connect()
        query = self.__Users.select().where(self.__Users.c.Username == username)
        row = db_connection.execute(query)
        if len(list(row)) == 0:
            return 0
        else:
            query = self.__Users.update().where(self.__Users.c.Username == username).values({'Password': password})
            db_connection.execute(query)
            return 1

    def get_password(self,username):
        username=str(username).upper()
        db_connection = self.__engine.connect()
        query = self.__Users.select().where(self.__Users.c.Username == username)
        row = db_connection.execute(query)
        no_el = len(list(row))
        # print(no_el)
        if no_el == 0:
            return 0
        else:
            table_content = list()
            for row in db_connection.execute(query):
                table_content.append(row)
            return (table_content[0][0],table_content[0][2],table_content[0][3])

    def find_id(self,_id):
        db_connection = self.__engine.connect()
        query = self.__Users.select().where(self.__Users.c.id == _id)
        row = db_connection.execute(query)
        no_el = len(list(row))
        # print(no_el)
        if no_el == 0:
            return 0
        else:
            table_content = list()
            for row in db_connection.execute(query):
                table_content.append(row)
            return (table_content[0][0],table_content[0][2],table_content[0][3])

    def truncate(self):
        db_connection = self.__engine.connect()
        query = self.__Users.delete()
        db_connection.execute(query)

#     def table_content(self):
#         try:
#             db_connection=self.__engine.connect()
#             query=self.__Users.select()
#             table_content=list()
#             for row in db_connection.execute(query):
#                 table_content.append(row)
#             return table_content
#         except KeyError:
#             return 0

# End of User Database Class
