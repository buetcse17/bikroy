import cx_Oracle #for oracle connection

from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages


from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
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

def profile(request):
    return render(request, 'home/profile.html', params)

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
        institution_name = request.POST['institutionName']
        faculty = request.POST['faculty']
        start_study = request.POST['institutionStart']
        end_study = request.POST['institutionEnd']
        result = request.POST['institutionResult']

        #work history
        organization_name = request.POST['organizationName']
        position = request.POST['organizationPosition']
        start_work = request.POST['organizationStart']
        end_work = request.POST['organizationEnd']
        salary = request.POST['organizationSalary']

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


        myuser = User.objects.create_user(username, email, password)
        myuser.first_name = first_name 
        myuser.last_name = last_name
        myuser.save()
        messages.success(request, "Signup Completed")

        
    return render(request, 'home/home.html')

def handleLogin(request):
    if request.method == 'POST':
        loginusername = request.POST['loginusername']
        loginpassword = request.POST['loginpassword']

        print(loginusername)
        print(loginpassword)

        user = authenticate(username=loginusername, password=loginpassword)

        if user is not None:
            login(request, user)
            messages.success(request, "Successfully Logged In")
            return redirect('home')
        else:
            messages.error(request, "Invalid Credentials, Please try again")
            return redirect('home')


def handleLogout(request):
    logout(request)
    messages.success(request, "You have successfully logged out")
    return redirect("home")

def postAd(request):
    if request.user.is_authenticated is False:
        #print('For posting Advertisement, Login is required. Please Log In')
        messages.success(request,'For posting Advertisement, Login is required. Please Log In')
        return redirect('home')

    else:
        return render(request, 'home/postAd.html', params)


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

        advertisement_type = 'paid'
        payment_system = 'bkash'
        payment_amount = '300'
        sql = "INSERT INTO advertisement VALUES('"+advertisement_id+"','"+ advertisement_type+"',"+ payment_amount+",'"+ payment_system+"', SYSDATE ,'"+ request.user.username+"')"

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

        advertisement_type = 'paid'
        payment_system = 'bkash'
        payment_amount = '300'
        sql = "INSERT INTO advertisement VALUES('"+advertisement_id+"','"+ advertisement_type+"',"+ payment_amount+",'"+ payment_system+"', SYSDATE ,'"+ request.user.username+"')"

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
