from aiogram.types import InlineKeyboardMarkup,InlineKeyboardButton,ReplyKeyboardMarkup,KeyboardButton
from request_funcs.requests import get_represent_dates
from aiogram.types.web_app_info import WebAppInfo
reply_start = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text= 'Вчитель')],
    [KeyboardButton(text = 'Учень')]

],resize_keyboard=True,input_field_placeholder='Виберіть пункт',one_time_keyboard=True)




reply_student = ReplyKeyboardMarkup(keyboard = [
    [KeyboardButton(text= 'Оцінки')],
    [KeyboardButton(text= 'Розклад')],
    [KeyboardButton(text= 'Вийти з акаунту')]
],resize_keyboard=True,input_field_placeholder='Виберіть пункт')

reply_teacher = ReplyKeyboardMarkup(keyboard = [
    
    [KeyboardButton(text = 'Розклад')],
    [KeyboardButton(text= 'Вийти з акаунту')]
],resize_keyboard=True,input_field_placeholder='Виберіть пункт')



add_mark_inline = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text= 'ВИБРАТИ УЧНЯ',callback_data='choose_student')],
    [InlineKeyboardButton(text= 'ОЦІНКИ',callback_data='choose_mark')],
    [InlineKeyboardButton(text = 'ПРИЧИНА',callback_data='choose_reason')]

])
keyboard_unuse = [i for i in range(1,13)]

for i in keyboard_unuse:
    if i % 2 == 0:
        keyboard_unuse.remove(keyboard_unuse[keyboard_unuse.index(i)-1])
        keyboard_unuse[keyboard_unuse.index(i)] = [i-1,i]

for i in keyboard_unuse:
    i[0] = KeyboardButton(text=str(i[0]))
    i[1] = KeyboardButton(text=str(i[1]))


counter = 0
marks_reply = ReplyKeyboardMarkup(keyboard=keyboard_unuse,resize_keyboard=True)


def keyboard_students(students:list) -> ReplyKeyboardMarkup:
    if int(str(len(students)/2).split('.')[1]) ==0:
        for i in students:
            if (students.index(i) +1) % 2 ==0:
                
                students[students.index(i)] = [students[students.index(i)-1],i]
        for i in students:
            if type(i) != list:
                students.remove(i)
                
                
        for i in students:
            i[0] = KeyboardButton(text=i[0])
            i[1] = KeyboardButton(text=i[1])

        


        return  ReplyKeyboardMarkup(keyboard=students,resize_keyboard=True,one_time_keyboard=True)
    else:
        less = []
        for i in students:
            if (students.index(i) +1) % 2 ==0:
                less.append(students[students.index(i)-1])
                students[students.index(i)] = [students[students.index(i)-1],i]
            
        for i in students:
            for l in less:
                if i == l:
                    students.remove(l)

        for i in students:
            if type(i) != list:
                students[students.index(i)] = [i]
                
                
        for i in students:
            if len(i)>1:
                i[0] = KeyboardButton(text=i[0])
                i[1] = KeyboardButton(text=i[1])
            else:
                students[students.index(i)] = [KeyboardButton(text=i[0])]

        


        return ReplyKeyboardMarkup(keyboard = students,one_time_keyboard=True,resize_keyboard=True)


def return_to_orig_keyboard(message,check_device):
    if check_device(message)[1] == 1:
        return reply_teacher
    if check_device(message)[1] == 0:
        return reply_student


def keyboard_subjects(subjects:str) -> ReplyKeyboardMarkup:
    subjects_list = []
    try:
        if len(subjects.split(',')) > 1:
            for i in subjects.split(','):
                subjects_list.append([i])
                
        else:
            
            subjects_list.append([subjects])

        
        for i in subjects_list:
            subjects_list[subjects_list.index(i)] = [KeyboardButton(text=i[0])]
        
        
       

        return ReplyKeyboardMarkup(keyboard = subjects_list,one_time_keyboard=True)
    except:
        pass



def reply_subjects_student(all_subjects:list[str]):
    subj = []
    for subject in all_subjects:
        
        if all_subjects.index(subject) % (len(all_subjects) / (len(all_subjects) /2)) == 0:
            if all_subjects.index(subject)+1 < len(all_subjects):
                subj.append([all_subjects[all_subjects.index(subject)],all_subjects[all_subjects.index(subject)+1]])
            else: subj.append([all_subjects[all_subjects.index(subject)]])
    
    for i in subj:
        if len(i) >1:
            i[0] = KeyboardButton(text = i[0])
            i[1] = KeyboardButton(text = i[1])
        else:
            i[0] = KeyboardButton(text = i[0])

    
    return ReplyKeyboardMarkup(keyboard=subj,one_time_keyboard=True)


def reply_dates_keyboard() -> ReplyKeyboardMarkup:
    dates = get_represent_dates()
    ready = []
    for i in dates:
        if dates.index(i) % 5 == 0:
            ready.append(dates[dates.index(i): dates.index(i) + 5])

    for i in ready:
        for o in i:
            i[i.index(o)] = KeyboardButton(text = str(o))
    

        

    return ReplyKeyboardMarkup(keyboard = ready,one_time_keyboard=True)


    

def test_web(route:str) -> ReplyKeyboardMarkup:
    test_web = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='hello',web_app=WebAppInfo(url = route))]])

    return test_web