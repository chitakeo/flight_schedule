import csv

def main():
    num = 0
    inspection_time = 48 #検査時間(2日=48時間)
    diagram = []
    planes = [0] * 6     #各飛行機の検査までの走行距離
    frag = [0] * 6       #スタンバイ機のフラグ      
    
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
    ''' いちいち実行するのめんどいので
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

    '''
    #本番は以下6行消します
    planes[0] = 1050
    planes[1] = 850
    planes[2] = 650
    planes[3] = 450
    planes[4] = 40
    planes[5] = 1240

    num = 0
    frag[decision_standby(planes)] = True

    print("\n運行開始\n")
    
    while num < 14:
        flight_schedule(diagram, frag, planes)
        print(str(num+1) +"日目終了")
        
        for row in diagram:
            row[5] = False

        num += 1

def decision_standby(planes):
    result = planes.index(min(planes))
    
    return result

def time_calculation(time):
    result = time.split(':')
    
    return int(result[0]) + int(result[1])/60

def flight_schedule(diagram, standby, planes):
    num = 0
    while num < 6:
        if standby[num] == True:
            print("飛行機" + str(num+1) + "検査まであと" + str(planes[num]) + "km スタンバイ")
        else:
            time = 3.00
            place = "start"
            print("飛行機"+ str(num+1))
            next = 0
            
            while True:
                next = next_flight(diagram, place, time)
                place = diagram[next][3]
                time = diagram[next][4]
                diagram[next][5] = True
                if next_flight(diagram, place, time) == -1:
                    break

                print(diagram[next][0])

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
        return -1

main()

