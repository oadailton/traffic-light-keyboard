import time
import threading
import sys
import os
import platform
import atexit
import colorama
import win32con
import win32api
from cfonts import render
from colorama import Fore, Style

sistema_operacional = platform.system()
colorama.init(autoreset=True)
cor = "GREEN" #essa é a cor inicial
tempo: int = 2
corverde = 0x90 #codigo correspondente a tecla "num lock"
coramarelo = 0x14 #codigo correspondente a tecla "caps lock"
corvermelho = 0x91 #codigo correspondente a tecla "scroll lock"
semaforo = 0 #especifica em que estado está, 0 = verde, 1 = amarelo, 2 = vermelho, 3 = amarelo intermitente
tempoverde = 10 #tempo de duração do semáforo verde até o amarelo 
tempovermelho = 10 #tempo de duração do semáforo vermelho até o verde

class Restauraraosair:
    def __init__(self, numlock, capslock, scrolllock):
        self.numlock = numlock 
        self.capslock = capslock 
        self.scrolllock = scrolllock

    def recuperar(self):
        if win32api.GetKeyState(corvermelho) & 1 == 0 and self.scrolllock == 1:
            ativarteclado(corvermelho)
        elif win32api.GetKeyState(corvermelho) & 1 == 1 and self.scrolllock == 0:
            ativarteclado(corvermelho)
        if win32api.GetKeyState(corverde) & 1 == 0 and self.numlock == 1:
            ativarteclado(corverde)
        elif win32api.GetKeyState(corverde) & 1 == 1 and self.numlock == 0:
            ativarteclado(corverde)
        if win32api.GetKeyState(coramarelo) & 1 == 0 and self.capslock == 1:
            ativarteclado(coramarelo)
        elif win32api.GetKeyState(coramarelo) & 1 == 1 and self.capslock == 0:
            ativarteclado(coramarelo)

def limpar_console():  
    if sistema_operacional == 'Windows':
        os.system('cls')
        os.system('echo off')
        os.system('title Keyboard Traffic Light')
    elif sistema_operacional == 'Linux' or sistema_operacional == 'Darwin':
        os.system('clear')
        os.system('set +x')

def print_and_update(text,x): 
    y = getattr(Fore, x)
    limpar_console()    
    #sys.stdout.write(f"{y}{Style.BRIGHT}{text}{Style.RESET_ALL}")
    texto = f"{y}{Style.BRIGHT}{text}{Style.RESET_ALL}"
    #print(f.renderText(texto))
    if x == "GREEN": #tive que adaptar em if, pois por variável usando get.attr ou normal não ia de jeito nenhum
        output = render(text, colors=['green', 'yellow'], align='center')
    elif x == "YELLOW":
        output = render(text, colors=['yellow', 'yellow'], align='center')
    elif x == "RED":
        output = render(text, colors=['red', 'yellow'], align='center')
    else:
        output = render("ERROR", colors=['red', 'yellow'], align='center') 
    print(output)
    sys.stdout.flush()
    sys.stdout.write('\r')


def ativarteclado(codigo): 
    win32api.keybd_event(codigo, 0, 0, 0)
    win32api.keybd_event(codigo, 0, win32con.KEYEVENTF_KEYUP, 0)

def verde():
    global semaforo
    semaforo = 0
    if win32api.GetKeyState(corverde) & 1 == 0:
        ativarteclado(corverde)
    if win32api.GetKeyState(coramarelo) & 1 == 1:
        ativarteclado(coramarelo)
    if win32api.GetKeyState(corvermelho) & 1 == 1:
        ativarteclado(corvermelho)
    
    
def amarelo(piscante):
    global semaforo
    if piscante == 0:
        semaforo = 1
    if piscante == 1:
        semaforo = 3
    if win32api.GetKeyState(coramarelo) & 1 == 0 or piscante == 1:
        ativarteclado(coramarelo)
    if win32api.GetKeyState(corverde) & 1 == 1:
        ativarteclado(corverde)
    if win32api.GetKeyState(corvermelho) & 1 == 1:
        ativarteclado(corvermelho)
    
def vermelho():
    global semaforo
    semaforo = 2
    if win32api.GetKeyState(corvermelho) & 1 == 0:
        ativarteclado(corvermelho)
    if win32api.GetKeyState(corverde) & 1 == 1:
        ativarteclado(corverde)
    if win32api.GetKeyState(coramarelo) & 1 == 1:
        ativarteclado(coramarelo)


def forcarativacaodesativacao(x):
    if x == 0:
        verde()
    elif x == 1:
        amarelo(0)
    elif x == 2:
        vermelho()

def semaforowork():
    global semaforo, tempo, cor, tempoverde, tempovermelho
    tempo = tempo - 1 #ele reduz o tempo de semaforo a cada um segundo
    forcarativacaodesativacao(semaforo)
    if semaforo == 0 and tempo == 0:
        tempo = 5 #retoma o tempo 
        amarelo(0) #escolhe qual semaforo ser ativo
        cor = "YELLOW"
    elif semaforo == 1 and tempo == 0:
        tempo = tempovermelho
        vermelho()
        cor = "RED"
    elif semaforo == 2 and tempo == 0:
        tempo = tempoverde
        verde()
        cor = "GREEN"
    elif semaforo > 2 and tempo == 0:
        amarelo(1)
        tempo = 1
        cor = "YELLOW"
    if semaforo < 3:
        print_and_update(str(tempo).zfill(2), cor) #atualiza o cronômetro digital
    else: 
        if win32api.GetKeyState(coramarelo) == 1:
            limpar_console()
            output = render("CAUTION", colors=['yellow', 'yellow'], align='center') 
            print(output)
        else:
            limpar_console()
            output = render("CAUTION", colors=['black', 'yellow'], align='center') 
            print(output)
    timer = threading.Timer(1, semaforowork)
    timer.start() 

def escolhatempov():
    global tempoverde, tempovermelho
    escolhatempoverde = input("For how long should the traffic light stay green? Choose a duration between 5 and 90 seconds.")
    if escolhatempoverde.isdigit():
        if 4 < int(escolhatempoverde) < 91:
            tempoverde = int(escolhatempoverde)
            limpar_console()
            escolhatempovermelho = input("For how long should the traffic light stay red? Choose a duration between 5 and 90 seconds.")
            if escolhatempovermelho.isdigit():
                if 4 < int(escolhatempovermelho) < 91:
                    tempovermelho = int(escolhatempovermelho)
                    limpar_console()
                    semaforowork()
                else:
                    print("Write a number from 5-90, no names or other characters")
                    escolhatempov()
            else:
                print("Write a number from 5-90, no names or other characters")
                escolhatempov()
        else:
            print("Write a number between 5 and 90, excluding values less than 5 or greater than 90.")
            escolhatempov()
    else:
        print("Write a number from 5-90, no names or other characters")
        escolhatempov()

def titlescreen():
    global tecladoinicial
    limpar_console()
    tecladoinicial = Restauraraosair(win32api.GetKeyState(corverde), win32api.GetKeyState(coramarelo), win32api.GetKeyState(corvermelho)) #Acionando essa função ao sair, ele manterá as teclas ativas do mesmo jeito quando iniciou
    output = render("Keyboard Traffic Light \r\n by Adailton", colors=['blue', 'yellow'], align='left') 
    print(output)
    time.sleep(2.5)
    ligarsemaforo()

def ligarsemaforo():
    global semaforo
    if sistema_operacional == 'Windows':
        os.system('title Keyboard Traffic Light')
    limpar_console()
    tipo = input("Which traffic light mode would you like: normal (0) or flashing yellow (1)?")
    if tipo == "0":
        semaforo = 0
        limpar_console()
        escolhatempov()
    elif tipo == "1":
        semaforo = 3
        tempo: 1
        limpar_console()
        semaforowork()
    else:
        print("You got it wrong.")
        ligarsemaforo()

@atexit.register
def hastalavistababy():
    global tecladoinicial
    tecladoinicial.recuperar()
    limpar_console() 
    output = render("thank you, and drive safely!", colors=['blue', 'yellow'], align='center') 
    print(output)

titlescreen() #é aqui que a festa começa
