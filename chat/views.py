import cx_Oracle

from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages

# Create your views here.

def mychats(request):
    dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='ORCL')
    conn = cx_Oracle.connect(user='bikroy', password='bikroy', dsn=dsn_tns)
    c = conn.cursor()
    #sql = "SELECT message_content FROM chat WHERE sender_username='"+request.session['username']+"'OR receiver_username='"+request.session['username']+"' ORDER BY TIME"
    #sql = "SELECT sender_username FROM chat WHERE receiver_username='"+request.session['username']+"' UNION "+"SELECT receiver_username FROM chat WHERE sender_username='"+request.session['username']+"'"
    sql = "SELECT * FROM((SELECT sender_username, max(time) as mx FROM chat WHERE receiver_username=:myusername GROUP BY sender_username) UNION ( SELECT receiver_username, max(time) as mx FROM chat WHERE sender_username=:myusername GROUP BY receiver_username)) ORDER BY mx desc"
    print(sql)
    c.execute(sql, {'myusername':str(request.session['username'])})
    result = []
    result = c.fetchall()

    #kar kar sathe chat hoyeche from last to first
    chatWith = []
    for row in result:
        #print(row[0])
        alreadyHas = False
        for item in chatWith:
            if item == row[0]:
                alreadyHas = True
        if alreadyHas == False:
            chatWith.append(row[0])
    print(chatWith)
    result.clear()
    lastMsg = []
    for name in chatWith:
        sql =   """
                    SELECT MESSAGE_CONTENT
                    FROM CHAT
                    WHERE (SENDER_USERNAME=:other AND RECEIVER_USERNAME=:me) OR (RECEIVER_USERNAME=:other AND SENDER_USERNAME=:me)
                    ORDER BY time desc
                """
        c.execute(sql, {'me':request.session['username'], 'other':name})
        result = c.fetchall()
        #print(result[0][0])
        lastMsg.append(result[0][0])
    print(lastMsg)

    result.clear()
    lastMsgTime = []
    for name in chatWith:
        sql =   """
                    SELECT time
                    FROM CHAT
                    WHERE (SENDER_USERNAME=:other AND RECEIVER_USERNAME=:me) OR (RECEIVER_USERNAME=:other AND SENDER_USERNAME=:me)
                    ORDER BY time desc
                """
        c.execute(sql, {'me':request.session['username'], 'other':name})
        result = c.fetchall()
        #print(result[0][0])
        lastMsgTime.append(result[0][0])
    print(lastMsgTime)

    chatWith_lastMsg = []
    for i in range(len(chatWith)):
        tempList = []
        tempList.append(chatWith[i])
        tempList.append(lastMsg[i])
        tempList.append(lastMsgTime[i])
        chatWith_lastMsg.append(tempList)
        #tempList.clear()
    print(chatWith_lastMsg)

    params = {'chatWith_lastMsg':chatWith_lastMsg}
    return render(request, 'chat/mychats.html', params)


def chatbox(request, chatUser):
    dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='ORCL')
    conn = cx_Oracle.connect(user='bikroy', password='bikroy', dsn=dsn_tns)
    c = conn.cursor()

    try:
        if request.method == 'POST':
            chatMessage = request.POST['chatMessage']

            sql = """
                    INSERT INTO CHAT
                    VALUES(CHAT_SEQUENCE.nextval, :chatMessage, SYSDATE, :sender_username, :receiver_username)
                    """
            c.execute(sql, {'chatMessage':chatMessage, 'sender_username':request.session['username'], 'receiver_username':chatUser})
            conn.commit()
            messages.success(request, 'Your message has been sent')
    except:
        messages.warning(request, 'Please type a message')
    sql =   """
            SELECT SENDER_USERNAME, MESSAGE_CONTENT, time
            FROM CHAT
            WHERE (SENDER_USERNAME=:other AND RECEIVER_USERNAME=:me) OR (RECEIVER_USERNAME=:other AND SENDER_USERNAME=:me)
            ORDER BY time
            """
    c.execute(sql, {'me':request.session['username'], 'other':chatUser})
    result = []
    result = c.fetchall()

    sender_msg_time = []
    for row in result:
        print(row)
        tempList = []
        tempList.append(row[0])
        tempList.append(row[1])
        tempList.append(row[2])
        sender_msg_time.append(tempList)

    params = {'sender_msg_time':sender_msg_time, 'chatUser':chatUser}
    return render(request, 'chat/chatbox.html', params)
    

    

