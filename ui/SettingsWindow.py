import tkinter as tk


def tkinter_window():
    window = tk.Tk()
    window.geometry('300x200')
    window.title('ScuttleBuddy')
    test_icon = tk.PhotoImage(file='./datadragon/summonerSpells/SummonerSmite.png')
    testButton = tk.Button(
        window,
        image=test_icon,
        text='Test',
        compound=tk.LEFT,
        command=lambda: window.quit()
    )
    testButton.pack(
        ipadx=5,
        ipady=5,
        expand=True
    )
    window.mainloop()
