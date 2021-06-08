from tkinter import *
import sqlite3
import cv2
import numpy as np
from pyzbar.pyzbar import decode
cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)


def click_evnt(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        root2 = Tk()
        root2.title("Sepet")

        def sepet_list():
            con2 = sqlite3.connect("sepet.db")
            curser2 = con2.cursor()

        # query database
            curser2.execute("SELECT * FROM sepet")
            kyt = curser2.fetchall()

            print(kyt)

            print_kyt = 'SEPETTEKILER\n'

            for record in kyt:
                print_kyt += str(record[0]) + "   " + str(record[1]) + " tl " + "\n"

            sepet_label = Label(root2)
            sepet_label.config(text=print_kyt, font=("Arial", 9))
            sepet_label.place(x=45, y=90)

            con2.commit()
            con2.close()

        def total():
            con2 = sqlite3.connect("sepet.db")
            curser2 = con2.cursor()

            topl = curser2.execute("SELECT SUM(ürün_fiyat) FROM sepet")
            topl = curser2.fetchall()
            topl.append("tl")

            total_label = Label(root2)
            total_label.config(text=topl, font=("Arial", 9))
            total_label.place(x=190, y=90)

        def kapat():
            #kpt_label = Label(root2)
            #kpt_label.place(x=800, y=100)
            root2.destroy()
            #cv2.destroyAllWindows()

        sepet_btn = Button(root2, text="Listele", command=sepet_list)
        sepet_btn.place(x=50, y=50)

        tpl_btn = Button(root2, text="total", command=total)
        tpl_btn.place(x=180, y=50)

        kpt_btn = Button(root2, text="CLOSE", command=kapat)
        kpt_btn.place(x=10, y=10)
        root2.mainloop()





con2 = sqlite3.connect("sepet.db")
curser2 = con2.cursor()

def sepet():
    con2 = sqlite3.connect("sepet.db")
    curser2 = con2.cursor()
    curser2.execute("CREATE TABLE IF NOT EXISTS sepet (ürün_ad TEXT,ürün_fiyat INT,ürün_kod TEXT )")
    con2.commit()
sepet()

curser2.execute("SELECT ürün_kod FROM sepet")
myDataList2=(curser2.fetchall())




con = sqlite3.connect("ürün_list.db")
curser = con.cursor()

def listeolustur():
    curser.execute("CREATE TABLE IF NOT EXISTS ürün_list (ürün_ad TEXT, ürün_fiyat INT,ürün_kod TEXT )")
    con.commit()
listeolustur()

curser.execute("SELECT ürün_kod FROM ürün_list")
myDataList=(curser.fetchall())
#records = curser.fetchall()
print(myDataList)


while True:


    success, img = cap.read()

    con = sqlite3.connect("ürün_list.db")
    curser = con.cursor()


    #query database
    curser.execute("SELECT * FROM ürün_list")
    recordss=curser.fetchall()


    for barcode in decode(img):
       # print(barcode.data)
        myData = barcode.data.decode('utf-8')
        print(myData)

        if myData in str(myDataList):
            con = sqlite3.connect("ürün_list.db")
            curser = con.cursor()
            curser.execute("SELECT ürün_ad,ürün_fiyat FROM ürün_list WHERE ürün_kod=?",(myData,))
            record = curser.fetchone()
            myOutput=record
            myColor=(0,255,0)
            if myData not in str(myDataList2):
                con2 = sqlite3.connect("sepet.db")
                curser2 = con2.cursor()
                curser2.execute("INSERT INTO sepet VALUES (:ürün_ad, :ürün_fiyat, :ürün_kod) ",
                               {

                                   'ürün_ad': record[0],
                                   'ürün_fiyat': record[1],
                                   'ürün_kod': myData,

                               })

                con2.commit()
                con2.close()
                myDataList2.append(myData)
            else:

                pts = np.array([barcode.polygon], np.int32)
                pts = pts.reshape((-1, 1, 2))
                cv2.polylines(img, [pts], True, myColor, 5)
                pts2 = barcode.rect
                cv2.putText(img, str(myOutput), (pts2[0], pts2[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.9, myColor, 2)

            con.commit()
            con.close()

        else:

            myOutput = ' '
            myColor = (0, 0, 255)
            root = Tk()
            root.title("ürün ekle")
            # database
            con = sqlite3.connect("ürün_list.db")
            curser = con.cursor()
            # create submit func for database
            def submit():

                con = sqlite3.connect("ürün_list.db")
                curser = con.cursor()
                curser.execute("INSERT INTO ürün_list VALUES (:ürün_ad, :ürün_fiyat, :ürün_kod) ",
                               {

                                   'ürün_ad': urun_ad.get(),
                                   'ürün_fiyat': urun_fiyat.get(),
                                   'ürün_kod': myData,

                               })

                con.commit()
                con.close()

                # to clear
                urun_ad.delete(0, END)
                urun_fiyat.delete(0, END)
                #root.destroy()

            # create query function
            def query():
                con = sqlite3.connect("ürün_list.db")
                curser = con.cursor()

                # query database
                curser.execute("SELECT * FROM ürün_list")
                records = curser.fetchall()
                print(records)
                print_records = 'Sisteme Kayıtlı Ürünler\n'

                for record in records:
                    print_records += str(record[0]) + "   " + str(record[1]) + "   " + str(record[2]) + "\n"
                query_label = Label(root)
                query_label.config(text=print_records, font=("Arial", 9))
                query_label.place(x=100, y=300)



            def clsd():
                clsd_label = Label(root)
                # clsd_label.config(text=a, font=("Arial", 9))
                clsd_label.place(x=800, y=100)
                root.destroy()


            def delete():

                con = sqlite3.connect("ürün_list.db")
                curser = con.cursor()
                curser.execute("DELETE FROM ürün_list WHERE ürün_ad=?", (urun_ad.get(),))
                con.commit()
                con.close()

                # to clear
                urun_ad.delete(0, END)

            # create text boxes
            urun_ad = Entry(root)
            urun_ad.place(x=80, y=70)

            urun_fiyat = Entry(root)
            urun_fiyat.place(x=90, y=90)

            urun_ad_label = Label(root)
            urun_ad_label.config(text="Ürün Adı", font=("Arial", 9))
            urun_ad_label.place(x=20, y=70)

            urun_fiyat_label = Label(root)
            urun_fiyat_label.config(text="Ürün Fiyatı", font=("Arial", 9))
            urun_fiyat_label.place(x=20, y=90)

            submit_btn = Button(root, text="Add Record To Database", command=submit)
            submit_btn.place(x=100, y=150)

            query_btn = Button(root, text="Kayıtlar ", command=query)
            query_btn.place(x=100, y=200)

            clsd_btn = Button(root, text="clsd", command=clsd)
            clsd_btn.place(x=10, y=20)

            delete_btn = Button(root, text="Delete", command=delete)
            delete_btn.place(x=50, y=200)
            con.commit()
            con.close()


            root.mainloop()
            myDataList.append(myData)

        pts = np.array([barcode.polygon], np.int32)
        pts = pts.reshape((-1, 1, 2))
        cv2.polylines(img, [pts], True, myColor, 5)
        pts2 = barcode.rect
        cv2.putText(img, str(myOutput), (pts2[0], pts2[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.9, myColor, 2)

    cv2.imshow('Result', img)
    cv2.setMouseCallback('Result', click_evnt)
    cv2.waitKey(1)
    #cv2.setMouseCallback('Result', click_evnt)




