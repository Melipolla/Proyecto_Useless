import tkinter as tk
ventana = tk.Tk()
ventana.title("Menú")

ventana.geometry('640x480+450+150')
ventana.configure(background='black')
var1=tk.StringVar(ventana)
var1.set('Juego Nuevo')
var2=tk.StringVar(ventana)
var2.set('Puntajes')
var3=tk.StringVar(ventana)
var3.set('Salir')
opcion1=['                                  Juego Nuevo                                           ']
opcion2=['                                      Puntajes                                               ']
opcion3=['                                          Salir                                                   ']
opcion3=tk.OptionMenu(ventana,var3,*opcion3)
opcion3.config(width=50)
opcion3.pack(side='bottom',padx=40,pady=40)
opcion2=tk.OptionMenu(ventana,var2,*opcion2)
opcion2.config(width=50)
opcion2.pack(side='bottom',padx=40,pady=40)
opcion1=tk.OptionMenu(ventana,var1,*opcion1)
opcion1.config(width=50)
opcion1.pack(side='bottom',padx=40,pady=40)
el=tk.Label(ventana,text='''The Legend of Zelda
The Way of the Triforce''',bg='black',fg='gold')
el.pack(padx=5,pady=5,ipadx=5,ipady=5,fill=tk.X)
ventana.mainloop()