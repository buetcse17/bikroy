import cx_Oracle

from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages

def searchHome(request):
    dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='ORCL')
    conn = cx_Oracle.connect(user='bikroy', password='bikroy', dsn=dsn_tns)
    c = conn.cursor()
    try:
        if request.method == 'POST':
            query = request.POST['query']
            print('QUERY is ', query)
            q = query.lower()
            query = '%'+str(q)+'%'

            sqlDevice = """ SELECT d.PRODUCT_ID, p.PRODUCT_NAME, p.PRICE, loc.DISTRICT, im.image_url
                            FROM PRODUCT p, DEVICES d, ADVERTISEMENT ad, LOCATION loc, image im, ACCOUNT ac, PROFILE pf
                            WHERE ((LOWER(DEVICE_CATAGORY) LIKE :query) OR
                            (LOWER(BRAND) LIKE :query) OR
                            (LOWER(MODEL) LIKE :query) OR
                            (LOWER(FEATURES) LIKE :query) OR
                            (LOWER(PRODUCT_NAME) LIKE :query) OR
                            (LOWER(DESCRIPTION) LIKE :query))
                            AND p.ADVERTISEMENT_ID = ad.ADVERTISEMENT_ID
                            AND d.PRODUCT_ID = p.PRODUCT_ID
                            AND im.PRODUCT_ID = p.PRODUCT_ID
                            AND ad.ADVERTISEMENT_TYPE='paid'
                            AND ad.USERNAME = ac.USERNAME
                            AND ac.PROFILE_NO=pf.PROFILE_NO
                            AND pf.LOCATION_ID = loc.LOCATION_ID
                            ORDER BY AD_TIME DESC
                        """
            result = []
 
            c.execute(sqlDevice, {'query':query})
            result = c.fetchall()
            devices = []
            for row in result:
                tempList = []
                tempList.append(row[0])
                tempList.append(row[1])
                tempList.append(row[2])
                tempList.append(row[3])
                tempList.append(row[4])
                devices.append(tempList)
            print(devices)

            sqlPet =    """
                            SELECT d.PRODUCT_ID, p.PRODUCT_NAME, p.PRICE, loc.DISTRICT, im.image_url
                            FROM PRODUCT p, PET d, ADVERTISEMENT ad, LOCATION loc, image im, ACCOUNT ac, PROFILE pf
                            WHERE ((LOWER(PET_TYPE) LIKE :query) OR
                            (LOWER(p.PRODUCT_NAME) LIKE :query) OR
                            (LOWER(p.DESCRIPTION) LIKE :query))

                            AND p.ADVERTISEMENT_ID = ad.ADVERTISEMENT_ID
                            AND d.PRODUCT_ID = p.PRODUCT_ID 
                            AND im.PRODUCT_ID = p.PRODUCT_ID
                            AND ad.ADVERTISEMENT_TYPE='paid'
                            AND ad.USERNAME = ac.USERNAME
                            AND ac.PROFILE_NO=pf.PROFILE_NO
                            AND pf.LOCATION_ID= loc.LOCATION_ID
                            ORDER BY AD_TIME DESC
                        """
            result = []
            c.execute(sqlPet, {'query':query})
            result = c.fetchall()
            pet = []
            for row in result:
                tempList = []
                tempList.append(row[0])
                tempList.append(row[1])
                tempList.append(row[2])
                tempList.append(row[3])
                tempList.append(row[4])
                pet.append(tempList)
            print(pet)
            
            sqlBook =   """
                            SELECT d.PRODUCT_ID, p.PRODUCT_NAME, p.PRICE, loc.DISTRICT, im.image_url
                            FROM PRODUCT p, BOOK d, ADVERTISEMENT ad, LOCATION loc, image im, ACCOUNT ac, PROFILE pf
                            WHERE ((LOWER(WRITER) LIKE :query) OR
                            (LOWER(GENRE) LIKE :query) OR
                            (LOWER(p.PRODUCT_NAME) LIKE :query) OR
                            (LOWER(p.DESCRIPTION) LIKE :query))

                            AND p.ADVERTISEMENT_ID = ad.ADVERTISEMENT_ID
                            AND d.PRODUCT_ID = p.PRODUCT_ID 
                            AND im.PRODUCT_ID = p.PRODUCT_ID
                            AND ad.ADVERTISEMENT_TYPE='paid'
                            AND ad.USERNAME = ac.USERNAME
                            AND ac.PROFILE_NO=pf.PROFILE_NO
                            AND pf.LOCATION_ID= loc.LOCATION_ID
                            ORDER BY AD_TIME DESC
                        """
            result = []
            c.execute(sqlBook, {'query':query})
            result = c.fetchall()
            book = []
            for row in result:
                tempList = []
                tempList.append(row[0])
                tempList.append(row[1])
                tempList.append(row[2])
                tempList.append(row[3])
                tempList.append(row[4])
                book.append(tempList)
            print(book)

            sqlCourse =     """
                                SELECT d.PRODUCT_ID, p.PRODUCT_NAME, p.PRICE, loc.DISTRICT, im.image_url
                                FROM PRODUCT p, COURSE d, ADVERTISEMENT ad, LOCATION loc, image im, ACCOUNT ac, PROFILE pf
                                WHERE ((LOWER(COURSE_TITLE) LIKE :query) OR
                                (LOWER(ORGANIZATION) LIKE :query) OR
                                (LOWER(p.PRODUCT_NAME) LIKE :query) OR
                                (LOWER(p.DESCRIPTION) LIKE :query))
                                
                                AND p.ADVERTISEMENT_ID = ad.ADVERTISEMENT_ID
                                AND d.PRODUCT_ID = p.PRODUCT_ID 
                                AND im.PRODUCT_ID = p.PRODUCT_ID
                                AND ad.ADVERTISEMENT_TYPE='paid'
                                AND ad.USERNAME = ac.USERNAME
                                AND ac.PROFILE_NO=pf.PROFILE_NO
                                AND pf.LOCATION_ID= loc.LOCATION_ID
                                ORDER BY AD_TIME DESC
                            """
            result = []
            c.execute(sqlCourse, {'query':query})
            result = c.fetchall()
            course = []
            for row in result:
                tempList = []
                tempList.append(row[0])
                tempList.append(row[1])
                tempList.append(row[2])
                tempList.append(row[3])
                tempList.append(row[4])
                course.append(tempList)
            print(course)
            
            sqlTution = """
                            SELECT d.PRODUCT_ID, p.PRODUCT_NAME, p.PRICE, loc.DISTRICT, im.image_url
                            FROM PRODUCT p, TUTION d, ADVERTISEMENT ad, LOCATION loc, image im, ACCOUNT ac, PROFILE pf
                            WHERE ((LOWER(TUTION_SUBJECT) LIKE :query) OR
                            (LOWER(p.PRODUCT_NAME) LIKE :query) OR
                            (LOWER(p.DESCRIPTION) LIKE :query))
                            
                            AND p.ADVERTISEMENT_ID = ad.ADVERTISEMENT_ID
                            AND d.PRODUCT_ID = p.PRODUCT_ID 
                            AND im.PRODUCT_ID = p.PRODUCT_ID
                            AND ad.ADVERTISEMENT_TYPE='paid'
                            AND ad.USERNAME = ac.USERNAME
                            AND ac.PROFILE_NO=pf.PROFILE_NO
                            AND pf.LOCATION_ID= loc.LOCATION_ID
                            ORDER BY AD_TIME DESC
                        """
            result = []
            c.execute(sqlTution, {'query':query})
            result = c.fetchall()
            tution = []
            for row in result:
                tempList = []
                tempList.append(row[0])
                tempList.append(row[1])
                tempList.append(row[2])
                tempList.append(row[3])
                tempList.append(row[4])
                tution.append(tempList)
            print(tution)

            sqlJob ="""
                        SELECT j.JOB_ID, j.JOB_TYPE, j.DESIGNATION, j.SALARY, loc.DISTRICT
                        FROM JOB j, ADVERTISEMENT ad, LOCATION loc, ACCOUNT ac, PROFILE pf
                        WHERE ((LOWER(j.BUSINESS_FUNCTION) LIKE :query) OR
                        (LOWER(j.DESIGNATION) LIKE :query) OR
                        (LOWER(j.DESCRIPTION) LIKE :query) OR 
						(LOWER(j.SKILLS_SUMMARY) LIKE :query))

                        AND j.ADVERTISEMENT_ID = ad.ADVERTISEMENT_ID
                        AND ad.ADVERTISEMENT_TYPE='paid'
                        AND ad.USERNAME = ac.USERNAME
                        AND ac.PROFILE_NO=pf.PROFILE_NO
                        AND pf.LOCATION_ID= loc.LOCATION_ID
                        ORDER BY AD_TIME DESC
                    """
            result = []
            c.execute(sqlJob, {'query':query})
            result = c.fetchall()
            job = []
            for row in result:
                tempList = []
                tempList.append(row[0])
                tempList.append(row[1])
                tempList.append(row[2])
                tempList.append(row[3])
                tempList.append(row[4])
                job.append(tempList)
            print(job)

            totalCount = len(devices)+len(pet)+len(book)+len(course)+len(tution)+len(job)
            params = {'query':q, 'devices':devices, 'deviceCount':len(devices), 'pet':pet, 'petCount':len(pet), 'book':book, 'bookCount':len(book), 'course':course, 'courseCount':len(course), 'tution':tution, 'tutionCount':len(tution), 'job':job, 'jobCount':len(job), 'totalCount':totalCount}
            return render(request,'search/searchHome.html', params)
        else:
            return redirect('home')
    except:
        return redirect('home')


def searchItem(request, query):
    dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='ORCL')
    conn = cx_Oracle.connect(user='bikroy', password='bikroy', dsn=dsn_tns)
    c = conn.cursor()
    try:
        print('QUERY is ', query)
        q = query.lower()
        query = '%'+str(q)+'%'

        sqlDevice = """ SELECT d.PRODUCT_ID, p.PRODUCT_NAME, p.PRICE, loc.DISTRICT, im.image_url
                        FROM PRODUCT p, DEVICES d, ADVERTISEMENT ad, LOCATION loc, image im, ACCOUNT ac, PROFILE pf
                        WHERE ((LOWER(DEVICE_CATAGORY) LIKE :query) OR
                        (LOWER(BRAND) LIKE :query) OR
                        (LOWER(MODEL) LIKE :query) OR
                        (LOWER(FEATURES) LIKE :query) OR
                        (LOWER(PRODUCT_NAME) LIKE :query) OR
                        (LOWER(DESCRIPTION) LIKE :query))
                        AND p.ADVERTISEMENT_ID = ad.ADVERTISEMENT_ID
                        AND d.PRODUCT_ID = p.PRODUCT_ID
                        AND im.PRODUCT_ID = p.PRODUCT_ID
                        AND ad.ADVERTISEMENT_TYPE='paid'
                        AND ad.USERNAME = ac.USERNAME
                        AND ac.PROFILE_NO=pf.PROFILE_NO
                        AND pf.LOCATION_ID = loc.LOCATION_ID
                        ORDER BY AD_TIME DESC
                    """
        result = []

        c.execute(sqlDevice, {'query':query})
        result = c.fetchall()
        devices = []
        for row in result:
            tempList = []
            tempList.append(row[0])
            tempList.append(row[1])
            tempList.append(row[2])
            tempList.append(row[3])
            tempList.append(row[4])
            devices.append(tempList)
        print(devices)

        sqlPet =    """
                        SELECT d.PRODUCT_ID, p.PRODUCT_NAME, p.PRICE, loc.DISTRICT, im.image_url
                        FROM PRODUCT p, PET d, ADVERTISEMENT ad, LOCATION loc, image im, ACCOUNT ac, PROFILE pf
                        WHERE ((LOWER(PET_TYPE) LIKE :query) OR
                        (LOWER(p.PRODUCT_NAME) LIKE :query) OR
                        (LOWER(p.DESCRIPTION) LIKE :query))

                        AND p.ADVERTISEMENT_ID = ad.ADVERTISEMENT_ID
                        AND d.PRODUCT_ID = p.PRODUCT_ID 
                        AND im.PRODUCT_ID = p.PRODUCT_ID
                        AND ad.ADVERTISEMENT_TYPE='paid'
                        AND ad.USERNAME = ac.USERNAME
                        AND ac.PROFILE_NO=pf.PROFILE_NO
                        AND pf.LOCATION_ID= loc.LOCATION_ID
                        ORDER BY AD_TIME DESC
                    """
        result = []
        c.execute(sqlPet, {'query':query})
        result = c.fetchall()
        pet = []
        for row in result:
            tempList = []
            tempList.append(row[0])
            tempList.append(row[1])
            tempList.append(row[2])
            tempList.append(row[3])
            tempList.append(row[4])
            pet.append(tempList)
        print(pet)
        
        sqlBook =   """
                        SELECT d.PRODUCT_ID, p.PRODUCT_NAME, p.PRICE, loc.DISTRICT, im.image_url
                        FROM PRODUCT p, BOOK d, ADVERTISEMENT ad, LOCATION loc, image im, ACCOUNT ac, PROFILE pf
                        WHERE ((LOWER(WRITER) LIKE :query) OR
                        (LOWER(GENRE) LIKE :query) OR
                        (LOWER(p.PRODUCT_NAME) LIKE :query) OR
                        (LOWER(p.DESCRIPTION) LIKE :query))

                        AND p.ADVERTISEMENT_ID = ad.ADVERTISEMENT_ID
                        AND d.PRODUCT_ID = p.PRODUCT_ID 
                        AND im.PRODUCT_ID = p.PRODUCT_ID
                        AND ad.ADVERTISEMENT_TYPE='paid'
                        AND ad.USERNAME = ac.USERNAME
                        AND ac.PROFILE_NO=pf.PROFILE_NO
                        AND pf.LOCATION_ID= loc.LOCATION_ID
                        ORDER BY AD_TIME DESC
                    """
        result = []
        c.execute(sqlBook, {'query':query})
        result = c.fetchall()
        book = []
        for row in result:
            tempList = []
            tempList.append(row[0])
            tempList.append(row[1])
            tempList.append(row[2])
            tempList.append(row[3])
            tempList.append(row[4])
            book.append(tempList)
        print(book)

        sqlCourse =     """
                            SELECT d.PRODUCT_ID, p.PRODUCT_NAME, p.PRICE, loc.DISTRICT, im.image_url
                            FROM PRODUCT p, COURSE d, ADVERTISEMENT ad, LOCATION loc, image im, ACCOUNT ac, PROFILE pf
                            WHERE ((LOWER(COURSE_TITLE) LIKE :query) OR
                            (LOWER(ORGANIZATION) LIKE :query) OR
                            (LOWER(p.PRODUCT_NAME) LIKE :query) OR
                            (LOWER(p.DESCRIPTION) LIKE :query))
                            
                            AND p.ADVERTISEMENT_ID = ad.ADVERTISEMENT_ID
                            AND d.PRODUCT_ID = p.PRODUCT_ID 
                            AND im.PRODUCT_ID = p.PRODUCT_ID
                            AND ad.ADVERTISEMENT_TYPE='paid'
                            AND ad.USERNAME = ac.USERNAME
                            AND ac.PROFILE_NO=pf.PROFILE_NO
                            AND pf.LOCATION_ID= loc.LOCATION_ID
                            ORDER BY AD_TIME DESC
                        """
        result = []
        c.execute(sqlCourse, {'query':query})
        result = c.fetchall()
        course = []
        for row in result:
            tempList = []
            tempList.append(row[0])
            tempList.append(row[1])
            tempList.append(row[2])
            tempList.append(row[3])
            tempList.append(row[4])
            course.append(tempList)
        print(course)
        
        sqlTution = """
                        SELECT d.PRODUCT_ID, p.PRODUCT_NAME, p.PRICE, loc.DISTRICT, im.image_url
                        FROM PRODUCT p, TUTION d, ADVERTISEMENT ad, LOCATION loc, image im, ACCOUNT ac, PROFILE pf
                        WHERE ((LOWER(TUTION_SUBJECT) LIKE :query) OR
                        (LOWER(p.PRODUCT_NAME) LIKE :query) OR
                        (LOWER(p.DESCRIPTION) LIKE :query))
                        
                        AND p.ADVERTISEMENT_ID = ad.ADVERTISEMENT_ID
                        AND d.PRODUCT_ID = p.PRODUCT_ID 
                        AND im.PRODUCT_ID = p.PRODUCT_ID
                        AND ad.ADVERTISEMENT_TYPE='paid'
                        AND ad.USERNAME = ac.USERNAME
                        AND ac.PROFILE_NO=pf.PROFILE_NO
                        AND pf.LOCATION_ID= loc.LOCATION_ID
                        ORDER BY AD_TIME DESC
                    """
        result = []
        c.execute(sqlTution, {'query':query})
        result = c.fetchall()
        tution = []
        for row in result:
            tempList = []
            tempList.append(row[0])
            tempList.append(row[1])
            tempList.append(row[2])
            tempList.append(row[3])
            tempList.append(row[4])
            tution.append(tempList)
        print(tution)

        sqlJob ="""
                    SELECT j.JOB_ID, j.JOB_TYPE, j.DESIGNATION, j.SALARY, loc.DISTRICT
                    FROM JOB j, ADVERTISEMENT ad, LOCATION loc, ACCOUNT ac, PROFILE pf
                    WHERE ((LOWER(j.BUSINESS_FUNCTION) LIKE :query) OR
                    (LOWER(j.DESIGNATION) LIKE :query) OR
                    (LOWER(j.DESCRIPTION) LIKE :query) OR 
                    (LOWER(j.SKILLS_SUMMARY) LIKE :query))

                    AND j.ADVERTISEMENT_ID = ad.ADVERTISEMENT_ID
                    AND ad.ADVERTISEMENT_TYPE='paid'
                    AND ad.USERNAME = ac.USERNAME
                    AND ac.PROFILE_NO=pf.PROFILE_NO
                    AND pf.LOCATION_ID= loc.LOCATION_ID
                    ORDER BY AD_TIME DESC
                """
        result = []
        c.execute(sqlJob, {'query':query})
        result = c.fetchall()
        job = []
        for row in result:
            tempList = []
            tempList.append(row[0])
            tempList.append(row[1])
            tempList.append(row[2])
            tempList.append(row[3])
            tempList.append(row[4])
            job.append(tempList)
        print(job)

        totalCount = len(devices)+len(pet)+len(book)+len(course)+len(tution)+len(job)
        params = {'query':q, 'devices':devices, 'deviceCount':len(devices), 'pet':pet, 'petCount':len(pet), 'book':book, 'bookCount':len(book), 'course':course, 'courseCount':len(course), 'tution':tution, 'tutionCount':len(tution), 'job':job, 'jobCount':len(job), 'totalCount':totalCount}
        return render(request,'search/searchHome.html', params)
    except:
        return redirect('home')


def searchAreaWise(request, query, area):
    dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='ORCL')
    conn = cx_Oracle.connect(user='bikroy', password='bikroy', dsn=dsn_tns)
    c = conn.cursor()
    try:
        print('QUERY is ', query)
        q = query.lower()
        query = '%'+str(q)+'%'

        sqlDevice = """ SELECT d.PRODUCT_ID, p.PRODUCT_NAME, p.PRICE, loc.DISTRICT, im.image_url
                        FROM PRODUCT p, DEVICES d, ADVERTISEMENT ad, LOCATION loc, image im, ACCOUNT ac, PROFILE pf
                        WHERE ((LOWER(DEVICE_CATAGORY) LIKE :query) OR
                        (LOWER(BRAND) LIKE :query) OR
                        (LOWER(MODEL) LIKE :query) OR
                        (LOWER(FEATURES) LIKE :query) OR
                        (LOWER(PRODUCT_NAME) LIKE :query) OR
                        (LOWER(DESCRIPTION) LIKE :query))
                        AND p.ADVERTISEMENT_ID = ad.ADVERTISEMENT_ID
                        AND d.PRODUCT_ID = p.PRODUCT_ID
                        AND im.PRODUCT_ID = p.PRODUCT_ID
                        AND ad.ADVERTISEMENT_TYPE='paid'
                        AND ad.USERNAME = ac.USERNAME
                        AND ac.PROFILE_NO=pf.PROFILE_NO
                        AND pf.LOCATION_ID = loc.LOCATION_ID
                        AND lower(loc.DIVISION) = lower(:area)
                        ORDER BY AD_TIME DESC
                    """
        result = []

        c.execute(sqlDevice, {'query':query, 'area':area})
        result = c.fetchall()
        devices = []
        for row in result:
            tempList = []
            tempList.append(row[0])
            tempList.append(row[1])
            tempList.append(row[2])
            tempList.append(row[3])
            tempList.append(row[4])
            devices.append(tempList)
        print(devices)

        sqlPet =    """
                        SELECT d.PRODUCT_ID, p.PRODUCT_NAME, p.PRICE, loc.DISTRICT, im.image_url
                        FROM PRODUCT p, PET d, ADVERTISEMENT ad, LOCATION loc, image im, ACCOUNT ac, PROFILE pf
                        WHERE ((LOWER(PET_TYPE) LIKE :query) OR
                        (LOWER(p.PRODUCT_NAME) LIKE :query) OR
                        (LOWER(p.DESCRIPTION) LIKE :query))

                        AND p.ADVERTISEMENT_ID = ad.ADVERTISEMENT_ID
                        AND d.PRODUCT_ID = p.PRODUCT_ID 
                        AND im.PRODUCT_ID = p.PRODUCT_ID
                        AND ad.ADVERTISEMENT_TYPE='paid'
                        AND ad.USERNAME = ac.USERNAME
                        AND ac.PROFILE_NO=pf.PROFILE_NO
                        AND pf.LOCATION_ID= loc.LOCATION_ID
                        AND lower(loc.DIVISION) = lower(:area)
                        ORDER BY AD_TIME DESC
                    """
        result = []
        c.execute(sqlPet, {'query':query, 'area':area})
        result = c.fetchall()
        pet = []
        for row in result:
            tempList = []
            tempList.append(row[0])
            tempList.append(row[1])
            tempList.append(row[2])
            tempList.append(row[3])
            tempList.append(row[4])
            pet.append(tempList)
        print(pet)
        
        sqlBook =   """
                        SELECT d.PRODUCT_ID, p.PRODUCT_NAME, p.PRICE, loc.DISTRICT, im.image_url
                        FROM PRODUCT p, BOOK d, ADVERTISEMENT ad, LOCATION loc, image im, ACCOUNT ac, PROFILE pf
                        WHERE ((LOWER(WRITER) LIKE :query) OR
                        (LOWER(GENRE) LIKE :query) OR
                        (LOWER(p.PRODUCT_NAME) LIKE :query) OR
                        (LOWER(p.DESCRIPTION) LIKE :query))

                        AND p.ADVERTISEMENT_ID = ad.ADVERTISEMENT_ID
                        AND d.PRODUCT_ID = p.PRODUCT_ID 
                        AND im.PRODUCT_ID = p.PRODUCT_ID
                        AND ad.ADVERTISEMENT_TYPE='paid'
                        AND ad.USERNAME = ac.USERNAME
                        AND ac.PROFILE_NO=pf.PROFILE_NO
                        AND pf.LOCATION_ID= loc.LOCATION_ID
                        AND lower(loc.DIVISION) = lower(:area)
                        ORDER BY AD_TIME DESC
                    """
        result = []
        c.execute(sqlBook, {'query':query, 'area':area})
        result = c.fetchall()
        book = []
        for row in result:
            tempList = []
            tempList.append(row[0])
            tempList.append(row[1])
            tempList.append(row[2])
            tempList.append(row[3])
            tempList.append(row[4])
            book.append(tempList)
        print(book)

        sqlCourse =     """
                            SELECT d.PRODUCT_ID, p.PRODUCT_NAME, p.PRICE, loc.DISTRICT, im.image_url
                            FROM PRODUCT p, COURSE d, ADVERTISEMENT ad, LOCATION loc, image im, ACCOUNT ac, PROFILE pf
                            WHERE ((LOWER(COURSE_TITLE) LIKE :query) OR
                            (LOWER(ORGANIZATION) LIKE :query) OR
                            (LOWER(p.PRODUCT_NAME) LIKE :query) OR
                            (LOWER(p.DESCRIPTION) LIKE :query))
                            
                            AND p.ADVERTISEMENT_ID = ad.ADVERTISEMENT_ID
                            AND d.PRODUCT_ID = p.PRODUCT_ID 
                            AND im.PRODUCT_ID = p.PRODUCT_ID
                            AND ad.ADVERTISEMENT_TYPE='paid'
                            AND ad.USERNAME = ac.USERNAME
                            AND ac.PROFILE_NO=pf.PROFILE_NO
                            AND pf.LOCATION_ID= loc.LOCATION_ID
                            AND lower(loc.DIVISION) = lower(:area)
                            ORDER BY AD_TIME DESC
                        """
        result = []
        c.execute(sqlCourse, {'query':query, 'area':area})
        result = c.fetchall()
        course = []
        for row in result:
            tempList = []
            tempList.append(row[0])
            tempList.append(row[1])
            tempList.append(row[2])
            tempList.append(row[3])
            tempList.append(row[4])
            course.append(tempList)
        print(course)
        
        sqlTution = """
                        SELECT d.PRODUCT_ID, p.PRODUCT_NAME, p.PRICE, loc.DISTRICT, im.image_url
                        FROM PRODUCT p, TUTION d, ADVERTISEMENT ad, LOCATION loc, image im, ACCOUNT ac, PROFILE pf
                        WHERE ((LOWER(TUTION_SUBJECT) LIKE :query) OR
                        (LOWER(p.PRODUCT_NAME) LIKE :query) OR
                        (LOWER(p.DESCRIPTION) LIKE :query))
                        
                        AND p.ADVERTISEMENT_ID = ad.ADVERTISEMENT_ID
                        AND d.PRODUCT_ID = p.PRODUCT_ID 
                        AND im.PRODUCT_ID = p.PRODUCT_ID
                        AND ad.ADVERTISEMENT_TYPE='paid'
                        AND ad.USERNAME = ac.USERNAME
                        AND ac.PROFILE_NO=pf.PROFILE_NO
                        AND pf.LOCATION_ID= loc.LOCATION_ID
                        AND lower(loc.DIVISION) = lower(:area)
                        ORDER BY AD_TIME DESC
                    """
        result = []
        c.execute(sqlTution, {'query':query, 'area':area})
        result = c.fetchall()
        tution = []
        for row in result:
            tempList = []
            tempList.append(row[0])
            tempList.append(row[1])
            tempList.append(row[2])
            tempList.append(row[3])
            tempList.append(row[4])
            tution.append(tempList)
        print(tution)

        sqlJob ="""
                    SELECT j.JOB_ID, j.JOB_TYPE, j.DESIGNATION, j.SALARY, loc.DISTRICT
                    FROM JOB j, ADVERTISEMENT ad, LOCATION loc, ACCOUNT ac, PROFILE pf
                    WHERE ((LOWER(j.BUSINESS_FUNCTION) LIKE :query) OR
                    (LOWER(j.DESIGNATION) LIKE :query) OR
                    (LOWER(j.DESCRIPTION) LIKE :query) OR 
                    (LOWER(j.SKILLS_SUMMARY) LIKE :query))

                    AND j.ADVERTISEMENT_ID = ad.ADVERTISEMENT_ID
                    AND ad.ADVERTISEMENT_TYPE='paid'
                    AND ad.USERNAME = ac.USERNAME
                    AND ac.PROFILE_NO=pf.PROFILE_NO
                    AND pf.LOCATION_ID= loc.LOCATION_ID
                    AND lower(loc.DIVISION) = lower(:area)
                    ORDER BY AD_TIME DESC
                """
        result = []
        c.execute(sqlJob, {'query':query, 'area':area})
        result = c.fetchall()
        job = []
        for row in result:
            tempList = []
            tempList.append(row[0])
            tempList.append(row[1])
            tempList.append(row[2])
            tempList.append(row[3])
            tempList.append(row[4])
            job.append(tempList)
        print(job)

        totalCount = len(devices)+len(pet)+len(book)+len(course)+len(tution)+len(job)
        params = {'query':q, 'devices':devices, 'deviceCount':len(devices), 'pet':pet, 'petCount':len(pet), 'book':book, 'bookCount':len(book), 'course':course, 'courseCount':len(course), 'tution':tution, 'tutionCount':len(tution), 'job':job, 'jobCount':len(job), 'totalCount':totalCount}
        return render(request,'search/searchHome.html', params)

    except:
        return redirect('home')