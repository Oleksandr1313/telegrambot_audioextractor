import telebot
from pytube import YouTube
import moviepy.editor
import os

bot = telebot.TeleBot("6122023294:AAEKrwa7GR9c6yu46lj-h5KMckWGgg7KCt0")

def download(url):
    video = YouTube(url)
    title = video.title
    video = video.streams.get_highest_resolution()
    try:
        video.download(r"C:\Main_Folder\desktop\projs\telegram_bot\vids")
        return title
    except:
        print("Failed to download")

def extract_audio(url):
    name = download(url)
    folder_path = r"C:\Main_Folder\desktop\projs\telegram_bot\vids"
    video_path = os.path.join(folder_path, f"{name}.mp4")

    video = moviepy.editor.VideoFileClip(video_path)
    audio = video.audio
    audio_path = os.path.join(folder_path, f"{name}.mp3")
    audio.write_audiofile(audio_path)

@bot.message_handler(commands=["start", "hello"])
def welcome(message):
    bot.reply_to(message, "Hey, how are you doing?")
    bot.send_message(message.chat.id, "Provide me with a URL")

@bot.message_handler(func=lambda message: True)
def send_audio(message):
    url = message.text
    video = YouTube(url)
    title = video.title
    bot.send_message(message.chat.id, f"Video title: {title}")
    extract_audio(url)

    folder_path = r"C:\Main_Folder\desktop\projs\telegram_bot\vids"
    audio_file_path = os.path.join(folder_path, f"{title}.mp3")

    try:
        with open(audio_file_path, 'rb') as audio_file:
            bot.send_audio(message.chat.id, audio_file)
            print("Audio sent successfully.")
    except Exception as e:
        print("Error:", e)

bot.polling()
