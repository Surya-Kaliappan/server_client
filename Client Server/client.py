import socket
import threading
import tkinter as tk
from tkinter import scrolledtext
from tkinter import messagebox
import ssl

HOST = 'localhost'
PORT = 1234
theme = 0

root = tk.Tk()
root.geometry("600x600")
root.title("Conversation Room")
root.resizable(False,False)
FONT = ("Helvetica",16)
TFONT = ("Helvetica",9)
BFONT = ("Helvetica",15)
MFONT = ("Helvetica",12)
OB = '#464EBB'
MGREY = '#1F1B24'

try:
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    context.load_verify_locations('new.pem')

    soc = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    client = context.wrap_socket(soc, server_hostname=HOST)
except:
    print("Connection Failed")
    exit(0)

def username_click(*args):
    check = username_textbox.get()
    if check=="Enter Username":
        username_textbox.delete(0,'end')

def username_leave(*args):
    check = username_textbox.get()
    if check == "" or check[0] == " ":
        username_textbox.delete(0,'end')
        username_textbox.insert(0,"Enter Username")
        root.focus()


def update_message(message):
    message_box.config(state=tk.NORMAL)
    message_box.insert(tk.END,message+'\n')
    message_box.config(state=tk.DISABLED)

def update_team_count(count):
    team_count_num.config(text=count)

def connect():
    try:
        global username
        username = username_textbox.get()
        if username != '':
            print("Connecting....")
            client.connect((HOST,PORT))
            root.bind('<Return>',send_message_button)
            message_button.config(state=tk.NORMAL)
            status_name.pack(side=tk.LEFT,padx=10)
            status.pack(side=tk.LEFT,padx=0)
            status.config(text="ONLINE",fg="green")
            team_count_num.pack(side=tk.RIGHT,padx=(0,40))
            team_count.pack(side=tk.RIGHT)
            print(f"Successfully connected to SERVER on {HOST} {PORT}")
            update_message("[SERVER] \"Successfully connected to the HOST\"")
            client.sendall(username.encode())
            username_textbox.config(state=tk.DISABLED)
            username_button.config(state=tk.DISABLED)
        else:
            messagebox.showerror("Invalid Error","Username cannot be empty")
            return 

        global run
        run = threading.Thread(target=listen_for_messages_from_server, args=(client, ))
        run.start()        

    except Exception as e:
        messagebox.showerror("Connection Failed",f"Unable to connect to SERVER on {HOST} {PORT}")
        print(e)
        return
    
def send_message():
    message = message_textbox.get()
    if message != '':
        client.sendall(message.encode())
        message_textbox.delete(0,len(message)+1)
    else:
        messagebox.showerror("Exit","Empty Message")

def send_message_button(event):
    send_message()

def connect_button(event):
    connect()

def on_closing_button(event):
    on_closing()

def change_theme():
    global theme
    if theme%2 == 0:
        message_box.config(bg="#fff",fg="#000")
        theme_button.config(text="Dark",fg="#000")
        theme = 1
    else:
        message_box.config(bg="#000",fg="#fff")
        theme_button.config(text="Light",fg="#fff")
        theme = 0

root.grid_rowconfigure(0,weight=1)
root.grid_rowconfigure(1,weight=4)
root.grid_rowconfigure(2,weight=1)

top_frame = tk.Frame(root,width=600,height=100,bg="lightblue")
top_frame.grid(row=0,column=0,sticky=tk.NSEW)

middle_frame = tk.Frame(root,width=600,height=400,bg="#000")
middle_frame.grid(row=1,column=0,sticky=tk.NSEW)

bottom_frame = tk.Frame(root,width = 600,height=100,bg='lightblue')
bottom_frame.grid(row=2,column=0,sticky=tk.NSEW)

username_textbox = tk.Entry(top_frame,font=FONT,fg="#000",width=23)
username_textbox.insert(0,"Enter Username")
username_textbox.pack(side=tk.LEFT,padx=30)
username_textbox.bind("<Button-1>",username_click)
username_textbox.bind("<Leave>",username_leave)

username_button = tk.Button(top_frame,text="Join",font=BFONT,bg=OB,fg="#fff",command=connect)
username_button.pack(side=tk.LEFT,padx=10)
root.bind('<Return>',connect_button)

status_name = tk.Label(top_frame,text="STATUS :",font=MFONT,bg="lightblue",fg="#000")

status = tk.Label(top_frame,text="OFFLINE",font=MFONT,bg="lightblue",fg="red")

message_textbox = tk.Entry(bottom_frame,font=FONT,fg="#000",width=40)
message_textbox.pack(side=tk.LEFT,padx=15)

message_button = tk.Button(bottom_frame,text="Send",font=BFONT,bg=OB,fg="#fff",command=send_message)
message_button.config(state=tk.DISABLED)
message_button.pack(side=tk.LEFT,padx=10)

message_box = scrolledtext.ScrolledText(middle_frame,font=MFONT,bg="#000",fg="#fff",width=67,height=26.5)
message_box.config(state=tk.DISABLED)
message_box.pack(side=tk.TOP)

team_count_num = tk.Label(middle_frame,font=TFONT,fg="#fff",bg="#000")
team_count = tk.Label(middle_frame,text="Group Strength :",font=TFONT,fg="#fff",bg="#000")

theme_name = tk.Label(middle_frame,text="Change Theme",font=TFONT,fg="#fff",bg="#000")
theme_name.pack(side=tk.LEFT,padx=20)
theme_button = tk.Button(middle_frame,text="LIGHT",font=TFONT,bg=OB,fg="#fff",command=change_theme)
theme_button.pack(side=tk.LEFT)

root.bind('<Escape>',on_closing_button)
    
def listen_for_messages_from_server(client):
    try:
        while True:
            message = client.recv(2048).decode('utf-8')
            if message != '':
                client_username = message.split('~')[0]
                client_content = message.split('~')[1]
                count = message.split('~')[2]
                message_textbox.focus()
                if client_username == username:
                    client_username = "ME"
                update_message(f"[{client_username}]\t\"{client_content}\"")
                update_team_count(count)
                
            else:
                messagebox.showerror("Invalid Error","Message recieved from client is empty")
    except:
        update_message(f"!! ~~ SERVER {HOST} {PORT} has Disconnected ~~")
        username_button.config(state=tk.NORMAL)
        message_button.config(state=tk.DISABLED)
        message_textbox.config(takefocus=0)
        root.bind('<Return>',connect_button)
        status.config(text="OFFLINE",fg="red")
        update_team_count("")
        print("Can't reach the SERVER...")
        
def on_closing():
    if messagebox.askokcancel("Quti","Do you want ot Leave from this Chat ?"):
        try:
            if username != '':
                client.close()
                print("Disconnected from the server")
        except:
            pass
        finally:
            root.destroy()

def main():
    root.protocol("WM_DELETE_WINDOW",on_closing)
    root.mainloop()

if __name__ == '__main__':
    main()
