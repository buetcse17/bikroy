from django.shortcuts import render
import cx_Oracle

# Create your views here.
def list(request):
    dict_result = []
    dsn_tns  = cx_Oracle.makedsn('localhost','1521',service_name='ORCL')
    conn = cx_Oracle.connect(user='bikroy',password='bikroy',dsn=dsn_tns)
    cursor = conn.cursor()
    sql = "select j.job_id, JOB_TYPE,DESIGNATION,SALARY,DISTRICT from job j, ADVERTISEMENT ad, ACCOUNT ac, PROFILE pf,LOCATION l  where j.ADVERTISEMENT_ID=ad.ADVERTISEMENT_ID and ad.USERNAME=ac.USERNAME and ac.PROFILE_NO= pf.PROFILE_NO and ad.ADVERTISEMENT_TYPE='paid' and pf.LOCATION_ID=l.LOCATION_ID order by PAYMENT_AMOUNT desc"
    cursor.execute(sql)
    result = cursor.fetchall()
    conn.close()
    for r in result:
        job_id=r[0]
        job_type=r[1]
        designation=r[2]
        salary=r[3]
        district=r[4]
        row={'job_id':job_id,'job_type':job_type,'designation':designation,'salary':salary,'district':district}
        dict_result.append(row)
    return render(request,'job/listJob.html',{'jobs':dict_result})

def listJobAreaWise(request, area):
    dict_result = []
    dsn_tns  = cx_Oracle.makedsn('localhost','1521',service_name='ORCL')
    conn = cx_Oracle.connect(user='bikroy',password='bikroy',dsn=dsn_tns)
    cursor = conn.cursor()
    sql = """   select j.job_id, JOB_TYPE,DESIGNATION,SALARY,DISTRICT 
                from job j, ADVERTISEMENT ad, ACCOUNT ac, PROFILE pf,LOCATION l  
                where j.ADVERTISEMENT_ID=ad.ADVERTISEMENT_ID and ad.USERNAME=ac.USERNAME and ac.PROFILE_NO= pf.PROFILE_NO and pf.LOCATION_ID=l.LOCATION_ID  and ad.ADVERTISEMENT_TYPE='paid'
                and LOWER(l.DIVISION)=:area
                order by ad.AD_TIME desc"""
    cursor.execute(sql, {'area':area})
    result = cursor.fetchall()
    conn.close()
    for r in result:
        job_id=r[0]
        job_type=r[1]
        designation=r[2]
        salary=r[3]
        district=r[4]
        row={'job_id':job_id,'job_type':job_type,'designation':designation,'salary':salary,'district':district}
        dict_result.append(row)
    return render(request,'job/listJob.html',{'jobs':dict_result})

def displayJob(request,job_id):
    dsn_tns  = cx_Oracle.makedsn('localhost','1521',service_name='ORCL')
    conn = cx_Oracle.connect(user='bikroy',password='bikroy',dsn=dsn_tns)
    #product_id='pr'+str(product_id)
    params={}
    dict_result=[]
    cursor = conn.cursor()
    sql = "select JOB_TYPE,DESIGNATION,SALARY,BUSINESS_FUNCTION,DESCRIPTION,REQUIRED_EXPERIENCE, GENDER_PREFERENCE,MINIMUM_QUALIFICATION,SKILLS_SUMMARY, AD_TIME,THANA,DISTRICT,DIVISION from job j, ADVERTISEMENT ad, ACCOUNT ac, PROFILE pf,LOCATION l  where j.ADVERTISEMENT_ID=ad.ADVERTISEMENT_ID and ad.USERNAME=ac.USERNAME and ac.PROFILE_NO= pf.PROFILE_NO and pf.LOCATION_ID=l.LOCATION_ID and j.job_id=:jbid"
    cursor.execute(sql,jbid=job_id)
    result = cursor.fetchall()
    for r in result:
        job_type=r[0]
        desg=r[1]
        sal=r[2]
        bus_func=r[3]
        desc=r[4]
        req_ex=r[5]
        gender_pref=r[6]
        min_qualification=r[7]
        skills=r[8]
        ad_time=r[9]
        thana=r[10]
        district=r[11]
        division=r[12]
    sql = ''"select j.job_id, JOB_TYPE,DESIGNATION,SALARY,DISTRICT from job j, ADVERTISEMENT ad, ACCOUNT ac, PROFILE pf,LOCATION l  where ( designation like '%"''+desg+''"%') and job_id<>:jb and j.ADVERTISEMENT_ID=ad.ADVERTISEMENT_ID and ad.USERNAME=ac.USERNAME and ad.ADVERTISEMENT_TYPE='paid' and ac.PROFILE_NO= pf.PROFILE_NO and pf.LOCATION_ID=l.LOCATION_ID order by PAYMENT_AMOUNT desc"''
    cursor.execute(sql,jb=job_id)
    result = cursor.fetchall()
    conn.close()
    for r in result:
        sjob_id=r[0]
        sjob_type=r[1]
        sdesignation=r[2]
        ssalary=r[3]
        sdistrict=r[4]
        row={'sjob_id':sjob_id,'sjob_type':sjob_type,'sdesignation':sdesignation,'ssalary':ssalary,'sdistrict':sdistrict}
        dict_result.append(row)
    params={'job_type':job_type,'designation':desg,'salary':sal,'business_function':bus_func,'description':desc,'required_experience':req_ex,'gender_preference':gender_pref,'minimum_qualification':min_qualification,'skills':skills,'ad_time':ad_time,'thana':thana,'district':district,'division':division,'similar':dict_result}
    return render(request,'job/displayJob.html',params)

