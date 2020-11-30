import cx_Oracle #for oracle connection

from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages


# from django.contrib.auth import authenticate, login, logout
# from django.contrib.auth.models import User
# Create your views here.

params = {'loginsuccess':True,'username':'null'}

def home(request):
    return render(request, 'home/home.html', params)

def about(request):
    return render(request, 'home/about.html', params)

def contact(request):
    if request.method == 'POST':
        # syntax: variable = request.POST['name_of_HTML_<input>_tag not id']

        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        content = request.POST['content']
        print("kkp is using post rqst")
        print(name, email, phone, content)
    return render(request, 'home/contact.html', params)

def signup(request):
    if request.method == 'POST':

        # insert to oracle
        dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='ORCL')
        conn = cx_Oracle.connect(user='bikroy', password='bikroy', dsn=dsn_tns)

        # account
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['pass1']

        # profile
        # make a profile id
        first_name = request.POST['fname']
        last_name = request.POST['lname']
        gender = request.POST['gender']
        date_of_birth = request.POST['dateOfBirth']
        profile_picture = request.POST['profilePicture']
        phone_no = request.POST['phoneNo']


        # education history

        #work history
        #organization_name = request.POST['organizationName']
        #position = request.POST['organizationPosition']
        #start_work = request.POST['organizationStart']
        #end_work = request.POST['organizationEnd']
        #salary = request.POST['organizationSalary']

        #location
        userDivision = request.POST['userDivision']
        userDistrict = request.POST['userDistrict']
        userThana = request.POST['userThana']
        userZip = request.POST['userZip']

        c = conn.cursor()
        
        location_id = -1
        sql = "SELECT location_id FROM location WHERE division = '"+ userDivision +"' AND district = '" + userDistrict+"' AND thana = '" + userThana+"' AND  zip_code = " + userZip+" "
        c.execute(sql)
        for r in c:
            location_id = r[0]
        
        if location_id == -1:
            sql = "SELECT COUNT(*) FROM location"
            c.execute(sql)
            
            for r in c:
                location_id = r[0] + 1
            location_id = str(location_id)
            sql = "INSERT INTO location VALUES('" + location_id + "','" +userDivision+"','" + userDistrict+ "','" +userThana+ "'," + userZip+")"
            c.execute(sql)
            conn.commit()

        
        sql = "SELECT COUNT(*) FROM profile"
        c.execute(sql)
        for r in c:
            profile_no = r[0] + 1
        profile_no = str(profile_no)
        profile_picture = "profile_picture_url"
        sql = "INSERT INTO profile VALUES('"+profile_no+"','" +first_name+"' , '" + last_name+"' , '" + gender+"' , TO_DATE('" + date_of_birth+"', 'yyyy-mm-dd') , '" + profile_picture+"' , '" + phone_no+"' , '" + location_id +"')"
        print('profileSQL : ' + sql)
        c.execute(sql)
        conn.commit()

        sql = "INSERT INTO account VALUES('"+ username+"','"+ email+"','"+ password+"','"+ profile_no+"')"
        c.execute(sql)
        conn.commit()
       
        conn.close()

         
        # myuser = User.objects.create_user(username, email, password)
        # myuser.first_name = first_name 
        # myuser.last_name = last_name
        # myuser.save()
        messages.success(request, "Signup Completed")

        
    return render(request, 'home/home.html')

def handleLogin(request):
    if request.method == 'POST':
        loginusername = request.POST['loginusername']
        loginpassword = request.POST['loginpassword']

        print(loginusername)
        print(loginpassword)

        dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='ORCL')
        conn = cx_Oracle.connect(user='bikroy', password='bikroy', dsn=dsn_tns)

        c = conn.cursor()
        sql = "SELECT password FROM ACCOUNT WHERE username ='"+loginusername+"'"
        c.execute(sql)
        result = []
        result = c.fetchall()

        if len(result)==0:
            messages.warning(request, "Invalid Credentials, Please try again")
            return redirect('home')
        realpassword = result[0][0]

        
        
        if loginpassword == realpassword:
            request.session['username'] = loginusername
            request.session['userLogged'] = True
            print("kaj hoise maybe")
            
            messages.success(request, "Successfully Logged In")
            return redirect('home')
        else:
            messages.error(request, "Invalid Credentials, Please try again")
            return redirect('home')

        # user = authenticate(username=loginusername, password=loginpassword)

        # if user is not None:
        #     login(request, user)
        #     messages.success(request, "Successfully Logged In")
        #     return redirect('home')
        # else:
        #     messages.error(request, "Invalid Credentials, Please try again")
        #     return redirect('home')


def handleLogout(request):
    if request.session['userLogged']==True:
        del request.session['userLogged']
        del request.session['username']
        messages.success(request, "You have successfully logged out")
    return redirect("home")

    # logout(request)
    # messages.success(request, "You have successfully logged out")
    # return redirect("home")

def postAd(request):
    try:
        if request.session['userLogged'] == True:
            #print('For posting Advertisement, Login is required. Please Log In')
            return render(request, 'home/postAd.html', params)
    except:
        messages.success(request,'For posting Advertisement, Login is required. Please Log In')
        return redirect('home')

    # if request.user.is_authenticated is False:
    #     #print('For posting Advertisement, Login is required. Please Log In')
    #     messages.success(request,'For posting Advertisement, Login is required. Please Log In')
    #     return redirect('home')

    # else:
    #     return render(request, 'home/postAd.html', params)


def postProductAd(request):
    return render(request,'home/postProductAd.html')


def productAdCategory(request,id):
    if request.method == 'POST':
        if id:
            product_name = request.POST['product_name']
            product_price = request.POST['product_price']
            product_description = request.POST['product_description']
            product_contact_no = request.POST['product_contact_no']
            product_picture = request.POST['product_picture']
            payment_amount = request.POST['payment_amount']
            payment_system = request.POST['payment_system']
            transaction = request.POST['transaction']
        if id==1:
            device_category = request.POST['device_category']
            device_brand = request.POST['device_brand']
            device_model = request.POST['device_model']
            device_generation = request.POST['device_generation']
            device_features = request.POST['device_features']
            device_condition = request.POST['device_condition']
            device_authenticity = request.POST['device_authenticity']
        if id==2:
            pet_type = request.POST['pet_type']
            pet_color = request.POST['pet_color']
            pet_age = request.POST['pet_age']
            pet_gender = request.POST['pet_gender']
            pet_food_habit = request.POST['pet_food_habit']
        if id==3:
            book_writer = request.POST['book_writer']
            book_genre = request.POST['book_genre']
            book_condition = request.POST['book_condition']
        if id==4:
            course_title = request.POST['course_title']
            course_organization = request.POST['course_organization']
        if id==5:
            tuition_subject = request.POST['tuition_subject']
            time_duration = request.POST['time_duration']
            tutor_gender = request.POST['tutor_gender']
            tutor_education_level = request.POST['tutor_education_level']

        print("---Printing Received Data---")
        print(product_name, product_price,product_description,product_contact_no)
        #print(device_category,device_brand,device_model,device_generation,device_features,device_condition,device_authenticity)
        #print(pet_type,pet_color,pet_age,pet_gender,pet_food_habit)
        #print(book_writer,book_genre,book_condition)
        #print(course_title,course_organization)
        #print(tuition_subject,time_duration,tutor_gender,tutor_education_level)
        print("------Printing Ended-------")

        messages.success(request, 'Your advertisement has been received')

        dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='ORCL')
        conn = cx_Oracle.connect(user='bikroy', password='bikroy', dsn=dsn_tns)

        advertisement_id = -1
        sql = "SELECT COUNT(*) FROM advertisement"
        c = conn.cursor()
        c.execute(sql)

        for r in c:
            advertisement_id = r[0] + 1
        print('ad id ', advertisement_id, type(advertisement_id))
        advertisement_id = str(advertisement_id)

        advertisement_type = 'pending'
        sql = "INSERT INTO advertisement VALUES('"+advertisement_id+"','"+ advertisement_type+"','"+ payment_amount+"','"+ payment_system+"', SYSDATE ,'"+ request.session['username']+"','"+transaction+"')"

        c.execute(sql)
        conn.commit()

        product_id = -1
        sql = "SELECT COUNT(*) FROM product"
        c = conn.cursor()
        c.execute(sql)

        for r in c:
            product_id = r[0] + 1
        print('product_id ', product_id, type(product_id))
        product_id = str(product_id)


        sql = "INSERT INTO product VALUES('"+product_id+"','"+ product_name+"','"+ product_price+"','"+ product_description+"','"+ product_contact_no+"','"+ advertisement_id+"')"
        print('product_sql ', sql)
        c.execute(sql)
        conn.commit()

        if id == 1:
            sql = "INSERT INTO devices VALUES('"+product_id+"','"+ device_category+"','"+ device_brand+"','"+ device_model+"','"+ device_generation+"','"+ device_features+"','"+ device_condition+"','"+ device_authenticity+"')"
            print('product_sql ', sql)
            c.execute(sql)
            conn.commit()
        
        if id == 2:
            sql = "INSERT INTO pet VALUES('"+product_id+"','"+ pet_type+"','"+ pet_color+"','"+ pet_age+"','"+ pet_gender+"','"+ pet_food_habit+"')"
            print('product_sql ', sql)
            c.execute(sql)
            conn.commit()
        
        if id ==3:
            sql = "INSERT INTO book VALUES('"+product_id+"','"+ book_writer+"','"+ book_genre+"','"+ book_condition+"')"
            print('product_sql ', sql)
            c.execute(sql)
            conn.commit()

        if id == 4:
            sql = "INSERT INTO course VALUES('"+product_id+"','"+ course_title+"','"+ course_organization+"')"
            print('product_sql ', sql)
            c.execute(sql)
            conn.commit()
        
        if id == 5:
            sql = "INSERT INTO tution VALUES('"+product_id+"','"+ tuition_subject+"','"+ time_duration+"','"+ tutor_gender+"','"+ tutor_education_level+"')"
            print('product_sql ', sql)
            c.execute(sql)
            conn.commit()
        

    return render(request, 'home/productAdCategory.html',{'id':id})




def postJobAd(request):
    if request.method == 'POST':
        organization_id = request.POST['organization_id']
        organization_name = request.POST['organization_name']
        job_type = request.POST['job_type']
        designation = request.POST['designation']
        approx_salary = request.POST['approx_salary']
        business_function = request.POST['business_function']
        minimum_qualification = request.POST['minimum_qualification']
        gender_preference = request.POST['gender_preference']
        required_experience = request.POST['required_experience']
        skill_summary = request.POST['skill_summary']
        description = request.POST['description']
        payment_amount = request.POST['payment_amount']
        payment_system = request.POST['payment_system']
        transaction = request.POST['transaction']
        description = organization_id + '\n' + organization_name + '\n' + description


        dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='ORCL')
        conn = cx_Oracle.connect(user='bikroy', password='bikroy', dsn=dsn_tns)

        advertisement_id = -1
        sql = "SELECT COUNT(*) FROM advertisement"
        c = conn.cursor()
        c.execute(sql)

        for r in c:
            advertisement_id = r[0] + 1
        print('ad id ', advertisement_id, type(advertisement_id))
        advertisement_id = str(advertisement_id)

        advertisement_type = 'pending'
        sql = "INSERT INTO advertisement VALUES('"+advertisement_id+"','"+ advertisement_type+"',"+ payment_amount+",'"+ payment_system+"', SYSDATE ,'"+ request.session['username']+"','"+transaction+"')"

        c.execute(sql)
        conn.commit()


        job_id = -1
        sql = "SELECT COUNT(*) FROM job"
        c = conn.cursor()
        c.execute(sql)

        for r in c:
            job_id = r[0] + 1
        print('job id ', job_id, type(job_id))
        job_id = str(job_id)


        sql = "INSERT INTO job VALUES('"+job_id+"','"+ job_type+"','"+ approx_salary+"','"+ designation+"','"+ business_function+"','"+ description+"','"+ required_experience+"','"+ gender_preference +"','"+ minimum_qualification+"','"+ skill_summary+"','" + advertisement_id+"')"
        print('job_sql ', sql)
        c.execute(sql)
        conn.commit()

        conn.close()

        messages.success(request, 'Your Ad request has been recieved')
        return redirect('postJobAd')

    return render(request,'home/postJobAd.html')



# def productAdCategoryById(id, request):





#for testing Oracle working or not
def list_jobs(request):
    dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='ORCL')
    conn = cx_Oracle.connect(user='hr', password='hr', dsn=dsn_tns)
    c = conn.cursor()
    print('Success')

    c.execute("select * from HR.countries")
    out = ''
    print(c)
    for row in c:
        out += str(row) + '\n'
    conn.close()
    return HttpResponse(out, content_type="text/plain")


def approval(request):
    return render(request,'home/approve.html')
def Productapproval(request,id,update_status):
    dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='ORCL')
    conn = cx_Oracle.connect(user='bikroy', password='bikroy', dsn=dsn_tns)
    c=conn.cursor()
    if update_status=='updated':
       if request.method == 'POST':
           adv_ids=request.POST.getlist('approvals') 
       for ad in adv_ids:
           adv_id=ad[0]
           c.execute("update ADVERTISEMENT set ADVERTISEMENT_TYPE='paid' where ADVERTISEMENT_ID=:adv",adv=adv_id)
           conn.commit()
    dict_result=[]
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
    return render(request,'home/ProductApproval.html',params)
def Jobapproval(request,update_status):
    dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='ORCL')
    conn = cx_Oracle.connect(user='bikroy', password='bikroy', dsn=dsn_tns)
    c=conn.cursor()
    if update_status=='updated':
       if request.method == 'POST':
           adv_ids=request.POST.getlist('approvals') 
       for ad in adv_ids:
           adv_id=ad[0]
           c.execute("update ADVERTISEMENT set ADVERTISEMENT_TYPE='paid' where ADVERTISEMENT_ID=:adv",adv=adv_id)
           conn.commit()
    dict_result=[]
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
    return render(request,'home/JobApproval.html',params)

def profile(request):
    username=request.session['username']
    dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='ORCL')
    conn = cx_Oracle.connect(user='bikroy', password='bikroy', dsn=dsn_tns)
    c=conn.cursor()
    dict_result=[]
    result=[]
    username=request.session['username']
    #sql='"select first_name,GENDER,date_of_birth,PHONE_NO,PROFILE_PICTURE,last_name from PROFILE p,ACCOUNT ac,LOCATION l where ac.PROFILE_NO=p.PROFILE_NO and p.LOCATION_ID=l.LOCATION_ID and USERNAME="'+username+'""'
    
    #test
    sql="""
    select first_name||' '||last_name,GENDER,date_of_birth,PHONE_NO,PROFILE_PICTURE 
    from PROFILE p,ACCOUNT ac,LOCATION l 
    where ac.PROFILE_NO=p.PROFILE_NO and p.LOCATION_ID=l.LOCATION_ID and USERNAME=:user1
    """
    #test
    
    c.execute(sql, {'user1':username})
    result=c.fetchall()
    for r in result:
        fname=r[0]
        gender=r[1]
        dob=r[2]
        phn=r[3]
        pro_pic=r[4]
    sql="""select DIVISION,DISTRICT,THANA from PROFILE p,ACCOUNT ac,LOCATION l where ac.PROFILE_NO=p.PROFILE_NO and p.LOCATION_ID=l.LOCATION_ID and USERNAME=:u
    """
    c.execute(sql,{'u':username})
    result=c.fetchall()
    for r in result:
        div=r[0]
        dist=r[1]
        thana=r[2]
    sql="""select INSTITUTION_NAME,INSTITUTION_TYPE,FACULTY,START_DATE,END_DATE,i.institution_id from INSTITUTION i, PROFILE p,EDUCATION_HISTORY edu,ACCOUNT ac where ac.PROFILE_NO=p.PROFILE_NO and edu.INSTITUTION_ID=i.INSTITUTION_ID and edu.PROFILE_NO=p.PROFILE_NO and END_DATE is not null and username=:u
    """
    c.execute(sql,{'u':username})
    result=c.fetchall()
    for r in result:
        inst=r[0]
        inst_typ=r[1]
        fac=r[2]
        strt=r[3]
        end=r[4]
        inst_id=r[5]
        row={'institution_id':inst_id,'institution_name':inst,'institution_type':inst_typ,'faculty':fac,'start_date':strt,'end_date':end}
        dict_result.append(row)
    sql="""select INSTITUTION_NAME,INSTITUTION_TYPE,FACULTY,START_DATE,i.institution_id from INSTITUTION i, PROFILE p,EDUCATION_HISTORY edu,ACCOUNT ac where ac.PROFILE_NO=p.PROFILE_NO and edu.INSTITUTION_ID=i.INSTITUTION_ID and edu.PROFILE_NO=p.PROFILE_NO and END_DATE is null and username=:u
    """
    c.execute(sql,{'u':username})
    result=c.fetchall()
    cinst=''
    cinst_typ=''
    cfac=''
    cstrt=''
    cinst_id=''
    for r in result:
        cinst=r[0]
        cinst_typ=r[1]
        cfac=r[2]
        cstrt=r[3]
        cinst_id=r[4]
    past_works=[]
    sql="""select ORGANIZATION_NAME,ORGANIZATION_TYPE,POSITION,START_DATE,END_DATE,o.organization_id from ORGANIZATION o, PROFILE p,WORK_HISTORY work,ACCOUNT ac where ac.PROFILE_NO=p.PROFILE_NO and work.ORGANIZATION_ID=o.ORGANIZATION_ID and work.PROFILE_NO=p.PROFILE_NO and END_DATE is not null and username=:u
    """
    c.execute(sql,{'u':username})
    result=c.fetchall()
    for r in result:
        org=r[0]
        org_typ=r[1]
        pos=r[2]
        wstrt=r[3]
        wend=r[4]
        org_id=r[5]
        row={'organization_id':org_id,'organization_name':org,'organization_type':org_typ,'position':pos,'wstart_date':wstrt,'wend_date':wend}
        past_works.append(row)
    sql="""select ORGANIZATION_NAME,ORGANIZATION_TYPE,POSITION,START_DATE,o.organization_id from ORGANIZATION o, PROFILE p,WORK_HISTORY work,ACCOUNT ac where ac.PROFILE_NO=p.PROFILE_NO and work.ORGANIZATION_ID=o.ORGANIZATION_ID and work.PROFILE_NO=p.PROFILE_NO and END_DATE is null and username=:u
    
    """
    c.execute(sql,{'u':username})
    result=c.fetchall()
    corg=''
    corg_typ=''
    cpos=''
    cwstrt=''
    corg_id=''
    for r in result:
        corg=r[0]
        corg_typ=r[1]
        cpos=r[2]
        cwstrt=r[3]
        corg_id=r[4]
    params={'full_name':fname,'phone_no':phn,'gender':gender,'date_of_birth':dob,'division':div,'district':dist,'thana':thana,'past_edus':dict_result,'curr_inst_name':cinst,'curr_inst_id':cinst_id,'curr_inst_type':cinst_typ,'curr_faculty':cfac,'curr_start_date':cstrt,'past_works':past_works,'curr_org_name':corg,'curr_org_id':corg_id,'curr_org_type':corg_typ,'curr_position':cpos,'curr_wstart_date':cwstrt}
    conn.close()
    return render(request, 'home/profile.html', params)

def addEdu(request):
    if request.method=='POST':
        institution_id = request.POST['Institution_id']
        institution_type = request.POST['InstitutionType']
        institution_name = request.POST['institutionName']
        faculty = request.POST['faculty']
        start_study =str(request.POST['institutionStart'])
        end_study = str(request.POST['institutionEnd'])
        institution_result = request.POST['institutionResult']
        UserName=request.session['username']

        #printdata run kor toh
        #print(type(start_study), end_study)
        #printdata

        dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='ORCL')
        conn = cx_Oracle.connect(user='bikroy', password='bikroy', dsn=dsn_tns)
        c=conn.cursor()
        sql="""select INSTITUTION_id from INSTITUTION where INSTITUTION_id=:instid
        """
        c.execute(sql,{'instid':institution_id})
        result=c.fetchall()
        if len(result)==0:
            sql="""INSERT into INSTITUTION values(:instid,:name,:typ,getloc(:u))
            """
            c.execute(sql,{'instid':institution_id,'name':institution_name,'typ':institution_type,'u':UserName})
        sql="""insert into  EDUCATION_HISTORY values(getProfile(:u),:inst,:fac,to_date(:strt,'yyyy-mm-dd'),to_date(:endedu,'yyyy-mm-dd'),:res)
        """
        c.execute(sql,{'inst':institution_id,'fac':faculty,'strt':str(start_study),'endedu':str(end_study),'res':institution_result,'u':UserName})
        conn.commit()
        conn.close()
        #mark
    # profile(request)
    return redirect("profile")

def addWork(request):
    if request.method=='POST':
        organization_id = request.POST['Organization_id']
        organization_type = request.POST['organizationType']
        organization_name = request.POST['organizationName']
        position = request.POST['organizationPosition']
        start_work = request.POST['organizationStart']
        end_work = request.POST['organizationEnd']
        salary = request.POST['organizationSalary']
        UserName=request.session['username']
        #printdata run kor toh
        #print(type(start_study), end_study)
        #printdata

        dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='ORCL')
        conn = cx_Oracle.connect(user='bikroy', password='bikroy', dsn=dsn_tns)
        c=conn.cursor()
        sql="""select organization_id from organization where organization_id=:orgid
        """
        c.execute(sql,{'orgid':organization_id})
        result=c.fetchall()
        if len(result)==0:
            sql="""INSERT into organization values(:orgid,:name,:typ,getloc(:u))
            """
            c.execute(sql,{'orgid':organization_id,'name':organization_name,'typ':organization_type,'u':UserName})
        sql="""insert into  Work_HISTORY values(getProfile(:u),:org,:pos,to_date(:strt,'yyyy-mm-dd'),to_date(:end,'yyyy-mm-dd'),:sal)
        """
        c.execute(sql,{'org':organization_id,'pos':position,'strt':str(start_work),'end':str(end_work),'sal':salary,'u':UserName})
        conn.commit()
        conn.close()
        #mark
    # profile(request)
    return redirect("profile")
       
