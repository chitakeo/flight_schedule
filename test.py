import csv
import random

def main():
    num = 0
    inspection_time = 48 #検査時間(2日=48時間)
    diagram = []
    inspection = [0] * 6 #検査
    planes = [0] * 6     #各飛行機の検査までの走行距離
    standby = [0] * 6    #スタンバイ機のフラグ      

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
    
    while num < 7:
        aircraft_check(inspection, planes, standby)
        print("検査が必要な飛行機はありますか?(yes/no)")
        val = input()
        if val == "yes":
            print("機体の番号を入力してください")
            val = input()
            inspection[int(val) - 1] = random.randint(48, 168)
            flight_schedule(diagram, inspection, standby, planes)
            day_check = dia_check(diagram)

            for dia in diagram:
                dia[5] = False

            print(str(num+1) +"日目終了")
            print(day_check)
            num += 1
        elif val == "no":
            flight_schedule(diagram, inspection, standby, planes)
            day_check = dia_check(diagram)

            for dia in diagram:
                dia[5] = False

            print(str(num+1) +"日目終了")
            print(day_check)
            num += 1
        else:
            print("yes か no で答えてください")
        
def aircraft_check(inspection, planes, standby):
    min = 1250
    num = 0

    if inspection_check(inspection) == True:
        while num < 6:
            if planes[num] < min:
                tmp = num
                min = planes[num]
            
            num += 1

        if min < 100:
            inspection[tmp] = 48
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
                #print(diagram[next][0])

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
        print(result)
        return result
    else:
        return len(diagram)

main()

