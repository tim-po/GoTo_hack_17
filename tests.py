for i in range(4):
    # button_g = 'button' + str(i)
    if custom_butons.get('user_button_name' + str(i)) is not None:
        button_g = types.KeyboardButton(str(custom_butons.get('user_button_name' + str(i))[0]))
    else:
        button_g = types.KeyboardButton(str(custom_butons.get('user_button_name' + str(i))))
    markup.add(button_g)
bot.send_message(message.chat.id, 'спец меню',
                 reply_markup=markup)