
TEXTS = {
    'es': {
        'welcome': "HOLA, soy Emi la mensajera! me encargo de que todas las órdenes de batalla lleguen a todos sin retraso!",
        'no_permission': "No tienes permisos para usar este comando.",
        'language_selected': "Has seleccionado el idioma español, ¡genial!",
        'language_non_exist': "Lenguaje no reconocido, por el momento solo está disponible (en, es, ru).",
        'set_language_bad': "¡Por favor, proporcione su lenguaje correctamente! Ej: (/set_language en)",
        'reset_info': "¡Toda la información de los grupos ha sido reiniciada!",
        'order_no_cited': "¡Por favor, cita el mensaje que quieres enviar!",
        'order_incorrect': "Uso incorrecto. Usa: /order <grupos>... Respondiendo a un mensaje",
        'order_no_participants': "\n\nAún no hay participantes, ¿a qué esperas? ¡Únete al plan de batalla!",
        'i_will_participate': "¡Yo participaré!",
        'order_no_group_founded': "Grupo '{grupo}' no encontrado.",
        'group_saved': "Grupo guardado como '{nombre_grupo}'.",
        'no_group_saved': "No hay grupos guardados.",
        'actual_groups': "Grupos actuales:\n",
        'squads_info_group': "{name}: participantes: {count}, lenguaje: {lang}\n",
        'button_squad_participants': "¡Participantes en el escuadrón de {name} ahora son {count}!",
        'button_has_pressed': "¡Ya has presionado este botón antes! 🎉",
        'group_not_found': "No se encontró el grupo correspondiente.",
        'group_has_eliminated': "Grupo '{nombre_grupo}' eliminado.",
        'command_center_deployed': "El centro de comando se ha establecido con éxito en este chat (ID: {chat_id}).",
        'default': "ERROR:XXX>Lo siento, el texto solicitado no está disponible.",
        'help_message': (
            'Ayuda:\n'
            'Usa /order + <escuadrones> para publicar una orden en su respectivo grupo\n'
            'Usa /register + <nombre sencillo> + <idioma: en, es, ru> para registrar a tu squad al bot mensajero\n'
            'Usa /squads para obtener la lista de los escuadrones actualmente disponibles y cuantos están listos para luchar!\n'
            'Usa /reset para restablecer la información de votos en caso de haber algún problema\n"'
            'Usa /remove para eliminar un gremio o escuadrón de la lista!\n'
            'Usa /set_language para cambiar el idioma del bot.'
        ),
    },
    'en': {
        'welcome': "HELLO, I am the Messenger BOT! I make sure that all battle orders reach everyone without delay!",
        'no_permission': "You don't have permission to use this command.",
        'language_selected': "You have selected English, great!",
        'language_non_exist': "Unrecognized language, currently only available (en, es, ru).",
        'set_language_bad': "Please provide your language correctly! Example: (/set_language en)",
        'reset_info': "All group information has been reset!",
        'order_no_cited': "Please quote the message you want to send!",
        'order_incorrect': "Incorrect use. Use: /order <groups>... While replying to a message",
        'order_no_participants': "\n\nNo participants yet, what are you waiting for? Join the battle plan!",
        'i_will_participate': "I will participate!",
        'order_no_group_founded': "Group '{grupo}' not found.",
        'group_saved': "Group saved as '{nombre_grupo}'.",
        'no_group_saved': "No groups saved.",
        'actual_groups': "Current groups:\n",
        'squads_info_group': "{name}: participants: {count}, language: {lang}\n",
        'button_squad_participants': "Participants in the {name} squad are now {count}!",
        'button_has_pressed': "You have already pressed this button before! 🎉",
        'group_not_found': "No corresponding group was found.",
        'group_has_eliminated': "Group '{nombre_grupo}' has been deleted.",
        'command_center_deployed': "The command center has been successfully set in this chat (ID: {chat_id}).",
        'default': "ERROR:XXX>Sorry, the requested text is not available.",
        'help_message': (
            'Help:\n'
            'Use /order + <squads> to publish an order in their respective group\n'
            'Use /register + <simple name> + <language: en, es, ru> to register your squad to the messenger bot\n'
            'Use /squads to get the list of currently available squads and how many are ready to fight!\n'
            'Use /reset to reset voting information in case of any problem\n'
            'Use /remove to remove a guild or squad from the list!\n'
            'Use /set_language to change the bot\'s language.'
        ),
    },
    'ru': {
        'welcome': "ПРИВЕТ, я BOT-посланник! Я забочусь о том, чтобы все боевые приказы доходили до всех без задержек!",
        'no_permission': "У вас нет прав на использование этой команды.",
        'language_selected': "Вы выбрали русский язык, отлично!",
        'language_non_exist': "Язык не распознан, в настоящее время доступен только (en, es, ru).",
        'set_language_bad': "Пожалуйста, укажите ваш язык правильно! Пример: (/set_language en)",
        'reset_info': "Вся информация о группах была сброшена!",
        'order_no_cited': "Пожалуйста, цитируйте сообщение, которое хотите отправить!",
        'order_incorrect': "Неправильное использование. Используйте: /order <группы>... Отвечая на сообщение",
        'order_no_participants': "\n\nПока нет участников, чего вы ждете? Присоединяйтесь к боевому плану!",
        'i_will_participate': "Я буду участвовать!",
        'order_no_group_founded': "Группа '{grupo}' не найдена.",
        'group_saved': "Группа сохранена как '{nombre_grupo}'.",
        'no_group_saved': "Группы не сохранены.",
        'actual_groups': "Текущие группы:\n",
        'squads_info_group': "{name}: участники: {count}, язык: {lang}\n",
        'button_squad_participants': "Участники в отряде {name} теперь составляют {count}!",
        'button_has_pressed': "Вы уже нажали эту кнопку ранее! 🎉",
        'group_not_found': "Соответствующая группа не найдена.",
        'group_has_eliminated': "Группа '{nombre_grupo}' удалена.",
        'command_center_deployed': "Центр управления успешно установлен в этом чате (ID: {chat_id}).",
        'default': "ОШИБКА:XXX>Извините, запрашиваемый текст недоступен.",
        'help_message': (
            'Помощь:\n'
            'Используйте /order + <отряды>, чтобы опубликовать приказ в соответствующей группе\n'
            'Используйте /register + <простое имя> + <язык: en, es, ru>, чтобы зарегистрировать свой отряд в посланнике\n'
            'Используйте /squads, чтобы получить список доступных отрядов и узнать, сколько готовы к бою!\n'
            'Используйте /reset, чтобы сбросить информацию о голосовании в случае проблемы\n'
            'Используйте /remove, чтобы удалить гильдию или отряд из списка!\n'
            'Используйте /set_language, чтобы изменить язык бота.'
        ),
    }
}

# Diccionario de idiomas soportados
SUPPORTED_LANGUAGES = ['en', 'es', 'ru']

