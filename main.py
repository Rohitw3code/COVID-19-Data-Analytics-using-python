from bs4 import BeautifulSoup
import requests
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import*
from tkinter import ttk
from pandas import DataFrame

root=Tk()
root.geometry('850x700')
root.config(bg='white')
root.wm_iconbitmap('virus1.ico')
root.title('COVID-19 Data Analytics')
#-----------------------------------------------------------------------
source=requests.get("https://www.worldometers.info/coronavirus/").text
soup=BeautifulSoup(source,'lxml')

match=soup.find('tbody')
match=match.find_all('tr')
#-----Frame-------------------------------------------
s = ttk.Style()
s.configure('TNotebook.Tab', font=('Comic Sans MS','15'))
tab=ttk.Notebook(root)

#--to style Button--------------------------

style = ttk.Style()
style.map("C.TButton",
    foreground=[('pressed', 'red'), ('active', 'blue')],
    background=[('pressed', '!disabled', 'black'), ('active', 'white')]
    )
style.configure('TButton', font = 
               ('calibri',18, 'bold'), 
                    borderwidth = '1')
#-------Image-----------------------------------------------------------------
canvas=Canvas(root,width=128,height=128,bg='white')
canvas.place(x=600,y=55)
profile=PhotoImage(file='protection.png')
canvas.create_image(0,0,anchor=NW,image=profile)

#-----------------------------------------------------------------------------
world=[]
continents=[]
no=0
for i in match:
   data=i.text.split('\n')
   fun=lambda a:False if a=='' else True
   data=list(filter(fun,data))
   if no<8:
      continents.append(data)
      no+=1
      continue
   world.append(data)
#-----------------------------------------------------
all_=Frame(tab, bg='white',width="800",height="200")
tab.add(all_,text="  world  ")

for i in ['Cases','Recovered','Death']:
   mm=i
   globals()[mm]=Frame(tab, bg='white',width="800",height="600")
   tab.add(eval(mm),text='  '+i+'  ')
tab.place(x=10,y=200,width=800,height=400)
tree=ttk.Treeview(all_)
#--Cases--------------------------------------------------------------------
name=[]
cases=[]
a=0
no=[]
for i in match:
   data=i.text.split('\n')
   fun=lambda a:False if a=='' else True
   data=list(filter(fun,data))
   name.append(data[0])
   value=int(data[1].replace(',',''))
   cases.append(value)
   a+=1
   no.append(a)
   if a==6:
      break
data1 = {'Country':name,
         'Cases':cases
        }
df1 = DataFrame(data1,columns=['Country','Cases'])
   
figure1 = plt.Figure(figsize=(5,6), dpi=100)
ax1 = figure1.add_subplot(111)
line1 = FigureCanvasTkAgg(figure1, Cases)
line1.get_tk_widget().pack(fill=BOTH)
df1 = df1[['Country','Cases']].groupby('Country').sum()
df1.plot(kind='line', legend=True, ax=ax1, color='orange',marker='o', fontsize=10)
ax1.set_title('Cases')
ax1.tick_params(axis='x', labelrotation=10)
#--Recovered--------------------------------------------------------------------
name=[]
cases=[]
a=0
no=[]
for i in match:
   data=i.text.split('\n')
   fun=lambda a:False if a=='' else True
   data=list(filter(fun,data))
   name.append(data[0])
   value=int(data[4].replace(',',''))
   cases.append(value)
   a+=1
   no.append(a)
   if a==6:
      break
data2 = {'Country':name,
         'Recovered':cases
        }
df2 = DataFrame(data2,columns=['Country','Recovered'])
   
figure2 = plt.Figure(figsize=(5,4), dpi=100)
ax2 = figure2.add_subplot(111)
line2 = FigureCanvasTkAgg(figure2, Recovered)
line2.get_tk_widget().pack(fill=BOTH)
df2 = df2[['Country','Recovered']].groupby('Country').sum()
df2.plot(kind='line', legend=True, ax=ax2, color='green',marker='o', fontsize=10)
ax2.set_title('Recovered')
ax2.tick_params(axis='x', labelrotation=10)
#-----------------------------------------------------------------------
#--Death--------------------------------------------------------------------
name=[]
cases=[]
a=0
no=[]
for i in match:
   data=i.text.split('\n')
   fun=lambda a:False if a=='' else True
   data=list(filter(fun,data))
   name.append(data[0])
   value=int(data[3].replace(',',''))
   cases.append(value)
   a+=1
   no.append(a)
   if a==6:
      break
data3 = {'Country':name,
         'Death':cases
        }
df3 = DataFrame(data3,columns=['Country','Death'])
   
figure3 = plt.Figure(figsize=(5,4), dpi=100)
ax3 = figure3.add_subplot(111)
line3 = FigureCanvasTkAgg(figure3,Death)
line3.get_tk_widget().pack(fill=BOTH)
df3 = df3[['Country','Death']].groupby('Country').sum()
df3.plot(kind='line', legend=True, ax=ax3, color='r',marker='o', fontsize=10)
ax3.set_title('Death')
ax3.tick_params(axis='x', labelrotation=10)

#-----------------------------------------------------------------------

cnty=('sno','country','Total Cases','New Cases','Total Death',
                 'Total Recovered','Active Cases','Serious Critical')
tree['columns']=cnty
tree.column('#0',width=50)
tree.column('#1',width=120)
for i in range(2,8):
   if i==1:
      tree.column('#'+str(i),width=150)
      continue
   tree.column('#'+str(i),width=105)
for i in range(8):
   tree.heading('#'+str(i),text=cnty[i])
a=1
for country in world:
   try:
      tree.insert('',str(a),'item '+str(a),text=a,values=(country[0],country[1],country[2],
                                                          country[3],country[4],country[5],country[6]), tags = ('oddrow',))
      a+=1
   except:
      pass
   
tree.tag_configure('oddrow', background='white')
for i in continents:
   if i[0].lower()=='world':
      break
Label(root,text="World COVID-19 Data Analytics",fg="blue",bg='white',font=('Comic Sans MS',20)).pack()
Label(root,text="Coronavirus Cases : "+str(i[1]),bg='white',fg="orange",font=('Comic Sans MS',20)).place(x=10,y=50)
Label(root,text="Deaths : "+str(i[3]),fg="red",bg='white',font=('Comic Sans MS', 20)).place(x=10,y=100)
Label(root,text="Recovered : "+str(i[5]),fg="green",bg='white',font=('Comic Sans MS',20)).place(x=10,y=150)
tree.pack()
root.mainloop()
