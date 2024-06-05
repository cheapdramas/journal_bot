from aiogram.types import Message
import emoji as emoji
import grequests
import ast
import requests
import json




def check_device(message:Message) -> list[int,int]:
    sites = ['https://16.16.198.178.nip.io/check_device']
        

    responses = [grequests.post(u,data=json.dumps({'device':str(message.chat.id)})) for u in sites]

    responses = grequests.map(responses)

    for i in responses:
        return ast.literal_eval(i.text)



def add_id(message:Message,log_id:int,teacher:bool = False):
    if teacher:

        s = ['https://16.16.198.178.nip.io/0986525956Ee/add_device']
        a = [grequests.post(u,data=json.dumps({'device_id':str(message.chat.id),'log_id':int(log_id),'is_teacher':True})) for u in s]
        a = grequests.map(a)
        for resp in a:
            print(resp.text)
    if not teacher:
        s = ['https://16.16.198.178.nip.io/0986525956Ee/add_device']
        a = [grequests.post(u,data=json.dumps({'device_id':str(message.chat.id),'log_id':int(log_id),'is_teacher':False})) for u in s]
        a = grequests.map(a)
        for resp in a:
            print(resp.text)

def get_marks(log_id:int) -> list:
    url = f'https://16.16.198.178.nip.io/0986525956Ee/get_marks/{log_id}'

    async_req = [grequests.get(url)]

    async_req = grequests.map(async_req)

    for resp in async_req:
        
        return resp.text


def get_schedule():
    url = 'https://16.16.198.178.nip.io/0986525956Ee/schedule'

    a = requests.get(url)

    return a.text
    


def get_students(id_teacher:int):
    url = f'https://16.16.198.178.nip.io/0986525956Ee/get_teacher_students/{id_teacher}'

    a = [grequests.get(url)]
    a = grequests.map(a)

    for i in a:
        return json.loads(i.text)
    
def get_student_id_byname(name:str) -> int:
    data = {'name': name}

    url = 'https://16.16.198.178.nip.io/get_student_id_by_name_scname'

    a = [grequests.post(url,data=json.dumps(data))]

    a= grequests.map(a)

    for i in a:
        return i.text
    


def get_teacher_subjects(id_teacher:int):

    url = f'https://16.16.198.178.nip.io/0986525956Ee/get_subjects_teacher/{id_teacher}'


    a = [grequests.get(url)]
    a = grequests.map(a)

    for resp in a:
        return json.loads(resp.text)


def get_marks_date(id_student:int):
    url = [f'https://16.16.198.178.nip.io/0986525956Ee/get_mark_date/{id_student}']

    a = [grequests.get(url) for url in url]
    a = grequests.map(a)

    for response in a:
        return json.loads(response.text)
    





    
def send_mark_to_db(subject:str,student_id:int,mark:int,reason:str = ''):
    url = ['https://16.16.198.178.nip.io/add_marks_tg']
    
    
    a = [grequests.post(url,data=json.dumps({'student_id':student_id,'subject':subject,'mark':mark,'reason':reason}))for url in url]

    a = grequests.map(a)

    
def get_all_subjects():
    url = ['https://16.16.198.178.nip.io/0986525956Ee/all_subjects']

    a = [grequests.get(url) for url in url]
    a= grequests.map(a)
    for response in a:
        return json.loads(response.text)
    

def get_subject_marks(student_id:int,subject: str):

    url = ['https://16.16.198.178.nip.io/student_subject_marks?password=0986525956Ee']
    data = {'student_id':student_id,'subject':subject}
    a = [grequests.post(url,data = json.dumps(data))for url in url]

    a = grequests.map(a)

    for response in a:
        return json.loads(response.text)
    

def delete_device(device_id:str):

    url = ['https://16.16.198.178.nip.io/delete_acc?password=0986525956Ee']
    data = json.dumps({'device_id':device_id})
    request = [grequests.post(url,data = data) for url in url]
    request = grequests.map(request)

    for response in request:
        print(response.text)


def add_homework_request(info_homework:dict):
    url = ['https://16.16.198.178.nip.io/add_homework_journal']

    request = [grequests.post(url,data = json.dumps(info_homework)) for url in url]

    request = grequests.map(request)

    for response in request:
        return response.status_code


def get_represent_dates():
    url = ['https://16.16.198.178.nip.io/get_dates_represent']

    request = [grequests.get(url) for url in url]

    request = grequests.map(request)

    for response in request:
        

        return json.loads(response.text)