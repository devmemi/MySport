import math
import time
import os
import sys
import pandas as pd
import mysql.connector

#Parent class for the data stored in database/excel locally.
class Data():
    
    def __init__(self, parent=None, nUserKey = 0):
        super().__init__()
    
    def SetConnection(self):
        print("SetConnection")
    
    def _GetData(self,query):
        print("GetData")
    
    def _GetSports(self):
        print("GetSports")
        
    def _GetActivity(self):
        print("GetActivity")
        
    def _GetExercise(self):
        print("GetExercise")
        
    def _GetUser(self):
        print("GetUser")
    
    def _GetWorkout(self):
        print("GetWorkout")
    
    def _GetImage(self):
        print("GetImage")
    
    def _GetAllData(self):
        self._GetSports()
        self._GetActivity()
        self._GetExercise()
        self._GetUser()
        self._GetWorkout()
        self._GetImage()
    
    def RefreshSports(self):
        self._GetSports()
    
    def RefreshActivity(self):
        self._GetActivity()
    
    def RefreshExercise(self):
        self._GetExercise()
    
    def RefreshUser(self):
        self._GetUser()
    
    def RefreshWorkout(self):
        self._GetWorkout()
    
    def RefreshImage(self):
        self._GetImage()
    
    
    def RefreshData(self):
        self.RefreshSports()
        self.RefreshActivity()
        self.RefreshExercise()
        self.RefreshUser()
        self.RefreshWorkout()
    
    def FinishConnection(self):
        print("FinishConnection")
    
    def ReadData():
        print("Read")

#Class that will read/store data locally in an excel file (or a group of them)
class ExcelData(Data):
    def __init__(self, parent=None):
        super().__init__()


#Class that will read/store data in the MySQLi database
class DatabaseData(Data):
    def __init__(self, parent=None, nUserKey = 0):
        super().__init__()
        self.nUserKey = nUserKey
        
        
        self.SetConnection() 
        if self.nUserKey == 0:
            self._GetUser()
        else:
            self._GetAllData()

#        self.FinishConnection()
        
    
    def SetConnection(self):
        try:
            self.connection = mysql.connector.connect(host='localhost',
                                                 database='spt',
                                                 user='root',
                                                 password='root')
            if self.connection.is_connected():
                db_Info = self.connection.get_server_info()
                print("Connected to MySQL Server version ", db_Info)
                self.cursor = self.connection.cursor()
                self.cursor.execute("select database();")
                record = self.cursor.fetchone()
                print("You're connected to database: ", record)
        
        except mysql.connector.Error as e:
            print("Error while connecting to MySQL", e)
    

    def _ExecuteQuery(self,query):
        try:
            if self.connection.is_connected():
                self.cursor.execute(query)
                record = self.cursor.fetchone()
                return record
            else:
                print("Error: Connection already closed.Call SetConnection() to" 
                      " stablish again")
                return None
        except Exception as e:
            self.FinishConnection()
            return None
    
    #####################################################################
    # Read data
    #####################################################################        
    def _GetData(self,query):
        try:
            if self.connection.is_connected():
                result_dataFrame = pd.read_sql(query,self.connection)
                return result_dataFrame
            else:
                print("Error: Connection already closed.Call SetConnection() to" 
                      " stablish again")
                return None
        except Exception as e:
            self.FinishConnection()
            return None 
        
    def _GetSports(self):
        query ="Select * from sport;"
        self.SportsData = self._GetData(query)
        
    def _GetActivity(self):
        query ="Select * from activity;"
        self.ActivityData = self._GetData(query)
        
    def _GetExercise(self):
        query ="Select * from exercise;"
        self.ExerciseData = self._GetData(query)
        
    def _GetUser(self):
        query ="Select * from user;"
        self.UserData = self._GetData(query)
    
    def _GetWorkout(self):
        query ="Select * from workout;"
        self.WorkoutData = self._GetData(query)
    
    def _GetImage(self):
        query ="Select * from image;"
        self.ImageData = self._GetData(query)
    
        
    
    #####################################################################
    # Insert data
    #####################################################################
    def _InsertData(self,query):
        self._ExecuteQuery(query)
        
    def _InsertSport(self):
        query ="Select * from sport;"
        self._InsertData(query)
        
    def _InsertActivity(self):
        query ="Select * from activity;"
        self._InsertData(query)
        
    def _InsertExercise(self):
        query ="Select * from exercise;"
        self._InsertData(query)
        
    def _InsertUser(self):
        query ="Select * from user;"
        self._InsertData(query)
    
    def _InsertWorkout(self):
        query ="Select * from workout;"
        self._InsertData(query)
    
    def _InsertImage(self):
        query ="Select * from image;"
        self._InsertData(query)
    
    #####################################################################
    # Update data
    #####################################################################
    def _UpdateData(self,query):
        self._ExecuteQuery(query)
    
    def _UpdateSport(self):
        query ="Select * from sport;"
        self._UpdateData(query)
        
    def _UpdateActivity(self):
        query ="Select * from activity;"
        self._UpdateData(query)
        
    def _UpdateExercise(self):
        query ="Select * from exercise;"
        self._UpdateData(query)
        
    def _UpdateUser(self):
        query ="Select * from user;"
        self._UpdateData(query)
    
    def _UpdateWorkout(self):
        query ="Select * from workout;"
        self._UpdateData(query)
    
    def _UpdateImage(self):
        query ="Select * from image;"
        self._UpdateData(query)
    
    #####################################################################
    # Delete data
    #####################################################################
    def _DeleteData(self,query):
        self._ExecuteQuery(query)
    
    def _DeleteSport(self):
        query ="Select * from sport;"
        self._DeleteData(query)
        
    def _DeleteActivity(self):
        query ="Select * from activity;"
        self._DeleteData(query)
        
    def _DeleteExercise(self):
        query ="Select * from exercise;"
        self._DeleteData(query)
        
    def _DeleteUser(self):
        query ="Select * from user;"
        self._DeleteData(query)
    
    def _DeleteWorkout(self):
        query ="Select * from workout;"
        self._DeleteData(query)
    
    def _DeleteImage(self):
        query ="Select * from image;"
        self._DeleteData(query)
    
    
    def FinishConnection(self):
        if self.connection.is_connected():
            self.cursor.close()
            self.connection.close()
            print("MySQL connection is closed")