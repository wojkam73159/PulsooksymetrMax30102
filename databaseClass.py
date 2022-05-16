import os
import pymongo
import sys
import multiprocessing
import time

def db_start(*argv):#zmien z konsoli na argv ze stringa
    #lis=argv.split()
    #sys.stdout=open(os.devnull)
    index=argv.index(' ')
    port=''
    path=''
    for i in range(0,index):
        port=port+argv[i]
    for i in range(index+1,len(argv)):
        path=path+argv[i]
    #print(port)
    os.system("mongod --dbpath "+path+" --port "+port)
    #sys.stdout=open(os.devnull) nie dziala 

class Database():
    def __init__(self):
        #jesli uruchomiona baza to ja wylacz , zeby moc ja wlaczyc na znanym porcie i folderze
        try:
            #mymongoDB.shutdown()
            os.system("mongo ")
            os.system("use admin")
            os.system("db.shutdownServer()")
        except:
            pass
        

    def start(self,port="27017", path="Database"):
        #os.system("python3 mongoStartServ.py "+port+" "+path)
        self.dbProcess=multiprocessing.Process(target=db_start,args="{0} {1}".format(port,path))
        self.dbProcess.start()
        time.sleep(0.5)#hazard po wlaczeniu bazy danych w innym procesie a proba polaczenia z klientem
        #w obecnym procesie ale w praktyce nie zachodzi
        self.client=pymongo.MongoClient('localhost',int(port))
        self.dbase=self.client.patients

    def shutdown(self) :
        self.client.admin.eval("db.shutdownServer()")
        #wyrzuca blad zawsze przy wywolaniu poniewaz po wylaczeniu serwera 
        # #eval probuje zwrocic wartosc wyrazenia a do tego wciaz potrzebuje polaczenia
        #serwera nie powinno sie wylaczac jako polaczony uzytkownik z programu
        #a raczej rozlaczac sie a serwer wylaczac skryptem
        #ale u mnie jest to rownowazne , bo i tak chce zawsze wylaczac serwer w okreslonym momencie z programu
        #bo jestem wlascicielem bazy danych ktora jest lokalna 
        #musialbym uruchamiac z nowego procesu skrypt ktory wylaczy baze danych 
        #a to jest to samo dla mnie co wykonanie tej operacji i lapanie wyjatkow 
        #db.shutdownServer()
        #self.dbProcess.join()
        pass
    def putResultIn(self,imie,nazwisko,HR,SPO2):
        self.dbase.patientData.insert_one({"imie": imie, "nazwisko":nazwisko, "HR": HR, "SpO2": SPO2 })
    def findUserResults(self, imie, nazwisko):
        #self.dbase.eval("db.getCollectionNames")
        #self.dbase.create_collection("patientData",)
        #self.dbase.eval("db.find()")
        return self.dbase.patientData.find(\
        {"$and":[\
        {"imie":{"$regex":imie , "$options":'i'}},\
        {"nazwisko":{"$regex":nazwisko , "$options":'i'}}\
        ]
        })
        #return self.dbase.patientData.find()
        
    #{ "_id" : ObjectId("6029200c99535f9b316cb949"), "imie" : "wojtek", "nazwisko" : "kam", "hr" : 80, "spo" : 99 }

