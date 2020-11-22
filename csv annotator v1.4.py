# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import sys
import tkinter as tk
import pandas as pd
import unicodedata
import codecs
from tkinter import messagebox
import os.path
from os import path


global tweet_counter
global rowNum

pd.set_option("display.max_colwidth", None)

file = "csv_for_annotation.csv"
df = pd.read_csv(file, usecols=['full_text'], encoding='utf-8')
df_copy = pd.read_csv(file, encoding='utf-8')


index = df.index
total_instances = len(index)
#print(total_instances)
#print(df.head())

root1 = tk.Tk()
frame1 = tk.Frame(root1)

root1.title("Starting Index")
root1.geometry('300x100')
frame1.pack(expand=True, fill=tk.BOTH)

label1 = tk.Label(frame1, text='Enter the row number')
label1.pack(side=tk.TOP)


entry1 = tk.Entry(frame1, bd=5)
entry1.pack(side=tk.TOP)



# global a
def getRowNum():
    a = entry1.get()

    global rowNum
    rowNum = a
    root1.destroy()


button1 = tk.Button(frame1, text='Submit', command=getRowNum)
button1.pack(side=tk.TOP)

label2 = tk.Label(frame1, text="Created by: Satanu Ghosh")
label2.config(font=("Helvetica", 5), fg="grey")
label2.pack(anchor=tk.SW)


def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        sys.exit()


root1.protocol("WM_DELETE_WINDOW", on_closing)
root1.mainloop()

print(rowNum)

#function for exit button
def terminate():
    #df_copy.index(getRowNum).insert(len(df_copy.columns), 'sentiment', emotion_list)
    print(emotion_list)
    print(tweet_counter)
    if path.exists("annotated_csv_"+rowNum+"-"+str(tweet_counter)+".csv"):
        messagebox.showinfo("Exit", "File Write Back Not Required")
    else:
        submit()
    #print(df_to_write.head())
    sys.exit()


#df_copy.insert(len(df_copy.columns), 'sentiment', [])
#print(df_copy.columns)

emotion_list = []
confidence_list = []

def next():

    #emotion_list = []
    emotion_list.append(emotion_type)
    confidence_level = x.get()
    confidence_list.append(confidence_level)
    root2.destroy()
    #df_copy.index(getRowNum).insert(len(df_copy), 'sentiment', emotion_series)

def submit():

    #df_copy['sentiment'] = ''

    df_to_write = pd.DataFrame(df_copy).set_index('tweet_id')[int(rowNum):tweet_counter].copy(deep=True)
    df_to_write.insert(len(df_to_write.columns), 'sentiment', emotion_list, allow_duplicates=True)
    df_to_write.insert(len(df_to_write.columns), 'confidence_level', confidence_list, allow_duplicates=True)

    #print(df_to_write.head())

    if int(rowNum) == tweet_counter:
        messagebox.showinfo("ERROR", "No annotation performed! No files written")
    else:
        df_to_write.to_csv("annotated_csv_"+rowNum+"-"+str(tweet_counter)+".csv", index=True, encoding="utf-8")
        messagebox.showinfo("Message", "File Write Back Successful")




#loop for iterating over the tweets
counter = 0
for i in range(int(rowNum), int(total_instances)):


    tweet_counter = counter + int(rowNum)
    content = df.iloc[i, 0]
    word = content.split(' ')
    #print(word)
    formatted_content = ''
    rem = 0
    for wordcount in range(len(word)):
        #print(wordcount)

        if rem < 7:
            #print(rem)
            formatted_content += word[wordcount]+' '
            rem += 1
        elif rem >= 7:
            #print(rem)
            formatted_content += "\n"
            rem = 0

    root2 = tk.Tk()
    root2.title("Annotator Window")
    #print(formatted_content)

    def on_closing():
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            sys.exit()


    root2.protocol("WM_DELETE_WINDOW", on_closing)

    #root2.geometry('400x150')
    frame2 = tk.Frame(root2)
    #frame2.config(height=3, width=3)
    # frame2.pack(side=tk.BOTTOM)
    frame2.grid(row=15, column=100)
    frame_label = tk.Frame(root2)
    frame_label.config(height=3, width=5)
    frame_label.grid(row=10, column=100)

    label2 = tk.Label(frame_label, text=formatted_content, bd=8, relief='groove')
    label2.config(font=("Times New Roman", 14), padx=3, pady=3)
    label2.grid(row=0, column=6, sticky=tk.W + tk.E)


    #label above radio button
    label_abv_radio = tk.Label(frame2, text="Classify the tweet with proper emotion. Choose the level of your confidence from the dropdown.", bd=5, bg="grey")
    label_abv_radio.pack(side=tk.TOP)

    # building a radio button structure and function related to it
    v = tk.IntVar()
    v.set(7)



    emotions = ["Love", "Joy", "Surprise", "Anger",
                "Sadness", "Fear", "Neutral", "Unrelated"]

    confidence = ["High", "Medium", "Low"]

    #emotion_type = "Unrelated"

    #function for radio button
    def showChoice():
        #print(v.get())
        emotion_num = v.get()
        global emotion_type

        if emotion_num is 0:
            emotion_type = "Love"
        elif emotion_num is 1:
            emotion_type = "Joy"
        elif emotion_num is 2:
            emotion_type = "Surprise"
        elif emotion_num is 3:
            emotion_type = "Anger"
        elif emotion_num is 4:
            emotion_type = "Sadness"
        elif emotion_num is 5:
            emotion_type = "Fear"
        elif emotion_num is 6:
            emotion_type = "Neutral"
        elif emotion_num is 7:
            emotion_type = "Unrelated"
        else:
            emotion_type = "None"
            



    for val, emotion in enumerate(emotions):
        tk.Radiobutton(frame2,
                       text=emotion,
                       padx=20,
                       variable=v,
                       command=showChoice,
                       value=val).pack(anchor=tk.W)


    x = tk.StringVar(root2)
    x.set(confidence[1])

    opt = tk.OptionMenu(frame2, x, *confidence)
    opt.config(bg='seashell3')
    opt.pack(anchor=tk.NE)






    """buttonL = tk.Button(frame2, text='Love')
    buttonJ = tk.Button(frame2, text='Joy')
    buttonSu = tk.Button(frame2, text='Surprise')
    buttonA = tk.Button(frame2, text='Anger')
    buttonSa = tk.Button(frame2, text='Sadness')
    buttonF = tk.Button(frame2, text='Fear')
    buttonN = tk.Button(frame2, text='Neutral')
    buttonU = tk.Button(frame2, text='Unrelated')"""
    buttonE = tk.Button(frame2, text='EXIT', command=terminate, bg='red')
    buttonN = tk.Button(frame2, text="NEXT", command=next, bg="green")
    buttonS = tk.Button(frame2, text="SAVE PROGRESS", command=submit, bg='yellow')
    # buttonL.pack(side=tk.LEFT)
    # buttonJ.pack(side=tk.LEFT)
    # buttonSu.pack(side=tk.LEFT)
    # buttonA.pack(side=tk.LEFT)
    # buttonSa.pack(side=tk.LEFT)
    # buttonF.pack(side=tk.LEFT)
    # buttonN.pack(side=tk.LEFT)
    # buttonU.pack(side=tk.LEFT)


    """buttonL.grid(row=4, column=15, sticky=tk.W + tk.E)
    buttonJ.grid(row=4, column=16, sticky=tk.W + tk.E)
    buttonSu.grid(row=4, column=17, sticky=tk.W + tk.E)
    buttonA.grid(row=4, column=18, sticky=tk.W + tk.E)
    buttonSa.grid(row=6, column=15, sticky=tk.W + tk.E)
    buttonF.grid(row=6, column=16, sticky=tk.W + tk.E)
    buttonN.grid(row=6, column=17, sticky=tk.W + tk.E)
    buttonU.grid(row=6, column=18, sticky=tk.W + tk.E)"""
    #buttonE.grid(row=18, column=15)

    buttonE.pack(side=tk.LEFT)
    buttonN.pack(side=tk.RIGHT)
    buttonS.pack(side=tk.BOTTOM)
    counter = counter + 1
    root2.mainloop()


# print(rowNum)
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
