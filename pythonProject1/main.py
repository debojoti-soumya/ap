# Face Recognition Based Banking System with AI


import os.path
import datetime
import pickle
import random
import tkinter as tk
import cv2
import subprocess
from PIL import Image, ImageTk
import face_recognition

import util

class App:
    def __init__(self):
        self.main_window = tk.Tk()
        self.main_window.geometry("1200x520+350+100")

        self.login_button_main_window = util.get_button(self.main_window, 'Login', 'blue', self.login)
        self.login_button_main_window.place(x=750, y=300)

        self.register_new_user_button_main_window = util.get_button(self.main_window, 'Register New User', 'purple',
                                                                    self.register_new_user, fg='black')
        self.register_new_user_button_main_window.place(x=750, y=400)

        self.webcam_label = util.get_img_label(self.main_window)
        self.webcam_label.place(x=10, y=0, width=700, height=500)

        self.add_webcam(self.webcam_label)

        self.db_dir = './db'
        if not os.path.exists(self.db_dir):
            os.mkdir(self.db_dir)

        self.log_path = './log.txt'

    def add_webcam(self, label):
        if 'cap' not in self.__dict__:
            self.cap = cv2.VideoCapture(0)

        self._label = label
        self.process_webcam()

    def process_webcam(self):
        ret, frame = self.cap.read()

        self.most_recent_capture_arr = frame
        img_ = cv2.cvtColor(self.most_recent_capture_arr, cv2.COLOR_BGR2RGB)
        self.most_recent_capture_pil = Image.fromarray(img_)
        imgtk = ImageTk.PhotoImage(image=self.most_recent_capture_pil)
        self._label.imgtk = imgtk
        self._label.configure(image=imgtk)

        self._label.after(20, self.process_webcam)

    def check_balance(self):

        self.balance = util.get_text_label(self.personal_page, "Your balance is " + str(random.randint(1, 1000)) + "৳", "yellow")
        self.balance.place(x=10, y=0, width=700, height=500)

    def send_money(self):
        pass

    def log_out(self):
        self.personal_page.destroy()
    def load_personal_page(self, name):
        self.personal_page = tk.Toplevel(self.main_window)
        self.personal_page.geometry("1200x520+370+120")
        self.personal_page.configure(bg='yellow')

        self.bank_welcome = util.get_text_label(self.personal_page, "Welcome to ABC Bank, " + name, col='yellow')
        self.bank_welcome.place(x=10, y=0, width=700, height=500)

        self.check_balance_button = util.get_button(self.personal_page, 'Check Balance', 'blue', self.check_balance)
        self.check_balance_button.place(x=750, y=20)

        self.send_money_button = util.get_button(self.personal_page, 'Send Money', 'green', self.send_money)
        self.send_money_button.place(x=750, y=120)

        self.cash_out_button = util.get_button(self.personal_page, 'Cash Out', '#D96804', self.send_money)
        self.cash_out_button.place(x=750, y=220)

        self.bill_payment_button = util.get_button(self.personal_page, 'Bill Payment', '#F453F4', self.send_money)
        self.bill_payment_button.place(x=750, y=320)

        self.log_out_button = util.get_button(self.personal_page, 'Log Out', '#D90424', self.log_out)
        self.log_out_button.place(x=750, y=420)

    def login(self):
        unknown_img_path = './.tmp.jpg'

        cv2.imwrite(unknown_img_path, self.most_recent_capture_arr)

        output = str(subprocess.check_output(['face_recognition', self.db_dir, unknown_img_path]))

        name = output.split(",")[1][:-5]

        if name in ['unknown_person', 'no_persons_found']:
            util.msg_box('Ups...', 'You are not a customer of the bank. Please register new user or try again.')
        else:
            self.load_personal_page(name)
            with open(self.log_path, 'a') as f:
                f.write('{},{}\n'.format(name, datetime.datetime.now()))
                f.close()
        # os.remove(unknown_img_path)


    def register_new_user(self):
        self.register_new_user_window = tk.Toplevel(self.main_window)
        self.register_new_user_window.geometry("1200x520+370+120")

        self.accept_button_register_new_user_window = util.get_button(self.register_new_user_window, 'Accept', 'green', self.accept_register_new_user)
        self.accept_button_register_new_user_window.place(x=750, y=300)

        self.try_again_button_register_new_user_window = util.get_button(self.register_new_user_window, 'Try again', 'red', self.try_again_register_new_user)
        self.try_again_button_register_new_user_window.place(x=750, y=400)

        self.capture_label = util.get_img_label(self.register_new_user_window)
        self.capture_label.place(x=10, y=0, width=700, height=500)

        self.add_img_to_label(self.capture_label)

        self.entry_text_register_new_user = util.get_entry_text(self.register_new_user_window)
        self.entry_text_register_new_user.place(x=750, y=150)

        self.text_label_register_new_user = util.get_text_label(self.register_new_user_window, 'Please, \ninput username:')
        self.text_label_register_new_user.place(x=750, y=70)

    def try_again_register_new_user(self):
        self.register_new_user_window.destroy()

    def add_img_to_label(self, label):
        imgtk = ImageTk.PhotoImage(image=self.most_recent_capture_pil)
        label.imgtk = imgtk
        label.configure(image=imgtk)

        self.register_new_user_capture = self.most_recent_capture_arr.copy()

    def start(self):
        self.main_window.mainloop()

    def accept_register_new_user(self):
        name = self.entry_text_register_new_user.get(1.0, "end-1c")

        # embeddings = face_recognition.face_encodings(self.register_new_user_capture)[0]

        cv2.imwrite(os.path.join(self.db_dir, '{}.jpg'.format(name)), self.register_new_user_capture)
        # pickle.dump(embeddings, file)

        util.msg_box('Success!', 'User was registered successfully !')

        self.register_new_user_window.destroy()


if __name__ == "__main__":
    app = App()
    app.start()