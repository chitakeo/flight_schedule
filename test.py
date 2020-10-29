import csv
import random

def main():
    num = 0
    inspection_time = 48 #検査時間(2日=48時間)
    diagram = []
    inspection = [0] * 6 #検査
    planes = [0] * 6     #各飛行機の検査までの走行距離
    standby = [0] * 6    #スタンバイ機のフラグ      

    while True:
        print("年を入れてください")
        year = input()
        if str.isdecimal(year) == True:
            break

        print("数値を入れて下さい")

    while True:
        print("月を入れてください")
        month = input()
        if str.isdecimal(month) == True:
            if 1 <= int(month) <= 12:
                break
            
        print("1から12の数値を入れて下さい")

    day_information = [[[0] * 6 for i in range(3)] for j in range(day_of_month(month, year)+1)]
    
    with open('diagram.csv') as f:
        reader = csv.reader(f)
        for row in reader:
            if num > 0:
                diagram.append(row)
                diagram[num-1][2] = time_calculation(diagram[num-1][2])
                diagram[num-1][4] = time_calculation(diagram[num-1][4])
                diagram[num-1].append(False)
            
            num += 1
    
    num = 0
    #いちいち実行するのめんどいので
    '''
    while num < 6:
        print("飛行機" + str(num+1) + "の走行距離を入力してください")
        val = input()
        print("飛行機" + str(num+1) + "の前回整備実施時の走行距離を入力してください")
        val2 = input()
        if str.isdecimal(val) == True and str.isdecimal(val2) == True:
            planes[num] = 1250 - (int(val) - int(val2))
            num +=1
        else:
            print("数値を入れて下さい")

    
    #本番は以下6行消します
    '''
    planes[0] = 1050
    planes[1] = 850
    planes[2] = 650
    planes[3] = 450
    planes[4] = 40
    planes[5] = 1240
    
    num = 0
    
    print("\n運行開始\n")
    
    flight_month(1, day_information, day_of_month(month, year), diagram, 0, inspection, standby, planes)
   
    while num < day_of_month(month, year):
        print(year + "年" + month + "月" + str(num+1) + "日")
        print("検査が必要な飛行機はありますか?(yes/no)")
        emergency = input()

        if emergency != "yes" and emergency != "no":
            print("yes か no を入力してください")
            num - 1
        elif emergency == "yes":
            while True:
                print("機体の番号を入力してください")
                plane = input()
                if 1 <= int(plane) <= 6:
                    flight_month(num+1, day_information, day_of_month(month, year), diagram, int(plane), inspection, standby, planes)
                    print(day_information)
                    break
                print("1~6の数値を入力してください") 

        num += 1


def aircraft_check(inspection, planes, standby):
    min = 1250
    num = 0

    for sta in standby:
        standby[num] = False
        num += 1

    num = 0

    if inspection_check(inspection) == True:
        while num < 6:
            if planes[num] < min:
                tmp = num
                min = planes[num]
            
            num += 1

        if min < 100:
            inspection[tmp] = 48
            tmp = 0
            
            while tmp < len(standby):
                standby[tmp] = False
                tmp += 1
    else:
        for ins in inspection: 
            ins -= 24
            if ins <= 0:
                ins = 0

    if inspection_check(inspection) == True:
        standby[planes.index(max(planes))] = True

def inspection_check(inspection):
    result = True

    for ins in inspection:
        if ins != 0:
            result = False

    return result

def decision_standby(standby):
    return 0
    
def dia_check(diagram):
    result = True

    for dia in diagram:
        if dia[5] == False:
            result = False

    return result

def time_calculation(time):
    result = time.split(':')
    
    return int(result[0]) + int(result[1])/60

def flight_schedule(diagram, inspection, standby, planes):
    num = 0
    while num < 6:
        if inspection[num] != 0:
            print("飛行機" + str(num+1) + "検査中。検査終了まで後" + str(inspection[num]) + "時間")
            inspection[num] -= 24
            if inspection[num] <= 0:
                inspection[num] = 0
                planes[num] = 1250 

        elif standby[num] == True:
            print("飛行機" + str(num+1) + "検査まであと" + str(planes[num]) + "km スタンバイ")
        else:
            amount_time = 0
            time = 3.00
            place = "start"
            print("飛行機"+ str(num+1))
            next = 0

            while True:
                next = next_flight(diagram, place, time)
                if next == len(diagram):
                    break
                place = diagram[next][3]
                time = diagram[next][4]
                amount_time += diagram[next][4] - diagram[next][2]
                diagram[next][5] = True
                print(diagram[next][0])

            planes[num] -= amount_time
            print("検査まであと" + str(planes[num]) + "km")
            
        num += 1

def next_flight(diagram, place, time):
    num = 0
    min_time = 24
    frag = True
    while num < len(diagram):
        if diagram[num][5] == False:
            if place == "start":
                if diagram[num][2] - time >= 1:
                    if diagram[num][2] - time < min_time:
                        min_time = diagram[num][2] - time
                        result = num
                        frag = False
            else:             
                if diagram[num][1] == place:
                    if diagram[num][2] - time >= 1:
                        if diagram[num][2] - time < min_time:
                            min_time = diagram[num][2] - time
                            result = num
                            frag = False


        num += 1

    if frag == False:
        return result
    else:
        return len(diagram)

def day_of_month(month, year):
    month = int(month)
    year = int(year)
    
    if month == 2:
        if year % 4 == 0:
            if year % 100 == 0:
                if year % 400 == 0:
                    return 29
                else:
                    return 28
            else:
                return 29
        else:
            return 28
    elif month == 4 or month == 6 or month == 9 or month == 11:
        return 30
    elif month == 1 or month == 3 or month == 5 or month == 7 or month == 8 or month == 10 or month == 12:
        return 31

def flight_month(day, day_information, day_of_month, diagram, emergency, inspection, standby, planes):
    if emergency != 0:
        inspection[emergency] = random.randint(48, 168)
    
    while day-1 < day_of_month:
        print(str(day) +"日の運行状況")
        aircraft_check(inspection, planes, standby)
        if day-1 == 0:
            num = 0
            while num < 6:
                day_information[0][0][num] = inspection[num]
                day_information[0][1][num] = standby[num]
                day_information[0][2][num] = planes[num]

                num += 1

        flight_schedule(diagram, inspection, standby, planes)
        day_check = dia_check(diagram)

        for dia in diagram:
            dia[5] = False

        num = 0
        
        while num < 6:
            day_information[day][0][num] = inspection[num]
            day_information[day][1][num] = standby[num]
            day_information[day][2][num] = planes[num]

            num += 1

    
       
        print(day_check)
        day += 1
       



main()

