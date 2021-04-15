# Importing required libraries
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Float, insert, update, delete, DateTime
# IOT Database
# Used to store data from MQTT sensors into Database

class IOT_Database:

    def __init__(self, database_name="Default_IOT.db"):
        # List of Table Objects to be created
        self.__engine = create_engine('sqlite:///' + database_name, echo=False)
        self.__meta = MetaData()
        self.__Water_Quality_Management = Table(
            'Water Quality Management', self.__meta,
            Column('id', Integer, primary_key=True),
            Column('Serial_Number', String),
            Column('pH', Float),
            Column('ORP', Float),
            Column('Conductivity', Float),
            Column('Temperature', Float),
            Column('Timestamp', DateTime)
        )

        self.__Air_Quality_Management = Table(
            'Air Quality Management', self.__meta,
            Column('id', Integer, primary_key=True),
            Column('Serial_Number', String),
            Column('CO2', Float),
            Column('Methane', Float),
            Column('CO', Float),
            Column('NO2', Float),
            Column('O3', Float),
            Column('SO2', Float),
            Column('Humidity', Float),
            Column('Temperature', Float),
            Column('Air Pressure', Float),
            Column('Luminosity', Float),
            Column('LPG', Float),
            Column('Timestamp', DateTime)
        )

        self.__Electric_Fencing = Table(
            'Electric Fencing', self.__meta,
            Column('id', Integer, primary_key=True),
            Column('Serial_Number', String),
            Column('Sensor1', Integer),
            Column('Sensor2', Float),
            Column('Sensor3', Float),
            Column('Timestamp', DateTime)
        )

        self.__Power_Management = Table(
            'Power Management', self.__meta,
            Column('id', Integer, primary_key=True),
            Column('Serial_Number', String),
            Column('Current', Integer),
            Column('Voltage', Float),
            Column('Timestamp', DateTime)
        )

        self.__Water_Monitoring = Table(
            'Water Monitoring', self.__meta,
            Column('id', Integer, primary_key=True),
            Column('Serial_Number', String),
            Column('pH', Float),
            Column('ORP', Float),
            Column('Conductivity', Float),
            Column('Temperature', Float),
            Column('Timestamp', DateTime)
        )

        self.__Solar_Panel = Table(
            'Solar Panel', self.__meta,
            Column('id', Integer, primary_key=True),
            Column('Serial_Number', String),
            Column('Current', Integer),
            Column('Voltage', Float),
            Column('Temperature', Float),
            Column('Timestamp', DateTime)
        )

        self.__Kitchen_Garden = Table(
            'Kitchen Garden', self.__meta,
            Column('id', Integer, primary_key=True),
            Column('Serial_Number', String),
            Column('Moisture', Integer),
            Column('Humidity', Float),
            Column('Temperature', Float),
            Column('Timestamp', DateTime)
        )

        self.__Smart_Lighting = Table(
            'Smart Lighting', self.__meta,
            Column('id', Integer, primary_key=True),
            Column('Serial_Number', String),
            Column('Motion', Integer),
            Column('Temperature', Float),
            Column('LDR', Float),
            Column('CO2', Float),
            Column('Timestamp', DateTime)
        )

        self.__Termite = Table(
            'Termite', self.__meta,
            Column('id', Integer, primary_key=True),
            Column('Serial_Number', String),
            Column('Discolouration', Integer),
            Column('pH', Float),
            Column('Ultra_Sound', Float),
            Column('CO2', Float),
            Column('Timestamp', DateTime)
        )

        self.__Waste_Management_System = Table(
            'Waste Management System', self.__meta,
            Column('id', Integer, primary_key=True),
            Column('Serial_Number', String),
            Column('Ultrasonic', Float),
            Column('Temperature', Float),
            Column('Timestamp', DateTime)
        )

        self.__Gardening = Table(
            'Gardening', self.__meta,
            Column('id', Integer, primary_key=True),
            Column('Serial_Number', String),
            Column('Solenoid Valve', Float),
            Column('Relay Value', Float),
            Column('Timestamp', DateTime)
        )

        # Dictionary mapping Table Name and Table Object
        self.__dict_map = dict()
        self.__dict_map['Water_Quality_Management'] = self.__Water_Quality_Management
        self.__dict_map['Air_Quality_Management'] = self.__Air_Quality_Management
        self.__dict_map['Electric_Fencing'] = self.__Electric_Fencing
        self.__dict_map['Power_Management'] = self.__Power_Management
        self.__dict_map['Water_Monitoring'] = self.__Water_Monitoring
        self.__dict_map['Solar_Panel'] = self.__Solar_Panel
        self.__dict_map['Kitchen_Garden'] = self.__Kitchen_Garden
        self.__dict_map['Smart_Lighting'] = self.__Smart_Lighting
        self.__dict_map['Termite'] = self.__Termite
        self.__dict_map['Waste_Management_System'] = self.__Waste_Management_System
        self.__dict_map['Gardening'] = self.__Gardening


    def create_table(self):
        # Function to create table schema for all tables
        self.__meta.create_all(self.__engine)

    def insert_value(self, table_name, insert_val):
        # Function to insert value into table
        print(type(insert_val))
        try:
            insert_val['Serial_Number'] = str(insert_val['Serial_Number'])
            # print(table_name, insert_val)
            db_connection = self.__engine.connect()
            # print(db_connection)
            query = self.__dict_map[table_name].insert().values(insert_val)
            print(query)
            db_connection.execute(query)
            # print(execute)
        except KeyError:
            # Return if the table name is not found
            print("Table Does Not Exist")

    def delete_serial(self, table_name, serial_no):
        try:
            db_connection = self.__engine.connect()
            query = self.__dict_map[table_name].delete().where(self.__dict_map[table_name].c.Serial_Number == serial_no)
            db_connection.execute(query)
        except KeyError:
            # Return if the table name is not found
            print("Table Does Not Exist")

    def table_content(self):
        # try:
        #     db_connection = self.__engine.connect()
        #     query = self.__dict_map[table_name].select()
        #     table_content = list()
        #     for row in db_connection.execute(query):
        #         table_content.append(row)
        #     return table_content
        # except KeyError:
        #     # Return if the table name is not found
        #     return 0
        content=dict()
        table_list=list(self.__engine.table_names())
        table_list = [x.replace(" ", "_") for x in table_list]
        for table in table_list:
            content[table]=dict()
            column_list=list(self.__dict_map[table].columns)
            column_list = [str(i).split('.')[1] for i in column_list]
            content[table]['column_names']=column_list
            db_connection = self.__engine.connect()
            query=self.__dict_map[table].select()
            row_list=list(db_connection.execute(query))
            content[table]['values']=row_list
        return(content)

    def truncate(self):
        db_connection = self.__engine.connect()
        table_list = list(self.__engine.table_names())
        table_list = [x.replace(" ", "_") for x in table_list]
        for table in table_list:
            query = self.__dict_map[table].delete()
            db_connection.execute(query)

# End of IOT_Database Class
