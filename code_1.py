# smart-store-inventory

from tkinter import messagebox
from tkinter import *
from datetime import date
import os, csv, pickle, mysql.connector
mydb = mysql.connector.connect(host= "localhost", port="3306",user= "root",password="aman7015", database="project")
mycursor = mydb.cursor()
table = 'items'
subHeadingFont = "Helvetica 10 bold" 
HeadingFont = "Helvetica 13 bold" 
item_Entry_List=[] # [[icode1,qty1],[icode2,qty2],[icode3,qty3]]

# root window

root = Tk()
root.title("Prajapati Store")
root.geometry('681x500')
#different screens

sale_Screen= Frame(root)
login_Screen = Frame(root) 
admin_Screen = Frame(root) 
sale_Screen.pack(fill='both', expand=1)

#default screen
def tologin(): 
    login_Screen.pack(fill='both', expand=1) 
    sale_Screen.pack_forget()

def backToSale(): 
    sale_Screen.pack(fill='both', expand=1) 
    login_Screen.pack_forget()

def tosale(): 
    sale_Screen.pack(fill='both', expand=1) 
    admin_Screen.pack_forget()

def authenticate():
    uname = entry_1.get()
    password = entry_2.get()
    if(uname == "" and password == "") :
        messagebox.showinfo("", "Blank Not allowed") 
    elif(uname == "aman7015" and password == "aman7015"):
        messagebox.showinfo("","Login Success") 
        admin_Screen.pack(fill='both', expand=1) 
        login_Screen.pack_forget() 
        entry_1.delete(0, END) 
        entry_2.delete(0, END)
    else :
        messagebox.showinfo("","Incorrent Username and Password")

   
# main funtions
def insertIntoFrame (t,frame):
    Label(frame,text="Product Name",font=subHeadingFont).grid(column=0,row=0,sticky=W)
    Label(frame,text="P Code",font=subHeadingFont).grid(column=1,row=0,sticky=W)
    Label(frame,text="Price",font=subHeadingFont).grid(column=2,row=0,sticky=W)
    Label(frame,text="Stock",font=subHeadingFont).grid(column=3,row=0,sticky=W)
    for i in range(len(t)):
        for j in range(4):
            Label(frame, text= str(t[i][j]),padx=10).grid(column=j,row=i+1,sticky = W)

def emptyFrame(frame):
    for widgets in frame.winfo_children():
        widgets.destroy()

def fetchall(frame):
    emptyFrame(frame)
    mycursor.execute("select * from "+table)
    t = mycursor.fetchall()
    insertIntoFrame(t,frame)

def add_More_Entry():
    icEntry = Entry(Icode_col,width= 7)
    icEntry.pack()
    pEntry = Entry(qty_col,width= 4)
    pEntry.pack()
    itemList = []
    itemList.append(icEntry)
    itemList.append(pEntry)
    item_Entry_List.append(itemList)

def delete_Entry():
    item_Entry_List[-1][0].destroy()
    item_Entry_List[-1][1].destroy()
    item_Entry_List.pop()
def edit_text_area(textArea, inputStr):
    textArea.configure(state='normal')
    if inputStr=="":
        textArea.delete("1.0", "end")
    else:
        textArea.insert(END,inputStr) 
        textArea.configure(state='disabled')

def makedayfolder(foldername):
  try:
    os.makedirs(foldername)
  except OSError:
    pass
   
def Billmaker(list1):
    orderNo = list1[0]
    data = list1[1]
    noOfItems=list1[2]
    total = list1[3]
    billNo =list1[4]

    makedayfolder("Bills/"+billNo[0:10])
    B = open("Bills/"+billNo[0:10]+"/"+billNo+".txt",'w+') 
    B.write("\t\t\t\tBILL\n") 
    B.write("-------------------------------------------------\n") 
    B.write("Bill No. : \t\t\t\t\t"+billNo+'\n')
    B.write("Order No. : \t\t\t\t"+str(orderNo)+'\n') 
    B.write("-------------------------------------------------\n") 
    B.write("\t\t\tPrajapati Store\n") 
    B.write("_________________________________________________\n") 
    B.write("Item Name\t\tQty\tPrice\t\t\tTotal\n") 
    B.write("-------------------------------------------------\n") 
    for i in range(noOfItems):
        # print(data[i])
        itemcol = str(data[i][0])+'\t\t'+str(data[i][2])+'\t'+str(data[i][1]) +'\t\t\t'+str(data[i][2]*data[i][1]) +'\n'
        B.write(itemcol) 
    B.write("_________________________________________________\n") 
    B.write("GRAND TOTAL = " +str(total)+'\n') 
    B.write("_________________________________________________\n") 
    B.close()
   
   
   
def update_orderno():
    f = open("supporting files/lastbill.txt","r+") 
    o = f.read()
    global ON, table
    Date,orderno = o.split('__')
    if str(date.today()) == Date:
            ON = int(orderno) + 1
    else:
            ON = 1
    f.close()

    
class bill():
    def __init__(self, orderno, itemsList):
        data = []        #[[IName, price, Qty],...]
        T = 0            # total Bill ammount
        for item in itemsList:
            # mystr = "select IName, price from "+table+" where ICode = "+'"'+str(item[0].get())+'"'
            # print(mystr)
            mycursor.execute("select IName, price from "+table+" where ICode = "+'"'+str(item[0].get())+'"')
            k = mycursor.fetchone()
            li = list(k) #[IName, price]
            qty = int(item[1].get())
            li.append(qty)         #[IName, price, qty]
            data.append(li)
            price = k[1]
            T = T+ qty*price

        self.orderNo = orderno
        self.data = data # [itemName,price, quantity req.] 
        self.noOfItems = len(itemsList)
        self.total = T
        self.billNo = str(date.today())+"__"+str(orderno)

def checkout(orderno, item_Entry_List):
    Bill = bill(orderno, item_Entry_List)
    edit_text_area(errorDisplay,"")
    validBill = True

    for i in range(len(item_Entry_List)):
        mycursor.execute("select stock from "+table+" where ICode ="+'"'+str(item_Entry_List[i][0].get())+'"') 
        k = mycursor.fetchone()
        s = int(k[0])               #avilable stock
        q = Bill.data[i][2]         #quantity req.
        if s < q:
            errormsg = str(Bill.data[i][0])+" is out of stock. \n Avialable Stock = "+str(s)+"\n"
            edit_text_area(errorDisplay,errormsg,) 
            validBill = False
    if validBill:
        update_orderno()
        Bill_data = [Bill.orderNo, Bill.data, Bill.noOfItems,Bill.total, Bill.billNo]
        Billmaker(Bill_data)
        G = open("supporting files/billdata.bin","ab") 
        pickle.dump(Bill_data, G)
        G.close
        global ON
        ON += 1
        billNo.config(text ="BILL NO :"+str(date.today())+"__"+str(ON))
        
        # updating last bill no inside the lastbill file ... to store it permanently.
        f = open("supporting files/lastbill.txt","w")
        f.write(Bill.billNo)
        f.close()

        # have to think about it..
        # path = Bill.billNo[0:10]+"/"+Bill.billNo+".txt" 
        # os.startfile(path, "open")

        for i in range(len(item_Entry_List)): #upating stock after bill is paid....
            IC = str(item_Entry_List[i][0].get())
            ST = int(item_Entry_List[i][1].get()) 
            mycursor.execute('UPDATE '+table+' SET stock = stock -'+ str(ST)+' WHERE ICode = "' +IC+'"')
            mydb.commit()

            #empting iCode and Qty entries
            for j in item_Entry_List[i]:
                j.delete(0, END)
        fetchall(table_space)


def update_price(): 
    edit_text_area(errorDisplay,'') 
    T=0
    for item in item_Entry_List:
        mycursor.execute("select price from "+table+" where ICode = "+'"'+str(item[0].get())+'"')
        k = mycursor.fetchone()
        T = T + k[0]*int(item[1].get()) 
    tatal_Label.config(text ="Total = Rs. "+str(T))



# funtions for Admin screen
def fetchonly (frame,a):
    emptyFrame(frame)
    mycursor.execute("select * from "+table+" where stock <= "+ str(a))
    t = mycursor.fetchall()
    insertIntoFrame(t,frame) 
    edit_text_area(statementarea,mycursor.statement+"\n" )

def importFromCSV(myfile):
    mycursor.execute("select ICode from "+table+" ") 
    items = mycursor.fetchall()
    f = open(myfile, 'r+',newline="")
    csvr = csv.reader(f)
    for i in csvr:
        if (i[1],) in items:
            str1 = 'UPDATE '+table+' SET price = '+str(i[2])+',stock = stock +'+ str(i[3])+' WHERE ICode = "' +str(i[1])+'"' 
        else :
            str1='INSERT INTO '+table+' VALUES ("'+str(i[0])+'","'+str(i[1])+'",'+str(i[2])+','+str(i[3])+')'
        mycursor.execute(str1)
        mydb.commit() 
        edit_text_area(statementarea,mycursor.statement+"\n" )
    fetchall(frame_0_u)


def editStock_Price():
    str1 = 'UPDATE '+table+' SET price = '+str(Price.get())+', stock=  stock +'+str(Stock1.get())+' WHERE ICode ="'+str(ICode.get())+'"'
    mycursor.execute(str1)
    mydb.commit() 
    edit_text_area(statementarea,mycursor.statement+"\n" ) 
    fetchall(frame_0_u)
    for i in [ICode,Price,Stock1]:
            i.delete(0, END)


def additem():
    str1='INSERT INTO '+table+' VALUES("'+str(iName.get())+'","'+str(iCode.get())+'",'+str(iPrice.get())+' ,'+str(stock1.get())+')'
    mycursor.execute(str1)
    mydb.commit() 
    edit_text_area(statementarea,mycursor.statement+"\n" ) 
    fetchall(frame_0_u)
    for i in [iName, iCode,iPrice,stock1]:
            i.delete(0, END)

         
def delete_item(iCode):
    command = 'DELETE FROM '+table+' WHERE ICode = "'+iCode+'"' 
    mycursor.execute(command)
    mydb.commit()
    del_iCode.delete(0,END) 
    edit_text_area(statementarea,mycursor.statement+"\n" ) 
    fetchall(frame_0_u)




# Sale screen UI
table_space = Frame(sale_Screen) 
table_space.grid(column=0,rowspan=10, padx="30") 
update_orderno()
fetchall(table_space)

add_to_cart = Frame(sale_Screen) 
add_to_cart.grid(column=1,row =0, padx="30") 
Label(add_to_cart,text="Add to cart",font=HeadingFont).grid(row=0,columnspan=2) 
Icode_col = Frame(add_to_cart) 
Icode_col.grid(column=0,row=1)
Label(Icode_col,text="I Code",font=subHeadingFont).pack() 
qty_col = Frame(add_to_cart) 
qty_col.grid(column=1,row=1) 
Label(qty_col,text="Qty",font=subHeadingFont).pack()
buttons_add_to_cart = Frame(sale_Screen) 
buttons_add_to_cart.grid(column=1,row=3)


Button(buttons_add_to_cart,text="add more", command= add_More_Entry).grid(column=0,row=0) 
Button(buttons_add_to_cart,text="delete", command= delete_Entry).grid(column=1,row=0)
Button(sale_Screen,text="Admin Screen", bg="#90EE90", command=tologin).place(x =510, y=10)
errorDisplay= Text(sale_Screen,wrap= NONE,width=25,height=5,state='disabled') 
errorDisplay.place(x=440,y = 50)
action_Frame = Frame(sale_Screen) 
action_Frame.place(x=495, y=170) 
Button(action_Frame,text="Calculate total", bg="#ADD8E6", command=update_price).pack()
Label(action_Frame).pack()
Button(action_Frame,text="Check Out",bg="#ADD8E6",command=lambda:checkout(ON,item_Entry_List)).pack( )
Label(action_Frame).pack()
tatal_Label= Label(action_Frame,text= "Total = Rs. 0",font=("bold", 12))
tatal_Label.pack()
Label(action_Frame).pack()
billNo= Label(action_Frame,text= "BILL NO : "+str(date.today())+"__"+str(ON))
billNo.pack()
for i in range(1):
    add_More_Entry()



# Login screen UI
labl_0 = Label(login_Screen, text="login",width=20,font=("bold", 20))
labl_0.place(x=90,y=60)
labl_1 = Label(login_Screen, text="User Name",width=20,font=("bold", 10))
labl_1.place(x=80,y=130)
entry_1 = Entry(login_Screen)
entry_1.place(x=240,y=130)
labl_2 = Label(login_Screen, text="Password",width=20,font=("bold", 10))
labl_2.place(x=80,y=180)
entry_2 = Entry(login_Screen, show="*")
entry_2.place(x=240,y=180)
Button(login_Screen, text='Submit',command=authenticate,width=20,bg='brown',fg='white').place(x=180,y=230)
Button(login_Screen, text='Go Back',command=backToSale).place(x=10,y=10)


# Admin screen UI

frame_0_0= Frame(admin_Screen ,pady = 10, padx = 30) 
frame_0_0.grid(column=0,row=0,sticky = S) 
Button(frame_0_0,text="Show all",bg="#FFB6C1",command=lambda:fetchall(frame_0_u)).grid(column=0, row=0)
stock = Entry(frame_0_0, width=7)
stock.grid(column=0,row=1)
Button(frame_0_0,text=">= only", bg="#FFB6C1", command=lambda:fetchonly(frame_0_u,stock.get())).grid(column=1,row=1 )
Button(frame_0_0,text="remove all", bg="#FFB6C1", command=lambda:emptyFrame(frame_0_u)).grid(column=1,row=0)
frame_1_0 = Frame(admin_Screen) 
frame_1_0.grid(column=1,row=0)
path = Entry(frame_1_0, width=10) 
path.grid(column=0,row=0) 
Button(frame_1_0,text="import using CSV", command=lambda:importFromCSV(str(path.get())), bg="#ADD8E6").grid(column=0,row=1)
frame_0_u= Frame(admin_Screen, pady = 10, padx = 5) 
frame_0_u.grid(column=0,rowspan=2,sticky = N)
frame_1_1= Frame(admin_Screen) 
frame_1_1.grid(column=1,row=1,sticky = N,padx="30",pady="10")
Label(frame_1_1,text= "Edit Stock/Price",font='Helvetica 11 bold').pack()
Coframe_1_1= Frame(frame_1_1)

Coframe_1_1.pack()
Label(Coframe_1_1,text= "Item Code : ").grid(column=0,row=1,sticky = W)
ICode = Entry(Coframe_1_1, width=10)
ICode.grid(column=1,row=1)
Label(Coframe_1_1,text= "Stock : ").grid(column=0,row=2,sticky = W) 
Stock1 = Entry(Coframe_1_1, width=10)
Stock1.insert(0, "0")
Stock1.grid(column=1,row=2)
Label(Coframe_1_1,text= "Price : ").grid(column=0,row=3,sticky = W) 
Price = Entry(Coframe_1_1, width=10)
Price.grid(column=1,row=3)
Button(frame_1_1,text="Update", command=editStock_Price,bg="#ADD8E6").pack()
frame_1_2 = Frame(admin_Screen) 
frame_1_2.grid(column=1,row=2,sticky = N,padx="30", pady="20")
Label(frame_1_2,text= "Add Item",font='Helvetica 11 bold').pack() 
Coframe_1_2= Frame(frame_1_2)
Coframe_1_2.pack()
Label(Coframe_1_2,text= "Item Name : ").grid(column=0,row=1,sticky = W)
iName = Entry(Coframe_1_2, width=10)
iName.grid(column=1,row=1)
Label(Coframe_1_2,text= "Item Code : ").grid(column=0,row=2,sticky = W)
iCode = Entry(Coframe_1_2, width=10)
iCode.grid(column=1,row=2)

   
Label(Coframe_1_2,text= "Stock : ").grid(column=0,row=3,sticky = W) 
stock1 = Entry(Coframe_1_2, width=10)
stock1.grid(column=1,row=3)
Label(Coframe_1_2,text= "Price : ").grid(column=0,row=4,sticky = W) 
iPrice = Entry(Coframe_1_2, width=10)
iPrice.grid(column=1,row=4)
Button(frame_1_2,text="Add", command=additem,bg="#ADD8E6").pack()
frame_u_3 = Frame(admin_Screen,pady=10,height=30, padx=10) 
frame_u_3.grid(row=3,columnspan=2)
v_sb = Scrollbar(frame_u_3)
v_sb.pack(side=RIGHT,fill = Y)
statementarea = Text(frame_u_3,wrap= NONE,width=80,height=6) 
statementarea.configure(state='disabled') 
statementarea.pack(side=TOP,fill=X) 
v_sb.config(command=statementarea.yview)
Label(admin_Screen,text= "Remove Item",font='Helvetica 11 bold').place(x=327,y=82)
Label(admin_Screen,text= "I Code : ").place(x=325 , y = 110) 
del_iCode = Entry(admin_Screen, width=7)
del_iCode.place(x= 375, y = 110) 
Button(admin_Screen,text="Delete",bg="#ADD8E6", command=lambda:delete_item(del_iCode.get())).place(x=350,y = 135)
Button(admin_Screen,text="Sale Screen", bg="#90EE90", command=tosale).place(x = 330, y = 10) 
fetchall(frame_0_u)
root.mainloop()
