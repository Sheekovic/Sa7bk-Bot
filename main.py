import telebot
import sqlite3

# Initialize your Telegram bot with the API token
bot = telebot.TeleBot('6479595687:AAEg8IFVeKKaJza1NvE1hxmiVnUkn2nhOdw')

# Function to create the conversations table if it doesn't exist
def create_conversations_table():
    conn = sqlite3.connect('chatbot.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS conversations (
            user_id INTEGER PRIMARY KEY,
            user_message TEXT,
            bot_response TEXT
        )
    ''')
    
    conn.commit()
    conn.close()

# Call the function to create the table
create_conversations_table()

# Define a function to store conversation data in the database
def store_conversation(user_id, user_message, bot_response):
    conn = sqlite3.connect('chatbot.db')
    cursor = conn.cursor()
    
    cursor.execute('INSERT INTO conversations (user_id, user_message, bot_response) VALUES (?, ?, ?)',
                   (user_id, user_message, bot_response))
    
    conn.commit()
    conn.close()

# Define a function to retrieve bot responses from the database
def get_bot_response(user_id, user_message):
    conn = sqlite3.connect('chatbot.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT bot_response FROM conversations WHERE user_id = ? AND user_message = ?',
                   (user_id, user_message))
    
    response = cursor.fetchone()
    
    conn.close()
    
    return response[0] if response else None

# Define a function to handle incoming messages
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_id = message.chat.id
    user_message = message.text
    
    # Check if we have a response in the database
    bot_response = get_bot_response(user_id, user_message)
    
    if bot_response:
        bot.send_message(user_id, bot_response)
    else:
        bot.send_message(user_id, "I'm not sure how to respond to that.")
        store_conversation(user_id, user_message, "I'm not sure how to respond to that.")

# Define a function to handle user feedback
@bot.message_handler(func=lambda message: message.text.lower() == "how do you respond?")
def handle_feedback(message):
    user_id = message.chat.id
    bot.send_message(user_id, "I learn from your responses. Just type a message, and I'll try to respond!")

# Start the bot
bot.polling()
