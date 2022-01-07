from aes_cbc import AES_CBC
from oracleAttack import find_plaintext
from tkinter import *
global_cipher = AES_CBC()

def encryptText():
    global ps
    global ciphertext
    ps = entry.get()
    ciphertext = global_cipher.encrypt(ps)
    l5 = Label(window, text="Encrypted text using AES-CBC-PKCS5 is:")
    l5.place(x=20, y=220)
    l5 = Label(window, text=ciphertext)
    l5.place(x=20, y=260)

def oracleAttack():
    global plaintext
    plaintext = find_plaintext(ciphertext)
    l5 = Label(window, text="Decrypted text using oracle padding attack on AES-CBC-PKCS5 is:")
    l5.place(x=20, y=340)
    l5 = Label(window, text=plaintext)
    l5.place(x=20, y=380)

if __name__ == "__main__":
    window = Tk()
    window.title("Padding Oracle Attack")
    window.geometry('1000x750')

    frame = LabelFrame(
        window,
        text='Padding Oracle Attack on AES-CBC with PKCS5 encoding',
        bg='#f0f0f0',
        font=(20)
    )
    frame.pack(expand=True, fill=BOTH)

    l1 = Label(window, text="Enter text to encrypt and then perform an oracle attack on it ")
    l1.place(x=20, y=100)

    entry = Entry(window, width=70)
    entry.place(x=20, y=140)

    btn1 = Button(window, text="Encrypt", width=20, command=encryptText)
    btn1.place(x=20, y=180)

    btn2 = Button(window, text="Attack using Oracle Padding Attack", width=30, command=oracleAttack)
    btn2.place(x=20, y=300)

    window.mainloop()