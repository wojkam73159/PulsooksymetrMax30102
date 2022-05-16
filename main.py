import os
import string
import display
import time
import math
import databaseClass


from heartrate_monitor2 import HeartRateMonitor
import time
import argparse
print("aby dokonac pomiaru z zapisem do bazy danych wpisz \"1\"")
print("aby dokonac odczytu z bazy wpisz \"2\"")
mojeLcd=display.lcd()
mojeLcd.lcd_display_string("1-pomiar",1,0)
mojeLcd.lcd_display_string("2-odczyt",2,0)
mojeLcd.lcd_clear()
messageFromUsr=int(input())
#print("M:{0},".format(type(messageFromUsr)))
while messageFromUsr!=1 and messageFromUsr!=2:
    print("aby dokonac pomiaru z zapisem do bazy danych wpisz \"1\"")
    print("aby dokonac odczytu z bazy wpisz \"2\"")
    messageFromUsr=int(input())
if(messageFromUsr==1):
    print("podaj swoje imie:")
    mojeLcd.lcd_clear()
    mojeLcd.lcd_display_string("podaj swoje imie:",1,0)
    imie=input()

    
    
    print("podaj swoje nazwisko:")
    mojeLcd.lcd_clear()
    mojeLcd.lcd_display_string("podaj swoje nazwisko:",1,0)
    nazwisko=input()
    print("poloz palec na czujniku i nacisnij y:")
    mojeLcd.lcd_clear()
    mojeLcd.lcd_display_string("y-palec na",1,0)
    mojeLcd.lcd_display_string("czujniku",2,0)
    messageFromUsr=input()
    while messageFromUsr!='y':
        print("poloz palec na czujniku i nacisnij y:")
        messageFromUsr=input()
    #os.system("python mainDoug.py | tee temp.txt")
    parser = argparse.ArgumentParser(description="Read and print data from MAX30102")
    parser.add_argument("-r", "--raw", action="store_true",
                        help="print raw data instead of calculation result")
    parser.add_argument("-t", "--time", type=int, default=30,
                        help="duration in seconds to read from sensor, default 30")
    args = parser.parse_args()

    print('sensor starting...')
    mojeLcd.lcd_clear()
    mojeLcd.lcd_display_string("nie ruszaj sie",1,0)
    hrm = HeartRateMonitor(print_raw=args.raw, print_result=(not args.raw))
    hrm.start_sensor()
    try:
        time.sleep(args.time)
    except KeyboardInterrupt:
        print('keyboard interrupt detected, exiting...')

    hrm.stop_sensor()
    print('sensor stoped!')

    F=open("temp.txt")
    hr=[]
    spo=[]
    hrCount=0
    spoCount=0
    lines=F.readlines()
    lines=lines[1:len(lines)-1:1]
    for line in lines:
        temp=line.split()
        #print(temp[1][0:len(temp[1])-1:1])
        #print("hi:{val1}".format(val1=temp[1]))
        #line[1]=line[1].rstrip(",")
        hrTemp=float(temp[1][0:len(temp[1])-1:1])
        spoTemp=float(temp[3])
        if hrTemp>0:
            hr.append(hrTemp)
            hrCount+=1
        if spoTemp>0:
            spo.append(spoTemp)
            spoCount+=1
        #print(temp)
    meanHR=sum(hr)/hrCount
    meanSPO=sum(spo)/spoCount
    F.close()
    #F=open("users.txt","a")
    #F.write("imie: {0}, nazwisko:{1}, BPM: {2}, SpO2: {3} \n".format(imie, nazwisko,meanHR, meanSPO))
    #F.close()
    print(meanHR)
    print(meanSPO)
    
    meanHR=math.floor(meanHR)
    meanSPO=math.floor(meanSPO)
    mojeLcd.lcd_display_string("HR:"+str(meanHR),1,0)
    mojeLcd.lcd_display_string("SPO:"+str(meanSPO),2,0)

    mymongoDB=databaseClass.Database()
    mymongoDB.start()
    mymongoDB.putResultIn(imie,nazwisko,meanHR,meanSPO)
    time.sleep(10)
    mojeLcd.lcd_clear()
    try:
        mymongoDB.shutdown()
    except:
        pass
if(messageFromUsr==2):#odczyt z bd

    mymongoDB=databaseClass.Database()
    print("podaj swoje imie:")
    mojeLcd.lcd_clear()
    imie=input()
    print("podaj swoje nazwisko:")
    mojeLcd.lcd_clear()
    nazwisko=input()

    mymongoDB.start()
    #mymongoDB.putResultIn("Wojciech","Kaminski",80,99)
    res=mymongoDB.findUserResults(imie,nazwisko)
    #print("resultat tutaj:{0}".format(res))#to do poprawic funkcje find kod z kompa stacjonarnego
    indeks=1
    for doc in res:
        #print("resultat tutaj:{0}".format(doc.values()))
        temp=[doc["imie"],doc["nazwisko"],doc["HR"],doc["SpO2"]]
        print("{0} {1} hr:{2} spo2:{3}".format(temp[0],temp[1],temp[2],temp[3]))
        mojeLcd.lcd_clear()
        mojeLcd.lcd_display_string("{0}".format(temp[0]),1,0)
        mojeLcd.lcd_display_string("{0}".format(temp[1]),2,0)
        time.sleep(3)
        mojeLcd.lcd_clear()
        mojeLcd.lcd_display_string("pomiar nr{1} hr:{0}".format(temp[2],indeks),1,0)
        mojeLcd.lcd_display_string("spo2:{0}".format(temp[3]),2,0)
        time.sleep(3)
        indeks+=1
        
    try:
        mymongoDB.shutdown()
    except:
        pass

    time.sleep(3)
    mojeLcd.lcd_clear()