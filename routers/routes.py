from aiogram import Router,F
from aiogram.filters import CommandStart,Command
from aiogram.types import Message
import emoji as emoji
import inputs.keyboards as kb
from aiogram.methods.send_photo import SendPhoto
from aiogram.types.menu_button_web_app import MenuButtonWebApp
from aiogram.fsm.state import State,StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove
from aiogram.types.web_app_info import WebAppInfo
import grequests
import requests
import ast
import json
from request_funcs.requests import *
from image_generator import Schedule
import aiogram.types as types

router = Router()
from pathlib import Path
import aiogram.filters as filters



teacher_button = MenuButtonWebApp(text = 'Журнал',web_app=WebAppInfo(url='https://13.60.35.192.traefik.me/'),type='web_app')





class Login(StatesGroup):
    who = State()
    login = State()
    password = State()



@router.message(CommandStart())
async def start(message:Message,state:FSMContext):
    
    if check_device(message) == "NO ACC":
        await message.answer(f'Вітаю! Насніть /login щоб увійти в акаунт! {emoji.emojize(":smirking_face:")}')
   

    else:
        await message.answer(f'Ви вже є у базі данних {emoji.emojize(":smirking_face:")}\n якщо хочете змінити акаунт тисніть /login',reply_markup=kb.return_to_orig_keyboard(message,check_device))
@router.message(Command('login'))
async def login(message:Message,state: FSMContext):
    await message.answer(f'Привіт, ти хто у нас?{emoji.emojize(":smirking_face:")}',reply_markup=kb.reply_start)
    await state.set_state(Login.who)



@router.message(Login.who)
async def who(message:Message,state:FSMContext):
    if message.text == 'Вчитель' or message.text == 'Учень':
        await state.update_data(who=message.text)
        await state.set_state(Login.login)
        await message.answer('Введіть логін')
    else:
        await message.answer('Немає такої ролі')
        await state.clear()

@router.message(Login.login)
async def start_route(message:Message,state:FSMContext):
    await state.update_data(login = message.text)
    await state.set_state(Login.password)
    await message.answer('Введіть пароль')

@router.message(Login.password)
async def password_route(message:Message,state:FSMContext):
    global teacher_id,student_id
    await state.update_data(password = message.text)
    data = await state.get_data()
    
    
    if data['who'] == 'Вчитель':
        
        sites = ['https://16.16.198.178.nip.io/0986525956Ee/teachers_log_pass']
        

        responses = [grequests.get(u) for u in sites]

        # wait for all results
        responses = grequests.map(responses)

        for response in responses:
           
            logs = ast.literal_eval(response.text)
            logined_teacher = False
            for i in logs:
                if i[1] == data['login'] and i[2] == data['password']:
                    logined_teacher = True
                    add_id(message,i[0],True)
                    
                    await state.clear()
                    await message.answer(f'Ви успішно увійшли в систему {emoji.emojize(":partying_face:")}',reply_markup=kb.reply_teacher)
                    await message.bot.set_chat_menu_button(message.chat.id,menu_button=teacher_button)
               

            if not logined_teacher:
                await message.answer(f'Такого акаунта не існує в базі данних.Натисніть /login щоб почати знову {emoji.emojize(":winking_face:")}')
                await state.clear()


    if data['who']=='Учень':
        sites = ['https://16.16.198.178.nip.io/0986525956Ee/students_log']
        

        responses = [grequests.get(u) for u in sites]

        # wait for all results
        responses = grequests.map(responses)

        for response in responses:
           
            logs = ast.literal_eval(response.text)
            logined_student = False
            for i in logs:
                
                if i[1] == data['login'] and i[2] == data['password']:
                    logined_student = True
                    
                    add_id(message,i[0])
                    await state.clear()
                    await message.answer(f'Ви успішно увійшли в систему {emoji.emojize(":partying_face:")}',reply_markup=kb.reply_student)
                    await message.bot.set_chat_menu_button(message.chat.id)
                

            if not logined_student:
                await message.answer(f'Не існує такого акаунта в базі данних.Натисніть /login щоб почати знову {emoji.emojize(":winking_face:")}')
                await state.clear()

class getSubjectMark(StatesGroup):
    subject = State()
    
@router.message(F.text.lower() == 'оцінки')
async def marks_route(message:Message,state:FSMContext):
    check = check_device(message)
    if check == 'NO ACC':
        await message.answer(f'Ви не увійшли в акаунт!Натисніть /login щоб увійти в акаунт')

    elif check[1] == 1:
        await message.answer(f'Не достатньо прав для цієї функції')
    elif check[1] == 0:
        subjects = get_all_subjects()

        await message.answer('Виберіть предмет',reply_markup=kb.reply_subjects_student(subjects))
        
        await state.set_state(getSubjectMark.subject)

@router.message(getSubjectMark.subject)
async def catch_student_mark_subject(message:Message,state:FSMContext):
    student_id = check_device(message)[0]
    subject = message.text
    marks = get_subject_marks(student_id,subject)
    total_marks_string = '~~~~~~~~Оцінки~~~~~~~~~~~~\n'
    
    if marks != []:
        for mark_list in marks:

            total_marks_string += mark_list[1] + ':'
            if mark_list[2] !=None:
                total_marks_string+= str(mark_list[0]) + ',' + mark_list[2] +'               ' + mark_list[3] +',' +mark_list[4]
            else:
                total_marks_string+= str(mark_list[0]) + '                ' + mark_list[3] +',' +mark_list[4]
            total_marks_string += '\n'
        total_marks_string += '~~~~~~~~Оцінки~~~~~~~~~~~~'
        await message.answer(total_marks_string,reply_markup=kb.return_to_orig_keyboard(message,check_device))
        await state.clear()
    else:
        await message.answer('Поки немає оцінок по цьому предмету',reply_markup=kb.return_to_orig_keyboard(message,check_device))
        await state.clear()
            

@router.message(F.text.lower() == 'розклад')
async def schedule_route(message:Message):
    if check_device(message) == 'NO ACC':
        await message.answer(f'Ви не увійшли в акаунт!Натисніть /login щоб увійти в акаунт')
    else:
        schedule = get_schedule()
        schedule = json.loads(schedule)
        schedule_draw = Schedule()
        for i in range(0,5):
            schedule_draw.draw_subject(i,schedule[i][1:])
        schedule_draw.save_pic()
        await message.reply_photo(photo = types.FSInputFile(path = f'{Path(__file__).parent.parent}\siga.png'))









@router.message(F.text.lower() == 'вийти з акаунту')
async def logout(message:Message):
    delete_device(str(message.chat.id))
    await message.answer('Ви вийшли з акаунту! натисніть /login щоб увійти в акаунт знову',reply_markup=ReplyKeyboardRemove())
    await message.bot.set_chat_menu_button(message.chat.id)



    



    
    
    







#                           CHANGING INLINEKEYBOARD IN THE SAME MESSAGE
# @router.callback_query(F.data == 'choose_mark')
# async def choose_mark_route(callback:types.CallbackQuery):
#     await callback.message.edit_text(text=f'{callback.message.text}',reply_markup=kb.marks_inline)



            


@router.message(Command('web',prefix=['!','/']))
async def webtest(message:Message):
    
    await message.answer('hello',reply_markup=kb.test_web('https://13.60.35.192.traefik.me'))



