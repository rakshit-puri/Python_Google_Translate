import gui
import sys
import googletrans
import speech_recognition as sr
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox, QMainWindow
import gtts
from playsound import playsound
import os


# Using Recognizer from speech recognition library
r1 = sr.Recognizer()
r1.dynamic_energy_threshold = False

# Setting minimum energy value, below it all noise will be ignored.
r1.energy_threshold = 450


# Main Class for GUI functionality
class Main(QMainWindow, gui.Ui_MainWindow):
    def __init__(self, parent=None):
        super(Main, self).__init__(parent)

        self.setupUi(self)
        self.textEdit.clear()
        self.add_languages()
        
        # Connecting functions with widgets.
        self.pushButton.clicked.connect(self.translate)
        self.pushButton_2.clicked.connect(self.clear)
        self.pushButton_3.clicked.connect(self.audio_to_text)
        self.pushButton_5.clicked.connect(self.swap)
        self.pushButton_6.clicked.connect(self.text_to_speech_input)
        self.pushButton_4.clicked.connect(self.text_to_speech_output)

    # Adding language list to Dropdown Menus 
    def add_languages(self):
        for x in googletrans.LANGUAGES.values():
            self.comboBox.addItem(x.capitalize())
            self.comboBox_2.addItem(x.capitalize())

    # Implementation of Speaker Icon for Input Text Widget.
    # It uses Google text-to-speech(gtts) Library to create the mp3 file and then plays it.
    # Old file is removed if it exists. 
    def text_to_speech_input(self):
        try:
            os.remove("x.mp3")
        except:
            pass

        try:
            text = self.textEdit.toPlainText()
            l1 = self.comboBox.currentText()
            for key, val in googletrans.LANGUAGES.items():
                if val.capitalize() == l1:
                    l1 = key
                    break
            # The language selected in dropdown menu is used as "lang" here
            tts = gtts.gTTS(text, lang = l1)
            tts.save("x.mp3")
            playsound("x.mp3")
        except Exception as e:
            print(e)
            self.error_message(e)

            
    # Implementation of Speaker Icon for Input Text Widget.
    # It uses Google text-to-speech(gtts) Library to create the mp3 file and then plays it.
    # Old file is removed if it exists. 
    def text_to_speech_output(self):
        try:
            os.remove("x.mp3")
        except:
            pass
        try:
            text = self.textEdit_2.toPlainText()
            l2 = self.comboBox_2.currentText()
            for key, val in googletrans.LANGUAGES.items():
                if val.capitalize() == l2:
                    l2 = key
                    break
            # The language selected in dropdown menu is used as "lang" here
            tts = gtts.gTTS(text, lang = l2)
            tts.save("x.mp3")
            playsound("x.mp3")
        except Exception as e:
            print(e)
            self.error_message(e)

    # Implementation of Translate button, it uses googletrans library
    def translate(self):
        try:
            text1 = self.textEdit.toPlainText()
            l1 = self.comboBox.currentText()
            l2 = self.comboBox_2.currentText()

            trans = googletrans.Translator()
            translate = trans.translate(text1, src = l1, dest = l2)
            self.textEdit_2.setText(translate.text)
        except Exception as e:
            self.error_message(e)

    # This is to create an error message box if error is encountered.
    def error_message(self, text):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setWindowTitle("Error")
        msg.setText(str(text))
        msg.exec_()
        
        
    # This is to detect audio using speech recognition library.
    # It is accessed using the Mic icon
    def audio_to_text(self):
        try:
            trans = googletrans.Translator()
            with sr.Microphone() as source:
                print("Speak now:")
                audio = r1.listen(source, timeout = 2)

                try:
                    get = r1.recognize_google(audio)
                    t = trans.translate(get)
                    self.textEdit.setText(t.origin)
                except Exception as e:
                    self.error_message(e)
        except Exception as e:
            self.error_message(e)

            
    # This is to clear the text widgets
    def clear(self):
        self.textEdit_2.clear()
        self.textEdit.clear()
        try:
            os.remove("x.mp3")
        except:
            pass
        

    # This is the implementation of the Swap icon
    # It swaps the values in the dropdown menu for input and output text widgets
    def swap(self):
        l1 = self.comboBox.currentText()
        l2 = self.comboBox_2.currentText()
        self.comboBox.setCurrentText(l2)
        self.comboBox_2.setCurrentText(l1)


# Program Execution 
if __name__ == '__main__':
    a = QtWidgets.QApplication(sys.argv)
    app = Main()
    app.show()
    a.exec_()
