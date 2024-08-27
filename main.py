import csv
from datetime import datetime
from deep_translator import GoogleTranslator
import pytz
import re
from telegram import Update, InputFile, InlineKeyboardButton, InlineKeyboardMarkup, Bot, BotCommand
from telegram.ext import ApplicationBuilder,CallbackContext, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler, CallbackContext
from openpyxl import Workbook, load_workbook
import os
from texts import TEXTS

#############################--GLOBAL-VARS--#############################################

GRUPOS = {}

COMMAND_CENTER_ID = None
COMMAND_CENTER_ID_FILE = 'command_center.csv'

##############################--SECURITY--################################################

async def is_admin(update, context) -> bool:
    user_id = update.effective_user.id
    chat_id = update.effective_chat.id

    # Verificar si el usuario es un administrador en el grupo
    chat_member = await context.bot.get_chat_member(chat_id, user_id)
    if chat_member.status in ['administrator', 'creator']:
        return True
    return False
    

#############################--FUNCIONES--################################################

def get_text(update: Update, key):
    """Obtiene el texto en el idioma preferido del usuario o detecta el idioma automáticamente."""
    lang = ""
    ids = 0.0
    chat_id = update.effective_chat.id
    names = ""
    for name, datos in GRUPOS.items():
        if datos['chat_id'] == chat_id:
            names = name
            lang = GRUPOS[name]['lang']
            return TEXTS[lang].get(key, TEXTS[lang]['default'])
    
    lang = detect_language(update.effective_user.language_code)
    return TEXTS[lang].get(key, TEXTS[lang]['default'].format(error=key))

def guardar_datos_csv():
    with open('grupos_data.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        # Escribir encabezados
        writer.writerow(['Grupo', 'Chat ID', 'lang'])
        
        # Escribir datos de cada grupo
        for nombre, datos in GRUPOS.items():
            writer.writerow([nombre, datos['chat_id'], datos['lang']])

def cargar_datos_csv() -> None:
    try:
        with open('grupos_data.csv', mode='r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            if reader is None: return
            next(reader)  # Saltar el encabezado
            for row in reader:
                nombre, chat_id, lang = row
                GRUPOS[nombre] = {
                    'chat_id': int(chat_id),
                    'count': 0,
                    'lang': lang,
                    'users': []
                }
    except Exception as e:
        print(f"Ocurrió un error al leer el archivo CSV: {e}")
    global COMMAND_CENTER_ID
    try:
        with open(COMMAND_CENTER_ID_FILE, mode='r', encoding='utf-8') as file:
            COMMAND_CENTER_ID = int(file.read().strip())
    except FileNotFoundError:
        print("Archivo de centro de comando no encontrado, se creará uno nuevo al usar /set_command_center.")
    except Exception as e:
        print(f"Ocurrió un error al leer el archivo: {e}")

################################--LANGUAGE--##############################################

async def set_language(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None: # Comando para establecer el idioma
    if not await is_admin(update, context) or COMMAND_CENTER_ID != update.effective_chat.id:
        await update.message.reply_text(get_text(update, 'no_permission'))
        return []
    
    chat_id = update.effective_chat.id
    name = ""
    for nombre, datos in GRUPOS.items():
        if datos['chat_id'] == chat_id:
            name = nombre
            break
    
    if context.args:
        txt = ' '.join(context.args).strip()
        if txt == 'en':
            GRUPOS[name]['lang'] = 'en'
            await update.message.reply_text(get_text(update, 'language_selected'))
            guardar_datos_csv()
        elif txt == 'es':
            GRUPOS[name]['lang'] = 'es'
            await update.message.reply_text(get_text(update, 'language_selected'))
            guardar_datos_csv()
        elif txt == 'ru':
            GRUPOS[name]['lang'] = 'ru'
            await update.message.reply_text(get_text(update, 'language_selected'))
            guardar_datos_csv() 
        else:
            await update.message.reply_text(get_text(update, 'language_non_exist'))
            #lenguaje no reconocido
    else:
        await update.message.reply_text(get_text(update, 'set_language_bad'))
        
def detect_language(language_code):
    """Detecta el idioma del usuario basado en el código de idioma proporcionado por Telegram."""
    if language_code is None:
        return 'en'
    elif language_code.startswith('es'):
        return 'es'
    elif language_code.startswith('ru'):
        return 'ru'
    else:
        return 'en'

################################--BOT--###################################################

async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text(get_text(update, 'welcome'))

async def help(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text(get_text(update, 'help_message'))

# Función para reiniciar la información de todos los grupos
async def reset(update: Update, context: CallbackContext) -> None:
    if not await is_admin(update, context) or COMMAND_CENTER_ID != update.effective_chat.id:
        await update.message.reply_text(get_text(update, 'no_permission'))
        return []
    for nombre, datos in GRUPOS.items():
        datos['count'] = 0
        datos['users'] = []
    await update.message.reply_text(get_text(update, 'reset_info'))

async def order(update: Update, context: CallbackContext) -> None:
    if not await is_admin(update, context) or COMMAND_CENTER_ID != update.effective_chat.id:
        await update.message.reply_text(get_text(update, 'no_permission').format(error="sin permiso"))
        return []
    bot: Bot = context.bot

    # Verificar que el mensaje esté citado
    if not update.message.reply_to_message:
        await update.message.reply_text(get_text(update, 'order_no_cited'))
        return

    # Obtener el mensaje citado
    mensaje = update.message.reply_to_message.text

    # Obtener el texto del comando
    texto_comando = update.message.text.strip()
    
    # Separar el comando del mensaje
    partes = texto_comando.split(' ', 1)
    
    if len(partes) < 2:
        await update.message.reply_text(get_text(update, 'order_incorrect'))
        return

    # Obtener los nombres de los grupos
    grupos = partes[1].split(',')
    
    if grupos[0] == 'ALL':
        for nombre, datos in GRUPOS.items():
            chat_id = datos['chat_id']
            text = GoogleTranslator(source='auto', target= str(GRUPOS[nombre]['lang'])).translate(mensaje)
            text += get_text(update, 'order_no_participants')
            keyboard = [[InlineKeyboardButton(get_text(update, 'i_will_participate'), callback_data=str(chat_id))]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            GRUPOS[nombre]['count'] = 0
            GRUPOS[nombre]['users'] = []
            await bot.send_message(chat_id=chat_id, text=text, reply_markup=reply_markup)
    else:
        for grupo in grupos:
            if grupo in GRUPOS:
                # Enviar mensaje al grupo especificado
                chat_id = GRUPOS[grupo]['chat_id']
                text = GoogleTranslator(source='auto', target= str(GRUPOS[grupo]['lang'])).translate(mensaje)
                text += get_text(update, 'order_no_participants')
                keyboard = [[InlineKeyboardButton(get_text(update, 'i_will_participate'), callback_data=str(chat_id))]]
                reply_markup = InlineKeyboardMarkup(keyboard)
                GRUPOS[grupo]['count'] = 0
                GRUPOS[grupo]['users'] = []
                await bot.send_message(chat_id=chat_id, text=text, reply_markup=reply_markup)
            else:
                await update.message.reply_text(get_text(update,'order_no_group_founded').format(grupo=grupo))

async def register(update: Update, context: CallbackContext) -> None:
    if not await is_admin(update, context) or COMMAND_CENTER_ID != update.effective_chat.id:
        update.message.reply_text(get_text(update, 'no_permission'))
        return []
    chat_id = update.effective_chat.id
    chat_title = update.effective_chat.title or "No name"
    nombre_grupo = ''
    lang = ''
    
    # Obtener el nombre del grupo desde el comando
    if context.args:
        context = ' '.join(context.args).strip()
        parts = context.split(' ', 2)
        nombre_grupo = parts[0] if len(parts) > 0 else chat_title
        lang = parts[1] if len(parts) > 1 else 'en'
    else:
        nombre_grupo = chat_title
        lang = 'en'

    # Guardar el grupo en GRUPOS
    GRUPOS[nombre_grupo] = {
        'chat_id': chat_id,
        'count': 0,
        'lang': lang,
        'users': []
    }
    guardar_datos_csv()
    
    await update.message.reply_text(get_text(update, 'group_saved').format(nombre_grupo=nombre_grupo))
    
async def squads(update: Update, context: CallbackContext) -> None:
    if not await is_admin(update, context) or COMMAND_CENTER_ID != update.effective_chat.id:
        ses = COMMAND_CENTER_ID != update.effective_chat.id
        es_admin = await is_admin(update, context)
        await update.message.reply_text(get_text(update, 'no_permission') + str(es_admin) + " - " + str(ses))
        return []
    if not GRUPOS:
        await update.message.reply_text(get_text(update, 'no_group_saved'))
        return

    mensaje = get_text(update, 'actual_groups')
    for nombre, datos in GRUPOS.items():
        mensaje += get_text(update, 'squads_info_group').format(name=nombre,count=datos['count'],lang=datos['lang'])
    
    await update.message.reply_text(mensaje)

# Función que maneja el callback del botón
async def boton_callback(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    user_id = query.from_user.id
    chat_id = int(query.data)

    await query.answer()

    # Encontrar el grupo correspondiente al chat_id
    for nombre, datos in GRUPOS.items():
        if datos['chat_id'] == chat_id:
            # Verificar si el usuario ya presionó el botón
            if user_id not in datos['users']:
                GRUPOS[nombre]['count'] += 1
                datos['users'].append(user_id)  # Añadir el user_id al arreglo
                text = query.message.text
                lineas = text.split("\n")
                lineas[-1] = get_text(update, 'button_squad_participants').format(name=nombre,count=GRUPOS[nombre]['count'])
                text = '\n'.join(lineas)
                await query.edit_message_text( text=text,
                    reply_markup=InlineKeyboardMarkup(
                        [[InlineKeyboardButton(get_text(update, 'i_will_participate'), callback_data=str(chat_id))]]
                    )
                )
            else:
                await query.answer(text=get_text(update, 'button_has_pressed'), show_alert=True)
            break
    else:
        await query.edit_message_text( text=text,
                    reply_markup=InlineKeyboardMarkup(
                        [[InlineKeyboardButton(get_text(update, 'group_not_found'), callback_data=str(chat_id))]]
                    ))

async def remove(update: Update, context: CallbackContext) -> None:
    if not await is_admin(update, context):
        await update.message.reply_text(get_text(update, 'no_permission'))
        return []
    nombre_grupo = ' '.join(context.args).strip()
    if nombre_grupo in GRUPOS:
        del GRUPOS[nombre_grupo]
        await update.message.reply_text(get_text(update, 'group_has_eliminated').format(nombre_grupo=nombre_grupo))
        guardar_datos_csv()
    else:
        await update.message.reply_text(get_text(update, 'group_not_found'))

async def set_command_center(update: Update, context: CallbackContext) -> None:
    if update.effective_user.id == 858368230:
        global COMMAND_CENTER_ID
        chat_id = update.effective_chat.id
        COMMAND_CENTER_ID = chat_id
        with open(COMMAND_CENTER_ID_FILE, mode='w', newline='', encoding='utf-8') as file:
            file.write(str(COMMAND_CENTER_ID))
        await update.message.reply_text(get_text(update, 'command_center_deployed').format(chat_id=COMMAND_CENTER_ID))
    else:
        await update.message.reply_text(get_text(update, 'no_permission'))


#############################--MAIN--####################################################

cargar_datos_csv()

test_bot = "7523544789:AAE6u1waeC3kL3LpZK_7-J_CNqNTdPbybG4"
messenger_bot = "7464240046:AAE_ZaNDZJvh-A-Y_wq3c6FnHwk_cB8zdc4"
app = ApplicationBuilder().token(messenger_bot).build()

app.add_handler(CommandHandler("set_command_center", set_command_center))
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("help", help))
app.add_handler(CommandHandler("order", order))
app.add_handler(CommandHandler("register", register))
app.add_handler(CommandHandler("squads", squads))
app.add_handler(CommandHandler("reset", reset))
app.add_handler(CommandHandler("remove", remove))
app.add_handler(CommandHandler("set_language", set_language))
app.add_handler(CallbackQueryHandler(boton_callback))

app.run_polling()
