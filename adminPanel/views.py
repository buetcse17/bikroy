from django.shortcuts import render, HttpResponse, redirect

import cx_Oracle


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
        sql=''"select ad.ADVERTISEMENT_ID,USERNAME,CONTACT_NO,PRODUCT_NAME,price,PAYMENT_AMOUNT, PAYMENT_SYSTEM,TRANSACTION from PRODUCT pr,ADVERTISEMENT ad,DEVICES d where pr.ADVERTISEMENT_ID=ad.ADVERTISEMENT_ID and ADVERTISEMENT_TYPE='pending' and pr.PRODUCT_ID=d.PRODUCT_ID"''
        c.execute(sql)
        result=c.fetchall()   
    elif id==2:
        sql=''"select ad.ADVERTISEMENT_ID,USERNAME,CONTACT_NO,PRODUCT_NAME,price,PAYMENT_AMOUNT, PAYMENT_SYSTEM,TRANSACTION from PRODUCT pr,ADVERTISEMENT ad,PET p where pr.ADVERTISEMENT_ID=ad.ADVERTISEMENT_ID and ADVERTISEMENT_TYPE='pending' and pr.PRODUCT_ID=p.PRODUCT_ID"''
        c.execute(sql)
        result=c.fetchall() 
    elif id==3:
        sql=''"select ad.ADVERTISEMENT_ID,USERNAME,CONTACT_NO,PRODUCT_NAME,price,PAYMENT_AMOUNT, PAYMENT_SYSTEM,TRANSACTION from PRODUCT pr,ADVERTISEMENT ad,book b where pr.ADVERTISEMENT_ID=ad.ADVERTISEMENT_ID and ADVERTISEMENT_TYPE='pending' and pr.PRODUCT_ID=b.PRODUCT_ID"''
        c.execute(sql)
        result=c.fetchall()
    elif id==4:
        sql=''"select ad.ADVERTISEMENT_ID,USERNAME,CONTACT_NO,PRODUCT_NAME,price,PAYMENT_AMOUNT, PAYMENT_SYSTEM,TRANSACTION from PRODUCT pr,ADVERTISEMENT ad,course c where pr.ADVERTISEMENT_ID=ad.ADVERTISEMENT_ID and ADVERTISEMENT_TYPE='pending' and pr.PRODUCT_ID=c.PRODUCT_ID"''
        c.execute(sql)
        result=c.fetchall() 
    elif id==5:
        sql=''"select ad.ADVERTISEMENT_ID,USERNAME,CONTACT_NO,PRODUCT_NAME,price,PAYMENT_AMOUNT, PAYMENT_SYSTEM,TRANSACTION from PRODUCT pr,ADVERTISEMENT ad,tution t where pr.ADVERTISEMENT_ID=ad.ADVERTISEMENT_ID and ADVERTISEMENT_TYPE='pending' and pr.PRODUCT_ID=t.PRODUCT_ID"''
        c.execute(sql)
        result=c.fetchall() 
    else:
        sql=''"select ad.ADVERTISEMENT_ID,USERNAME,CONTACT_NO,PRODUCT_NAME,price,PAYMENT_AMOUNT, PAYMENT_SYSTEM,TRANSACTION from PRODUCT pr,ADVERTISEMENT ad,DEVICES d,pet p,book b, course c,tution t where pr.ADVERTISEMENT_ID=ad.ADVERTISEMENT_ID and ADVERTISEMENT_TYPE='pending' and pr.PRODUCT_ID<>d.PRODUCT_ID and pr.PRODUCT_ID<>p.PRODUCT_ID and pr.PRODUCT_ID<>b.PRODUCT_ID and pr.PRODUCT_ID<>c.PRODUCT_ID and pr.PRODUCT_ID<>t.PRODUCT_ID"''
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
            row={'advertisement_id':ad_id,'username':name,'contact_no':contact_no,'product_name':prod_name,'price':price,'payment_amount':payment,'payment_system':payment_system,'transaction':trans}
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
    sql="""SELECT ad.ADVERTISEMENT_ID,USERNAME,DESIGNATION,SALARY,PAYMENT_AMOUNT,PAYMENT_SYSTEM,TRANSACTION from ADVERTISEMENT ad, job j where j.ADVERTISEMENT_ID=ad.ADVERTISEMENT_ID and ADVERTISEMENT_TYPE='pending'""" 
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
            row={'advertisement_id':ad_id,'username':name,'designation':desig,'salary':sal,'payment_amount':payment,'payment_system':payment_system,'transaction':trans}
            dict_result.append(row)
    params={'jobs':dict_result}
    conn.close()
    return render(request,'adminPanel/JobApproval.html',params)

