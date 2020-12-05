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
