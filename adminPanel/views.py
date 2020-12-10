from django.shortcuts import render, HttpResponse, redirect

import cx_Oracle

from matplotlib import pyplot as plt
from matplotlib.pyplot import figure
import numpy as np


# Create your views here.

def adminDashboard(request):
    return render(request, 'adminPanel/adminDashboard.html')

def userData(request):

    dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='ORCL')
    conn = cx_Oracle.connect(user='bikroy', password='bikroy', dsn=dsn_tns)
    c = conn.cursor()

    sql = """   SELECT ac.USERNAME, FIRST_NAME||' '|| LAST_NAME, ac.EMAIL, pf.PHONE_NO, loc.THANA, loc.DISTRICT, loc.DIVISION, loc.ZIP_CODE 
                FROM ACCOUNT ac, PROFILE pf, LOCATION loc
                WHERE ac.PROFILE_NO=pf.PROFILE_NO and pf.LOCATION_ID=loc.LOCATION_ID
                ORDER BY ac.username ASC
            """
    c.execute(sql)
    result = []
    result = c.fetchall()

    user_name = []
    profile_name = []
    email = []
    phone_no = []
    thana = []
    district = []
    division = []
    zip_code = []
   

    for row in result:
        user_name.append(row[0])
        profile_name.append(row[1])
        email.append(row[2])
        phone_no.append(row[3])
        thana.append(row[4])
        district.append(row[5])
        division.append(row[6])
        zip_code.append(row[7])
        

    all = []
    for i in range(len(email)):
        tempList = []
        tempList.append(user_name[i])
        tempList.append(profile_name[i])
        tempList.append(email[i])
        tempList.append(phone_no[i])
        tempList.append(thana[i])
        tempList.append(district[i])
        tempList.append(division[i])
        tempList.append(zip_code[i])
        
        all.append(tempList)
    params = {'all':all}
    return render(request, 'adminPanel/userData.html', params)

def approval(request):
    return render(request,'adminPanel/approve.html')
def Productapproval(request,id,update_status):
    dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='ORCL')
    conn = cx_Oracle.connect(user='bikroy', password='bikroy', dsn=dsn_tns)
    c=conn.cursor()
    if update_status=='updated':
        if request.method == 'POST':
            adv_ids=request.POST.getlist('approvals')
            print(adv_ids) 
            for ad in adv_ids:
                adv_id=ad[0]
                c.execute("update ADVERTISEMENT set ADVERTISEMENT_TYPE='paid' where ADVERTISEMENT_ID=:adv",adv=ad)
                conn.commit()
    dict_result=[]
    result=[]
    if id==1:
        sql=''"select ad.ADVERTISEMENT_ID,USERNAME,CONTACT_NO,PRODUCT_NAME,price,PAYMENT_AMOUNT, PAYMENT_SYSTEM,TRANSACTION, pr.PRODUCT_ID from PRODUCT pr,ADVERTISEMENT ad,DEVICES d where pr.ADVERTISEMENT_ID=ad.ADVERTISEMENT_ID and ADVERTISEMENT_TYPE='pending' and pr.PRODUCT_ID=d.PRODUCT_ID"''
        c.execute(sql)
        result=c.fetchall()   
    elif id==2:
        sql=''"select ad.ADVERTISEMENT_ID,USERNAME,CONTACT_NO,PRODUCT_NAME,price,PAYMENT_AMOUNT, PAYMENT_SYSTEM,TRANSACTION, pr.PRODUCT_ID from PRODUCT pr,ADVERTISEMENT ad,PET p where pr.ADVERTISEMENT_ID=ad.ADVERTISEMENT_ID and ADVERTISEMENT_TYPE='pending' and pr.PRODUCT_ID=p.PRODUCT_ID"''
        c.execute(sql)
        result=c.fetchall() 
    elif id==3:
        sql=''"select ad.ADVERTISEMENT_ID,USERNAME,CONTACT_NO,PRODUCT_NAME,price,PAYMENT_AMOUNT, PAYMENT_SYSTEM,TRANSACTION, pr.PRODUCT_ID from PRODUCT pr,ADVERTISEMENT ad,book b where pr.ADVERTISEMENT_ID=ad.ADVERTISEMENT_ID and ADVERTISEMENT_TYPE='pending' and pr.PRODUCT_ID=b.PRODUCT_ID"''
        c.execute(sql)
        result=c.fetchall()
    elif id==4:
        sql=''"select ad.ADVERTISEMENT_ID,USERNAME,CONTACT_NO,PRODUCT_NAME,price,PAYMENT_AMOUNT, PAYMENT_SYSTEM,TRANSACTION, pr.PRODUCT_ID from PRODUCT pr,ADVERTISEMENT ad,course c where pr.ADVERTISEMENT_ID=ad.ADVERTISEMENT_ID and ADVERTISEMENT_TYPE='pending' and pr.PRODUCT_ID=c.PRODUCT_ID"''
        c.execute(sql)
        result=c.fetchall() 
    elif id==5:
        sql=''"select ad.ADVERTISEMENT_ID,USERNAME,CONTACT_NO,PRODUCT_NAME,price,PAYMENT_AMOUNT, PAYMENT_SYSTEM,TRANSACTION, pr.PRODUCT_ID from PRODUCT pr,ADVERTISEMENT ad,tution t where pr.ADVERTISEMENT_ID=ad.ADVERTISEMENT_ID and ADVERTISEMENT_TYPE='pending' and pr.PRODUCT_ID=t.PRODUCT_ID"''
        c.execute(sql)
        result=c.fetchall() 
    else:
        sql=''"select ad.ADVERTISEMENT_ID,USERNAME,CONTACT_NO,PRODUCT_NAME,price,PAYMENT_AMOUNT, PAYMENT_SYSTEM,TRANSACTION, pr.PRODUCT_ID from PRODUCT pr,ADVERTISEMENT ad,DEVICES d,pet p,book b, course c,tution t where pr.ADVERTISEMENT_ID=ad.ADVERTISEMENT_ID and ADVERTISEMENT_TYPE='pending' and pr.PRODUCT_ID<>d.PRODUCT_ID and pr.PRODUCT_ID<>p.PRODUCT_ID and pr.PRODUCT_ID<>b.PRODUCT_ID and pr.PRODUCT_ID<>c.PRODUCT_ID and pr.PRODUCT_ID<>t.PRODUCT_ID"''
        c.execute(sql)
        result=c.fetchall()        
    for r in result:
            ad_id=r[0]
            name=r[1]
            contact_no=r[2]
            prod_name=r[3]
            price=r[4]
            payment=r[5]
            payment_system=r[6]
            trans=r[7]
            prod_id=r[8]
            row={'advertisement_id':ad_id,'username':name,'contact_no':contact_no,'product_name':prod_name,'price':price,'payment_amount':payment,'payment_system':payment_system,'transaction':trans, 'prod_id':prod_id}
            dict_result.append(row)
    params={'products':dict_result,'id':id}
    conn.close()
    return render(request,'adminPanel/ProductApproval.html',params)
def Jobapproval(request,update_status):
    dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='ORCL')
    conn = cx_Oracle.connect(user='bikroy', password='bikroy', dsn=dsn_tns)
    c=conn.cursor()
    if update_status=='updated':
        if request.method == 'POST':
            adv_ids=request.POST.getlist('approvals') 
            for ad in adv_ids:
                adv_id=ad[0]
                c.execute("update ADVERTISEMENT set ADVERTISEMENT_TYPE='paid' where ADVERTISEMENT_ID=:adv",adv=ad)
                conn.commit()
    dict_result=[]
    result=[]
    sql="""SELECT ad.ADVERTISEMENT_ID,USERNAME,DESIGNATION,SALARY,PAYMENT_AMOUNT,PAYMENT_SYSTEM,TRANSACTION, j.JOB_ID from ADVERTISEMENT ad, job j where j.ADVERTISEMENT_ID=ad.ADVERTISEMENT_ID and ADVERTISEMENT_TYPE='pending'""" 
    c.execute(sql)
    result=c.fetchall()        
    for r in result:
            ad_id=r[0]
            name=r[1]
            desig=r[2]
            sal=r[3]
            payment=r[4]
            payment_system=r[5]
            trans=r[6]
            job_id = r[7]
            row={'advertisement_id':ad_id,'username':name,'designation':desig,'salary':sal,'payment_amount':payment,'payment_system':payment_system,'transaction':trans, 'job_id':job_id}
            dict_result.append(row)
    params={'jobs':dict_result}
    conn.close()
    return render(request,'adminPanel/JobApproval.html',params)


def statistics(request):
    dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='ORCL')
    conn = cx_Oracle.connect(user='bikroy', password='bikroy', dsn=dsn_tns)
    c=conn.cursor()

    #area wise advertisement count
    sql =   """
                select INITCAP(loc.division) as area, count(loc.division) as cnt , sum(ad.PAYMENT_AMOUNT) amt
                from ADVERTISEMENT ad, ACCOUNT ac, PROFILE pf, LOCATION loc
                where ad.USERNAME=ac.USERNAME and ac.PROFILE_NO=pf.PROFILE_NO and pf.LOCATION_ID=loc.LOCATION_ID and ad.ADVERTISEMENT_TYPE='paid'
                GROUP BY loc.DIVISION
                ORDER BY cnt desc

            """
    c.execute(sql)
    result = []
    result = c.fetchall()
    area = []
    how_many_ad = []
    how_many_money = []
    for row in result:
        area.append(row[0])
        how_many_ad.append(row[1])
        how_many_money.append(row[2])
    
    area_cnt_ad = []
    x_axis_labels = []
    y_axis_values = []
    for i in range(len(area)):
        tempList = []
        tempList.append(area[i])
        x_axis_labels.append(area[i])
        tempList.append(how_many_ad[i])
        y_axis_values.append(int(how_many_ad[i]))
        tempList.append(how_many_money[i])
        area_cnt_ad.append(tempList)
    
    
    chart_areawisecnt = get_plot(x_axis_labels, y_axis_values, 'Area Wise Ad Quantity', 'Area Names', 'How Many Ad Posted')
    x_axis_labels.clear()
    y_axis_values.clear()
    how_many_ad.clear()
    how_many_money.clear()

    #username wise advertisement count
    sql =   """
                select ad.USERNAME, count(ad.USERNAME) as cnt, sum(ad.PAYMENT_AMOUNT) amt
                from ADVERTISEMENT ad, ACCOUNT ac, PROFILE pf, LOCATION loc 
                where ad.USERNAME=ac.USERNAME and ac.PROFILE_NO=pf.PROFILE_NO and pf.LOCATION_ID=loc.LOCATION_ID and ad.ADVERTISEMENT_TYPE='paid'
                GROUP BY ad.USERNAME
                ORDER BY cnt desc
            """
    c.execute(sql)
    result = []
    result = c.fetchall()
    userName = []
    how_many_ad = []
    how_many_money = []
    for row in result:
        userName.append(row[0])
        how_many_ad.append(row[1])
        how_many_money.append(row[2])
    
    

    userName_cnt_ad = []
    for i in range(len(userName)):
        tempList = []
        tempList.append(userName[i])
        x_axis_labels.append(userName[i])
        tempList.append(how_many_ad[i])
        y_axis_values.append(int(how_many_ad[i]))
        tempList.append(how_many_money[i])
        userName_cnt_ad.append(tempList)

    chart_userwisecnt = get_plot(x_axis_labels, y_axis_values, 'User Wise Ad Quantity', 'Username', 'How Many Ad Posted')

    #total ad, total income of bikroy
    sql =   """
                select count(*), sum(PAYMENT_AMOUNT)
                from ADVERTISEMENT
                WHERE ADVERTISEMENT_TYPE='paid'
            """
    c.execute(sql)
    result = []
    result = c.fetchall()
    
    total_ad = result[0][0]
    total_income = result[0][1]


    #total pending ad
    sql =   """
                select count(*)
                from ADVERTISEMENT
                WHERE ADVERTISEMENT_TYPE<>'paid'
            """
    c.execute(sql)
    result = []
    result = c.fetchall()
    
    total_pending = result[0][0]

    params = {'area_cnt_ad':area_cnt_ad, 'userName_cnt_ad':userName_cnt_ad, 'total_ad':total_ad, 'total_income':total_income, 'chart_areawisecnt':chart_areawisecnt, 'chart_userwisecnt':chart_userwisecnt, 'total_pending':total_pending}

    
    return render(request, 'adminPanel/statistics.html', params)
    


import base64
from io import BytesIO

def get_graph():
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    graph = base64.b64encode(image_png)
    graph = graph.decode('utf-8')
    buffer.close()
    return graph

def get_plot(x, y, graph_name, x_label, y_label):
    plt.switch_backend('AGG')

    plt.figure(figsize=(8, 5))
    
    # Creating n-dimensional array with evenly spaced values
    y_pos=np.arange(len(x))

    # Input bar values
    # Define the bar styles with width, color, and legend labels
    plt.bar(y_pos + 0, y, width=0.3, color = 'y', label=graph_name)

    # Define X-axis labels
    plt.xticks(y_pos, x)

    # Defines best position of the legend in the figure
    plt.legend(loc='best')

    # Defines X and Y axis labels
    plt.ylabel(y_label)
    plt.xlabel(x_label)

    # Defines plot title
    plt.title(graph_name)
    plt.tight_layout()
    graph = get_graph()
    return graph