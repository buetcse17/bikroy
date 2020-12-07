import cx_Oracle #for oracle connection

from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
import os

# from django.contrib.auth import authenticate, login, logout
# from django.contrib.auth.models import User
# Create your views here.

# params = {'loginsuccess':True,'username':'null'}

def home(request):
    dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='ORCL')
    conn = cx_Oracle.connect(user='bikroy', password='bikroy', dsn=dsn_tns)

    c = conn.cursor()

    sql = """   SELECT pd.PRODUCT_ID, pd.PRODUCT_NAME, pd.PRICE, loc.DISTRICT, im.image_url
                FROM PRODUCT pd, ADVERTISEMENT ad, LOCATION loc, ACCOUNT ac, PROFILE pf, image im
                WHERE ad.ADVERTISEMENT_ID = pd.ADVERTISEMENT_ID AND ad.USERNAME=ac.USERNAME AND pf.PROFILE_NO=ac.PROFILE_NO AND pf.LOCATION_ID=loc.LOCATION_ID AND im.PRODUCT_ID=pd.PRODUCT_ID
                AND LOWER(ad.ADVERTISEMENT_TYPE)='paid'
                ORDER BY AD_TIME DESC
            """
    c.execute(sql)
    result = []
    result = c.fetchall()

    prod_id_list = []
    prod_name_list = []
    prod_price_list = []
    prod_loc_list = []
    prod_image_list = []

    for row in result:
        prod_id_list.append(row[0])
        prod_name_list.append(row[1])
        prod_price_list.append(row[2])
        prod_loc_list.append(row[3])
        prod_image_list.append(row[4])
    # print(prod_id_list)
    # print(prod_name_list)
    # print(prod_price_list)
    # print(prod_loc_list)
    # print(prod_image_list)

    prod_type_list = []
    for i in prod_id_list:
        sql1 = """SELECT PRODUCT_ID FROM DEVICES WHERE PRODUCT_ID = :p"""
        sql2 = """SELECT PRODUCT_ID FROM PET WHERE PRODUCT_ID = :p"""
        sql3 = """SELECT PRODUCT_ID FROM BOOK WHERE PRODUCT_ID = :p"""
        sql4 = """SELECT PRODUCT_ID FROM COURSE WHERE PRODUCT_ID = :p"""
        sql5 = """SELECT PRODUCT_ID FROM TUTION WHERE PRODUCT_ID = :p"""
        #sql6

        c.execute(sql1, {'p':i})
        result = []
        result = c.fetchall()
        if len(result) != 0:
            prod_type_list.append(1)
            continue

        c.execute(sql2, {'p':i})
        result = []
        result = c.fetchall()
        if len(result) != 0:
            prod_type_list.append(2)
            continue

        c.execute(sql3, {'p':i})
        result = []
        result = c.fetchall()
        if len(result) != 0:
            prod_type_list.append(3)
            continue

        c.execute(sql4, {'p':i})
        result = []
        result = c.fetchall()
        if len(result) != 0:
            prod_type_list.append(4)
            continue

        c.execute(sql5, {'p':i})
        result = []
        result = c.fetchall()
        if len(result) != 0:
            prod_type_list.append(5)
            continue

    length_of_list = len(prod_id_list)

    all = []
    for i in range(length_of_list):
        tempList = []
        tempList.append(prod_id_list[i])
        tempList.append(prod_name_list[i])
        tempList.append(prod_price_list[i])
        tempList.append(prod_loc_list[i])
        tempList.append(prod_type_list[i])
        tempList.append(prod_image_list[i])
        all.append(tempList)
    # print(all)
    params = {'length_of_list':range(length_of_list), 'all':all}
    return render(request, 'home/home.html', params)

def about(request):
    return render(request, 'home/about.html')

def contact(request):
    if request.method == 'POST':
        # syntax: variable = request.POST['name_of_HTML_<input>_tag not id']

        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        content = request.POST['content']
        print("kkp is using post rqst")
        print(name, email, phone, content)
    return render(request, 'home/contact.html')

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
            sql = """SELECT LOCATION_SEQUENCE.nextval FROM DUAL"""
            c.execute(sql)
            result = []
            result = c.fetchall()

            location_id = result[0][0]
            print('location id seq = ', location_id)
            sql = """INSERT INTO location VALUES(:location_id, :userDivision, :userDistrict, :userThana, :userZip)"""
            c.execute(sql, {'location_id':location_id, 'userDivision':userDivision, 'userDistrict':userDistrict, 'userThana':userThana, 'userZip':userZip})
            conn.commit()

        sql = """SELECT PROFILE_SEQUENCE.nextval FROM DUAL"""
        c.execute(sql)
        result = []
        result = c.fetchall()

        profile_no = str(result[0][0])        
        print('profile no seq = ', profile_no)
        profile_picture = "profile_picture_url"
        sql = """INSERT INTO profile VALUES(:profile_no, :first_name, :last_name, :gender, TO_DATE(:date_of_birth, 'yyyy-mm-dd') , :profile_picture, :phone_no, :location_id)"""
        print('profileSQL : ' + sql)
        c.execute(sql, {'profile_no':profile_no, 'first_name':first_name, 'last_name':last_name, 'gender':gender, 'date_of_birth':date_of_birth, 'profile_picture':profile_picture, 'phone_no':phone_no, 'location_id':location_id})
        conn.commit()

        sql = """INSERT INTO account VALUES(:username, :email, :password, :profile_no)"""
        c.execute(sql, {'username': username, 'email': email, 'password': password, 'profile_no': profile_no})
        conn.commit()
       
        conn.close()
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

        
        sql="""select ora_hash(:p) from dual
        """
        c.execute(sql,{'p':str(loginpassword)})
        result=[]
        result=c.fetchall()
        loginpassword=result[0][0]
        print(loginpassword)
        print(realpassword)
        if str(loginpassword) == str(realpassword):
            request.session['username'] = loginusername
            request.session['userLogged'] = True
            print("kaj hoise maybe")
            
            messages.success(request, "Successfully Logged In")
            return redirect('home')
        else:
            messages.error(request, "Invalid Credentials, Please try again")
            return redirect('home')


def handleLogout(request):
    if request.session['userLogged']==True:
        del request.session['userLogged']
        del request.session['username']
        messages.success(request, "You have successfully logged out")
    return redirect("home")


def postAd(request):
    try:
        if request.session['userLogged'] == True:
            #print('For posting Advertisement, Login is required. Please Log In')
            return redirect("myAds")
    except:
        messages.success(request,'For posting Advertisement, Login is required. Please Log In')
        return redirect('home')


def postProductAd(request):
    return render(request,'home/postProductAd.html')


def productAdCategory(request,id):
    if request.method == 'POST':
        if id:
            product_name = request.POST['product_name']
            product_price = request.POST['product_price']
            product_description = request.POST['product_description']
            product_contact_no = request.POST['product_contact_no']

            try:
                product_picture = request.FILES['product_picture']
            except:
                #messages.warning(request, 'Product Image did not upload')
                pass
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


        c = conn.cursor()
        sql = """SELECT AD_SEQUENCE.nextval FROM DUAL"""
        c.execute(sql)
        result = []
        result = c.fetchall()

        advertisement_id = str(result[0][0])

        advertisement_type = 'pending'
        sql = "INSERT INTO advertisement VALUES('"+advertisement_id+"','"+ advertisement_type+"','"+ payment_amount+"','"+ payment_system+"', SYSDATE ,'"+ request.session['username']+"','"+transaction+"')"

        c.execute(sql)
        conn.commit()

        
        sql = """SELECT PRODUCT_SEQUENCE.nextval FROM DUAL"""
        c.execute(sql)
        result = []
        result = c.fetchall()

        product_id = str(result[0][0])

        sql = "INSERT INTO product VALUES('"+product_id+"','"+ product_name+"','"+ product_price+"','"+ product_description+"','"+ product_contact_no+"','"+ advertisement_id+"')"
        print('product_sql ', sql)
        c.execute(sql)
        conn.commit()

        #delete if product image previously exists
        nam = 'static/productImage/'+str(product_id)+'.jpg'
        if os.path.isfile(nam):
            os.remove(nam)
        
        #add if product image doesn't exist
        folder = 'static/productImage'
        try:
            extenstion = product_picture.name
            extenstion = extenstion.split('.')
            extenstion = extenstion[1]
            filename = str(product_id) + '.' + 'jpg'
            fs = FileSystemStorage(location=folder)
            filesaved = fs.save(filename, product_picture)
            file_url = fs.url(filesaved)
            my_url = folder + '/' + filename
            print('file_url is :', file_url)
            print('my_url is :', my_url)
            sql = """INSERT INTO IMAGE VALUES(IMAGE_SEQUENCE.nextval, :image_url, :product_id)"""
            c.execute(sql, {'image_url':my_url, 'product_id':product_id})
            conn.commit()
        except:
            my_url = folder + '/' + 'noImageAvailable.jpg'
            sql = """INSERT INTO IMAGE VALUES(IMAGE_SEQUENCE.nextval, :image_url, :product_id)"""
            c.execute(sql, {'image_url':my_url, 'product_id':product_id})
            conn.commit()
            messages.warning(request, 'You submitted without any product image')
            pass


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
        description = organization_id + ' - ' + organization_name + ' - ' + description


        dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='ORCL')
        conn = cx_Oracle.connect(user='bikroy', password='bikroy', dsn=dsn_tns)

        c = conn.cursor()
        sql = """SELECT AD_SEQUENCE.nextval FROM DUAL"""
        c.execute(sql)
        result = []
        result = c.fetchall()

        advertisement_id = str(result[0][0])

        advertisement_type = 'pending'
        sql = "INSERT INTO advertisement VALUES('"+advertisement_id+"','"+ advertisement_type+"',"+ payment_amount+",'"+ payment_system+"', SYSDATE ,'"+ request.session['username']+"','"+transaction+"')"

        c.execute(sql)
        conn.commit()

        sql = """SELECT JOB_SEQUENCE.nextval FROM DUAL"""
        c.execute(sql)
        result = []
        result = c.fetchall()

        job_id = str(result[0][0])


        sql = "INSERT INTO job VALUES('"+job_id+"','"+ job_type+"','"+ approx_salary+"','"+ designation+"','"+ business_function+"','"+ description+"','"+ required_experience+"','"+ gender_preference +"','"+ minimum_qualification+"','"+ skill_summary+"','" + advertisement_id+"')"
        print('job_sql ', sql)
        c.execute(sql)
        conn.commit()

        conn.close()

        messages.success(request, 'Your Ad request has been recieved')
        return redirect('postJobAd')

    return render(request,'home/postJobAd.html')



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
    select first_name,GENDER,date_of_birth,PHONE_NO,PROFILE_PICTURE,email,last_name 
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
        eml=r[5]
        lname=r[6]
    sql="""select DIVISION,DISTRICT,THANA,zip_code from PROFILE p,ACCOUNT ac,LOCATION l where ac.PROFILE_NO=p.PROFILE_NO and p.LOCATION_ID=l.LOCATION_ID and USERNAME=:u
    """
    c.execute(sql,{'u':username})
    result=c.fetchall()
    for r in result:
        div=r[0]
        dist=r[1]
        thana=r[2]
        zip=r[3]
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
    print(past_works)
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
    params={'first_name':fname,'last_name':lname,'phone_no':phn,'email':eml,'gender':gender,'date_of_birth':dob,'division':div,'district':dist,'thana':thana,'zipCode':zip,'past_edus':dict_result,'curr_inst_name':cinst,'curr_inst_id':cinst_id,'curr_inst_type':cinst_typ,'curr_faculty':cfac,'curr_start_date':cstrt,'past_works':past_works,'curr_org_name':corg,'curr_org_id':corg_id,'curr_org_type':corg_typ,'curr_position':cpos,'curr_wstart_date':cwstrt}
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

def deleteEdu(request,institution_id):
    userName=request.session['username']
    dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='ORCL')
    conn = cx_Oracle.connect(user='bikroy', password='bikroy', dsn=dsn_tns)
    c=conn.cursor()
    sql="""delete from EDUCATION_HISTORY where INSTITUTION_ID=:inst_id and PROFILE_NO=GETPROFILE(:u)
    """
    c.execute(sql,{'inst_id':institution_id,'u':userName})
    conn.commit()
    conn.close()
    return redirect("profile")

def editEdu(request,institution_id):
    userName=request.session['username']
    dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='ORCL')
    conn = cx_Oracle.connect(user='bikroy', password='bikroy', dsn=dsn_tns)
    c=conn.cursor()
    if request.method=="POST":
        faculty=request.POST['editFaculty']
        start_date=request.POST['editStartDate']
        end_date=request.POST['editEndDate']
        sql="""update EDUCATION_HISTORY set faculty=:f,START_DATE=TO_DATE(:st_date,'yyyy-mm-dd'),END_DATE=TO_DATE(:end_date, 'yyyy-mm-dd') where PROFILE_NO=GETPROFILE(:u) and INSTITUTION_ID=:inst_id
        """
        c.execute(sql,{'f':faculty,'st_date':start_date,'end_date':end_date,'u':userName,'inst_id':institution_id})
        conn.commit()
        conn.close()
    return redirect("profile")

def deleteWork(request,organization_id):
    userName=request.session['username']
    dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='ORCL')
    conn = cx_Oracle.connect(user='bikroy', password='bikroy', dsn=dsn_tns)
    c=conn.cursor()
    sql="""delete from WORK_HISTORY where organization_ID=:org_id and PROFILE_NO=GETPROFILE(:u)
    """
    c.execute(sql,{'org_id':organization_id,'u':userName})
    conn.commit()
    conn.close()
    return redirect("profile")

def editWork(request,organization_id):
    userName=request.session['username']
    dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='ORCL')
    conn = cx_Oracle.connect(user='bikroy', password='bikroy', dsn=dsn_tns)
    c=conn.cursor()
    if request.method=="POST":
        position=request.POST['editPosition']
        wstart_date=request.POST['editWorkStartDate']
        wend_date=request.POST['editWorkEndDate']
        sql="""update work_HISTORY set position=:p,START_DATE=TO_DATE(:st_date,'yyyy-mm-dd'),END_DATE=TO_DATE(:end_date, 'yyyy-mm-dd') where PROFILE_NO=GETPROFILE(:u) and organization_ID=:org_id
        """
        c.execute(sql,{'p':position,'st_date':wstart_date,'end_date':wend_date,'u':userName,'org_id':organization_id})
        conn.commit()
        conn.close()
    return redirect("profile")

def myAds(request):
    dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='ORCL')
    conn = cx_Oracle.connect(user='bikroy', password='bikroy', dsn=dsn_tns)
    userName=request.session['username']
    c = conn.cursor()

    sql = """   SELECT pd.PRODUCT_ID, pd.PRODUCT_NAME, pd.PRICE, loc.DISTRICT,pd.description, im.image_url
                FROM PRODUCT pd, ADVERTISEMENT ad, LOCATION loc, ACCOUNT ac, PROFILE pf, image im
                WHERE ad.ADVERTISEMENT_ID = pd.ADVERTISEMENT_ID AND ad.USERNAME=ac.USERNAME AND pf.PROFILE_NO=ac.PROFILE_NO AND pf.LOCATION_ID=loc.LOCATION_ID and im.product_id=pd.product_id
                AND LOWER(ad.ADVERTISEMENT_TYPE)='paid' and ad.username=:u
                ORDER BY AD_TIME DESC"""
    
    c.execute(sql,{'u':userName})
    result = []
    result = c.fetchall()

    prod_id_list = []
    prod_name_list = []
    prod_price_list = []
    prod_loc_list = []
    prod_des_list = []
    prod_image_list = []

    for row in result:
        prod_id_list.append(row[0])
        prod_name_list.append(row[1])
        prod_price_list.append(row[2])
        prod_loc_list.append(row[3])
        prod_des_list.append(row[4])

        prod_image_list.append(row[5])
    # print(prod_id_list)
    # print(prod_name_list)
    # print(prod_price_list)
    # print(prod_loc_list)
    # print(prod_image_list)

    prod_type_list = []
    for i in prod_id_list:
        sql1 = """SELECT PRODUCT_ID FROM DEVICES WHERE PRODUCT_ID = :p"""
        sql2 = """SELECT PRODUCT_ID FROM PET WHERE PRODUCT_ID = :p"""
        sql3 = """SELECT PRODUCT_ID FROM BOOK WHERE PRODUCT_ID = :p"""
        sql4 = """SELECT PRODUCT_ID FROM COURSE WHERE PRODUCT_ID = :p"""
        sql5 = """SELECT PRODUCT_ID FROM TUTION WHERE PRODUCT_ID = :p"""
        #sql6

        c.execute(sql1, {'p':i})
        result = []
        result = c.fetchall()
        if len(result) != 0:
            prod_type_list.append(1)
            continue

        c.execute(sql2, {'p':i})
        result = []
        result = c.fetchall()
        if len(result) != 0:
            prod_type_list.append(2)
            continue

        c.execute(sql3, {'p':i})
        result = []
        result = c.fetchall()
        if len(result) != 0:
            prod_type_list.append(3)
            continue

        c.execute(sql4, {'p':i})
        result = []
        result = c.fetchall()
        if len(result) != 0:
            prod_type_list.append(4)
            continue

        c.execute(sql5, {'p':i})
        result = []
        result = c.fetchall()
        if len(result) != 0:
            prod_type_list.append(5)
            continue

    length_of_list = len(prod_id_list)

    all = []
    for i in range(length_of_list):
        tempList = []
        tempList.append(prod_id_list[i])
        tempList.append(prod_name_list[i])
        tempList.append(prod_price_list[i])
        tempList.append(prod_loc_list[i])
        tempList.append(prod_type_list[i])
        tempList.append(prod_des_list[i])
        tempList.append(prod_image_list[i])
        all.append(tempList)

    sql = """   SELECT pd.PRODUCT_ID, pd.PRODUCT_NAME, pd.PRICE, loc.DISTRICT,pd.description, im.image_url
                FROM PRODUCT pd, ADVERTISEMENT ad, LOCATION loc, ACCOUNT ac, PROFILE pf, image im
                WHERE ad.ADVERTISEMENT_ID = pd.ADVERTISEMENT_ID AND ad.USERNAME=ac.USERNAME AND pf.PROFILE_NO=ac.PROFILE_NO AND pf.LOCATION_ID=loc.LOCATION_ID and im.product_id=pd.product_id
                AND LOWER(ad.ADVERTISEMENT_TYPE)='pending' and ad.username=:u
                ORDER BY AD_TIME DESC"""
        

    c.execute(sql,{'u':userName})
    resultPending = []
    resultPending = c.fetchall()

    prod_id_list_pending = []
    prod_name_list_pending = []
    prod_price_list_pending = []
    prod_loc_list_pending = []
    prod_image_list_pending = []
    prod_des_list_pending=[]

    for row in resultPending:
        prod_id_list_pending.append(row[0])
        prod_name_list_pending.append(row[1])
        prod_price_list_pending.append(row[2])
        prod_loc_list_pending.append(row[3])
        prod_des_list_pending.append(row[4])
        prod_image_list_pending.append(row[5])
    #print(prod_id_list_pending)
    #print(prod_name_list_pending)
    #print(prod_price_list_pending)
    #print(prod_loc_list_pending)

    prod_type_list_pending = []
    for i in prod_id_list_pending:
        sql1 = """SELECT PRODUCT_ID FROM DEVICES WHERE PRODUCT_ID = :p"""
        sql2 = """SELECT PRODUCT_ID FROM PET WHERE PRODUCT_ID = :p"""
        sql3 = """SELECT PRODUCT_ID FROM BOOK WHERE PRODUCT_ID = :p"""
        sql4 = """SELECT PRODUCT_ID FROM COURSE WHERE PRODUCT_ID = :p"""
        sql5 = """SELECT PRODUCT_ID FROM TUTION WHERE PRODUCT_ID = :p"""
        #sql6

        c.execute(sql1, {'p':i})
        result = []
        result = c.fetchall()
        if len(result) != 0:
            prod_type_list_pending.append(1)
            continue

        c.execute(sql2, {'p':i})
        result = []
        result = c.fetchall()
        if len(result) != 0:
            prod_type_list_pending.append(2)
            continue

        c.execute(sql3, {'p':i})
        result = []
        result = c.fetchall()
        if len(result) != 0:
            prod_type_list_pending.append(3)
            continue

        c.execute(sql4, {'p':i})
        result = []
        result = c.fetchall()
        if len(result) != 0:
            prod_type_list_pending.append(4)
            continue

        c.execute(sql5, {'p':i})
        result = []
        result = c.fetchall()
        if len(result) != 0:
            prod_type_list_pending.append(5)
            continue

    length_of_list_pending = len(prod_id_list_pending)

    all_pending = []
    for i in range(length_of_list_pending):
        tempList_pending = []
        tempList_pending.append(prod_id_list_pending[i])
        tempList_pending.append(prod_name_list_pending[i])
        tempList_pending.append(prod_price_list_pending[i])
        tempList_pending.append(prod_loc_list_pending[i])
        tempList_pending.append(prod_type_list_pending[i])
        tempList_pending.append(prod_des_list_pending[i])
        tempList_pending.append(prod_image_list_pending[i])
        all_pending.append(tempList_pending)
    
    jobs = []
    sql = "select j.job_id, JOB_TYPE,DESIGNATION,SALARY,DISTRICT from job j, ADVERTISEMENT ad, ACCOUNT ac, PROFILE pf,LOCATION l  where j.ADVERTISEMENT_ID=ad.ADVERTISEMENT_ID and ad.USERNAME=ac.USERNAME and ad.ADVERTISEMENT_TYPE='paid' and ac.PROFILE_NO= pf.PROFILE_NO and pf.LOCATION_ID=l.LOCATION_ID and ac.username=:u order by PAYMENT_AMOUNT desc"
    c.execute(sql,{'u':userName})
    result=[]
    result = c.fetchall()
    #conn.close()
    for r in result:
        job_id=r[0]
        job_type=r[1]
        designation=r[2]
        salary=r[3]
        district=r[4]
        row={'job_id':job_id,'job_type':job_type,'designation':designation,'salary':salary,'district':district}
        jobs.append(row)

    jobs_pending = []
    sql = "select j.job_id, JOB_TYPE,DESIGNATION,SALARY,DISTRICT from job j, ADVERTISEMENT ad, ACCOUNT ac, PROFILE pf,LOCATION l  where j.ADVERTISEMENT_ID=ad.ADVERTISEMENT_ID and ad.USERNAME=ac.USERNAME and ad.ADVERTISEMENT_TYPE='pending' and ac.PROFILE_NO= pf.PROFILE_NO and pf.LOCATION_ID=l.LOCATION_ID and ac.username=:u order by PAYMENT_AMOUNT desc"
    c.execute(sql,{'u':userName})
    result=[]
    result = c.fetchall()
    #conn.close()
    for r in result:
        job_id=r[0]
        job_type=r[1]
        designation=r[2]
        salary=r[3]
        district=r[4]
        row={'job_id':job_id,'job_type':job_type,'designation':designation,'salary':salary,'district':district}
        jobs_pending.append(row)
    conn.close()
    params = {'length_of_list':range(length_of_list), 'allApproved':all,'length_of_list_pending':range(length_of_list_pending), 'allPending':all_pending,'allJobsApproved':jobs,'allJobsPending':jobs_pending}
    return render(request, 'home/postAd.html',params)

def deleteAd(request,product_id):
    #userName=request.session['username']
    dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='ORCL')
    conn = cx_Oracle.connect(user='bikroy', password='bikroy', dsn=dsn_tns)
    c=conn.cursor()
    # sql="""select GETADV(PRODUCT_ID) from PRODUCT where PRODUCT_ID=:p"""
    # c.execute(sql,{'p':product_id})
    # result=[]
    # result=c.fetchall()
    # adv_id=str(result[0][0])
    sql="""SELECT PRODUCT_id from DEVICES where PRODUCT_ID=:p
    """
    c.execute(sql,{'p':product_id})
    result=[]
    result=c.fetchall()
    if len(str(result))!=0:
        sql="""delete from devices where PRODUCT_ID=:p"""
        c.execute(sql,{'p':product_id})
    sql="""SELECT PRODUCT_id  from pet where PRODUCT_ID=:p
    """
    c.execute(sql,{'p':product_id})
    result=[]
    result=c.fetchall()
    if len(str(result))!=0:
        sql="""delete from pet where PRODUCT_ID=:p"""
        c.execute(sql,{'p':product_id})
    sql="""SELECT PRODUCT_id from book where PRODUCT_ID=:p
    """
    c.execute(sql,{'p':product_id})
    result=[]
    result=c.fetchall()
    if len(str(result))!=0:
        sql="""delete from book where PRODUCT_ID=:p"""
        c.execute(sql,{'p':product_id})
    sql="""SELECT PRODUCT_id  from course where PRODUCT_ID=:p
    """
    c.execute(sql,{'p':product_id})
    result=[]
    result=c.fetchall()
    if len(str(result))!=0:
        sql="""delete from course where PRODUCT_ID=:p"""
        c.execute(sql,{'p':product_id})
    sql="""SELECT PRODUCT_id  from tution where PRODUCT_ID=:p
    """
    c.execute(sql,{'p':product_id})
    result=[]
    result=c.fetchall()
    if len(str(result))!=0:
        sql="""delete from tution where PRODUCT_ID=:p"""
        c.execute(sql,{'p':product_id})
    sql="""delete from image where product_id=:p
    """
    c.execute(sql,{'p':product_id})
    sql="""DELETE from product WHERE PRODUCT_ID=:p"""
    c.execute(sql,{'p':product_id})
    # sql="""delete from advertisement where advertisement_id=:ad
    # """
    # c.execute(sql,{'ad':adv_id})
    conn.commit()
    conn.close()
    return redirect("myAds")
def editAd(request,product_id):
    #userName=request.session['username']
    dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='ORCL')
    conn = cx_Oracle.connect(user='bikroy', password='bikroy', dsn=dsn_tns)
    c=conn.cursor()
    if request.method=="POST":
        prod_name=request.POST['editProdName']
        price=request.POST['editPrice']
        des=request.POST['editDescription']
        sql="""update product set product_name=:pn,price=:pr, description=:d where product_id=:p
        """
        c.execute(sql,{'pn':prod_name,'pr':price,'d':des,'p':product_id})
        conn.commit()
        conn.close()
    return redirect("myAds")
def editProfile(request):
    userName=request.session['username']
    dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='ORCL')
    conn = cx_Oracle.connect(user='bikroy', password='bikroy', dsn=dsn_tns)
    c=conn.cursor()
    if request.method=="POST":
        f_name=request.POST['editFirstName']
        l_name=request.POST['editLastName']
        phn=request.POST['editPhoneNo']
        dob=request.POST['editDOB']
        gender=request.POST['editGender']
        sql="""update profile set first_name=:f,last_name=:l,gender=:g,date_of_birth=to_date(:dob,'yyyy-mm-dd'),phone_no=:phn where profile_no=getProfile(:u)
        """
        c.execute(sql,{'f':f_name,'l':l_name,'g':gender,'dob':dob,'phn':phn,'u':userName})
        conn.commit()
        conn.close()
    return redirect("profile")

def changePassword(request):
    userName=request.session['username']
    dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='ORCL')
    conn = cx_Oracle.connect(user='bikroy', password='bikroy', dsn=dsn_tns)
    c=conn.cursor()
    if request.method=="POST":
        old_pass=request.POST['oldPass']
        new_pass=request.POST['newPass']
        confirm_pass=request.POST['confirmPass']
        sql = "SELECT password FROM ACCOUNT WHERE username ='"+userName+"'"
        c.execute(sql)
        result = []
        result = c.fetchall()
        real_pass = result[0][0]

        sql="""select ora_hash(:p) from dual
                """
        c.execute(sql,{'p':str(old_pass)})
        result=[]
        result=c.fetchall()
        given_pass=result[0][0]
        if str(given_pass) == str(real_pass):
            if str(new_pass)==str(confirm_pass):
                sql="""update account set password=:p where username=:u
                """
                c.execute(sql,{'p':new_pass,'u':userName})
                conn.commit()
                conn.close()
                messages.success(request, "Password changed Sucessfully")
            else:
                messages.warning(request, "You have confirmed Wrong Password")
        else:
            messages.warning(request, "You have entered wrong old password.Try again")
    return redirect('profile')

def deleteJobAd(request,job_id):
    #userName=request.session['username']
    dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='ORCL')
    conn = cx_Oracle.connect(user='bikroy', password='bikroy', dsn=dsn_tns)
    c=conn.cursor()
    
    sql="""DELETE from job WHERE job_ID=:j"""
    c.execute(sql,{'j':job_id})
    conn.commit()
    conn.close()
    return redirect("myAds")

def editLoc(request):
    userName=request.session['username']
    dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='ORCL')
    conn = cx_Oracle.connect(user='bikroy', password='bikroy', dsn=dsn_tns)
    c=conn.cursor()
    if request.method=="POST":
        div=request.POST['editDivision']
        dist=request.POST['editDistrict']
        thana=request.POST['editThana']
        zip_code=request.POST['editzipCode']
        sql="""select location_id from location where lower(division)=lower(:d) and lower(thana)=lower(:t) and lower(district)=lower(:dt) and lower(zip_code)=lower(:z)"""
        c.execute(sql,{'d':div,'dt':dist,'t':thana,'z':zip_code})
        result1=[]
        #print('location',result1)
        result1=c.fetchall()
        if len(result1)==0:
            sql = """SELECT LOCATION_SEQUENCE.nextval FROM DUAL"""
            c.execute(sql)
            result = []
            result = c.fetchall()
            location_id = result[0][0]
            sql="""insert into location values(:l,:d,:dt,:t,:z)"""
            c.execute(sql,{'d':div,'dt':dist,'t':thana,'z':zip_code,'l':location_id})
            sql="""update profile set location_id=:l where profile_no=getProfile(:u)"""
            c.execute(sql,{'l':location_id,'u':userName})
            conn.commit()
        else:
            sql="""update profile set location_id=:l where profile_no=getProfile(:u)"""
            c.execute(sql,{'l':str(result1[0][0]),'u':userName})
            conn.commit()
    conn.close()
    return redirect("profile")











       
