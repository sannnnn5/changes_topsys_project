def all_a():
    car_price,car_range,car_power,car_100,car_top_spd=main()
    cp_p, cr_p, cpp_p, c1_p, t_p=wight_inp()
    cp, cr, cpp, c1, t=calculate_input(cp_p, cr_p, cpp_p, c1_p, t_p)
    qm,qx=shed(cp, cr, cpp, c1, t)
    bed=step4bad(qx,cp, cr, cpp, c1, t)
    good=step4good(qm,cp, cr, cpp, c1, t)
    fin=fin_num(good,bed)
    

    return fin



def main():
    
    # მონაცემთა ბაზა.რაც ამ სტეპის ნაწილში უნდა დასორტირდეს იმ გვარად რომ კატეგორიების მიხედვით გადანაწილდეს მოდელი და კატეგორიის მონაცემი
    data_list=[]
    data={}

    while True:
        user=input("model: ")
        
        
        if user:
            data_list.append(user)
        elif user=="":
            data["model"]=data_list
            len_models=len(data_list)
            break
    data_price=[]
    data_range=[]
    data_power=[]
    data_accs=[]
    data_speed=[]
    while len_models > 0:
        len_models-=1
        user_p=input("price: ")
        data_price.append(user_p)
        user_r=input("range: ")
        data_range.append(user_r)
        user_pp=input("power: ")
        data_power.append(user_pp)
        user_a=input("accs: ")
        data_accs.append(user_a)
        user_s=input("speed: ")
        data_speed.append(user_s)
    data['Price']=data_price
    data['Range_miles']=data_range
    data['power']=data_power
    data['0-100_km_h_seconds']=data_accs
    data['Top_Speed_mph_2']=data_speed
    print(data)

    car_price={}
    
    car_range={}

    car_power={}

    car_100={}
    
    car_top_spd={}
    
# აქ ფორმულას გამოყავს საშვალო რიცხვი თავის კატეგორიიდან
    prc_sum=sum(data['Price'])
    for car,coast in zip(data['Model'],data['Price']):
        car_price[car]=coast/(prc_sum*2)*0.5

    range_sum=sum(data['Range_miles'])
    for car,range in zip(data['Model'],data['Range_miles']):
        car_range[car]=range/(range_sum*2)*0.5

    power_sum=sum(data['power'])
    for car,power in zip(data['Model'],data['power']):
        car_power[car]=power/(power_sum*2)*0.5

    to_100_sum=sum(data['0-100_km_h_seconds'])
    for car,c100 in zip(data['Model'],data['0-100_km_h_seconds']):
        car_100[car]=c100/(to_100_sum*2)*0.5

    top_speed_sum=sum(data['Top_Speed_mph_2'])
    for car,top_spd in zip(data['Model'],data['Top_Speed_mph_2']):
        car_top_spd[car]=top_spd/(top_speed_sum*2)*0.5

    return car_price,car_range,car_power,car_100,car_top_spd



def wight_inp():
    while True:
        user = input("If you want to change the percentage, type yes.\nIf you do not want to change the percentage, type no: ").lower()
        if user == "no":
            return 20, 20, 20, 20, 20 
        elif user == "yes":
            result = []
            total = 100
            while True:
                try:
                    ask = float(input("Enter percentage: "))
                    if ask < 0 or ask > 100:
                        print("Percentage must be between 0 and 100.")
                        continue
                    if sum(result) + ask > 100:
                        print("You have exceeded the total percentage. Please re-enter.")
                        total=100
                        result = []  # Reset the result list if the total exceeds 100%
                        continue
                        
                    result.append(ask)
                    total -= ask
                    print(f"Remaining percentage: {total}")
                    
                    if len(result) == 5 and total == 0:
                        return tuple(result)
                    
                except ValueError:
                    print("Invalid input. Please enter a number.")
        else:
            print("Invalid input. Please type 'yes' or 'no'.")
            continue

        cp_p, cr_p, cpp_p, c1_p, t_p=result
        return cp_p, cr_p, cpp_p, c1_p, t_p

def calculate_input(cp_p, cr_p, cpp_p, c1_p, t_p):

    cp, cr, cpp, c1, t = main()
    for i, e in zip(cp.values(), cp.keys()):
        if cp_p > 0:    
            cp[e] = (i * cp_p)/100
        else:
            cp[e] = i/100
    for i, e in zip(cr.values(), cr.keys()):
        if cr_p > 0:    
            cr[e] = (i * cr_p)/100
        else:
            cr[e] = i/100
    for i, e in zip(cpp.values(), cpp.keys()):
        if cpp_p > 0:
            cpp[e] = (i * cpp_p)/100
        else:
            cpp[e] = i/100
    for i, e in zip(c1.values(), c1.keys()):
        if c1_p > 0:
            c1[e] = (i * c1_p)/100
        else:
            c1[e] = i/100
    for i, e in zip(t.values(), t.keys()):
        if t_p > 0:    
            t[e] = (i * t_p)/100
        else:
            t[e] = i/100
    # print(cp,"\n",cr,"\n",cpp,"\n",c1,"\n",t)
    return cp, cr, cpp, c1, t


# # ამ სტეპს გამოგვაქვს მინიმალური და მაქსიმალური მნიშვნელობის მქონე ობიექტები კატეგორიებიდან. სტეპ 2 დან შემოტანილ ბიბლიოტეკაში.

def shed(q,w,e,r,t):
    q_min={}
    q_max={}

    

    
    # ვადგენ მინიმუმ და მაქსიმუმ მონაცემების მქონე ობიექტს ფასებიდან
    q_min["price"]=min(q.values())
    q_max["price"]=max(q.values())
    
    # ვადგენ მინიმუმ და მაქსიმუმ მონაცემების მქონე ობიექტს რეინჯიდან
    q_max["range"]=max(w.values())
    q_min["range"]=min(w.values())
    
            
    q_max["power"]=max(e.values())
    q_min["power"]=min(e.values())
    

    q_min["accseleration"]=min(r.values())
    q_max["accseleration"]=max(r.values())   

    q_max["speed"]=max(t.values())
    q_min["speed"]=min(t.values())
    
    bed_result={
    }
    good_res={}

    us_price=input("> price <")
    us_range=input("> range <")
    us_power=input("> power <")
    us_accseleration=input("> accseleration <")
    us_speed=input("> top_speed <")
    

    if us_price == "<":
        good_res["price"]=q_min['price']
        bed_result["price"]=q_max["price"]
    elif us_price ==">":
        good_res["price"]=q_max["price"]
        bed_result["price"]=q_min["price"]

    if us_range == "<":
        good_res["range"]=q_min['range']
        bed_result["range"]=q_max["range"]
    elif us_range ==">":
        good_res["range"]=q_max["range"]
        bed_result["range"]=q_min["range"]
    
    if us_power == "<":
        good_res["power"]=q_min['power']
        bed_result["power"]=q_max["power"]
    elif us_power ==">":
        good_res["power"]=q_max["power"]
        bed_result["power"]=q_min["power"]
    
    if us_accseleration == "<":
        good_res["accseleration"]=q_min['accseleration']
        bed_result["accseleration"]=q_max["accseleration"]
    elif us_accseleration ==">":
        good_res["accseleration"]=q_max["accseleration"]
        bed_result["accseleration"]=q_min["accseleration"]
    
    if us_speed == "<":
        good_res["speed"]=q_min['speed']
        bed_result["speed"]=q_max["speed"]
    elif us_speed ==">":
        good_res["speed"]=q_max["speed"]
        bed_result["speed"]=q_min["speed"]
    
    
    return good_res,bed_result

def step4bad(bed_result,car_price,range,power,accs,top):
    

    cars={}

    for pr,r,po,acc,t in zip(car_price,range,power,accs,top):
        # print(car_price[pr])
        # print(bed_result["price"])
        all_sum = 0
        if car_price[pr] > bed_result["price"]:
            
            all_sum= ((car_price[pr] - bed_result["price"]) * 2)   
            
        elif car_price[pr] < bed_result["price"]:
            all_sum = ((bed_result["price"] - car_price[pr]) * 2)            
            
        if range[r] > bed_result["range"]:
            all_sum += ((range[r] - bed_result["range"]) * 2)
        elif range[r] < bed_result["range"]:
            all_sum += ((bed_result["range"] - range[r]) * 2)
        
        
        if power[po] > bed_result["power"]:
            all_sum += ((power[po] - bed_result["power"]) * 2)
        elif power[po] < bed_result["power"]:
            all_sum += ((bed_result["power"] - power[po]) * 2)
        
        
        if accs[acc] > bed_result["accseleration"]:
            all_sum += ((accs[acc] - bed_result["accseleration"]) * 2)
        elif accs[acc] < bed_result["accseleration"]:
            all_sum += ((bed_result["accseleration"] - accs[acc]) * 2)
        
        
        if top[t] > bed_result["speed"]:
            all_sum += ((top[t] - bed_result["speed"]) * 2)
        elif top[t] < bed_result["speed"]:
            all_sum += ((bed_result["speed"] - top[t]) * 2)
        
        cars[pr]=all_sum*0.5
    return cars


def step4good(good_res,car_price,range,power,accs,top):
    cars={}

    for pr,r,po,acc,t in zip(car_price,range,power,accs,top):
        
        all_sum = 0
        if car_price[pr] > good_res["price"]:
            
            all_sum= ((car_price[pr] - good_res["price"]) * 2)   
            
        elif car_price[pr] < good_res["price"]:
            all_sum = ((good_res["price"] - car_price[pr]) * 2)            
            
        if range[r] > good_res["range"]:
            all_sum += ((range[r] - good_res["range"]) * 2)
        elif range[r] < good_res["range"]:
            all_sum += ((good_res["range"] - range[r]) * 2)
        
        
        if power[po] > good_res["power"]:
            all_sum += ((power[po] - good_res["power"]) * 2)
        elif power[po] < good_res["power"]:
            all_sum += ((good_res["power"] - power[po]) * 2)
        
        
        if accs[acc] > good_res["accseleration"]:
            all_sum += ((accs[acc] - good_res["accseleration"]) * 2)
        elif accs[acc] < good_res["accseleration"]:
            all_sum += ((good_res["accseleration"] - accs[acc]) * 2)
        
        
        if top[t] > good_res["speed"]:
            all_sum += ((top[t] - good_res["speed"]) * 2)
        elif top[t] < good_res["speed"]:
            all_sum += ((good_res["speed"] - top[t]) * 2)
        
        cars[pr]=all_sum*0.5
    return cars

def fin_num(min_num,max_num):
    
    

    fin={}
    fin_sum=0
    for mi,mx in zip(min_num,max_num):
        fin_sum=max_num[mx]/(min_num[mi]+ max_num[mx])
        fin[mi]=fin_sum
    my_dict=fin
    sorted_values_desc = sorted(my_dict.items(), key=lambda x: x[1], reverse=True) 
    
    return sorted_values_desc

a=all_a()
for i in a:
    print(i)