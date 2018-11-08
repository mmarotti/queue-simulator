# -*- coding: utf-8 -*-

from event import Event, Arrival, Exit
from element import Element
from termcolor import colored
import matplotlib.pyplot as plt

average_time_group = []
average_time_analitic_group = []
dropout_taxe_group = []
use_taxe_group = []
use_taxe_analitic_group = []
expected_number_of_elements_group = []
expected_number_of_elements_analitic_group = []

class Simulator:
    def __init__(self, queue_size, e_c, e_x):
        self.queue_size = queue_size
        self.e_c = e_c
        self.e_x = e_x
        self.progression = []

    def simulate(self, initial_event, simulation_time):
        self.time = 0
        self.num_arrivals=0
        self.events = [initial_event]
        self.queue = []
        self.processed_queue = []
        self.num_dropouts = 0
        self.simulation_time = simulation_time

        self.progression.append([len(self.queue), self.time])

        while(self.time <= simulation_time):
            if(self.events[0].__class__.__name__ == "Arrival"):
                self.time = self.events[0].time
                self.num_arrivals += 1
                if(len(self.queue) < self.queue_size):
                    self.queue.append(Element(self.time))
                    if(len(self.queue) == 1):
                        self.queue[0].start_processing = self.time
                    else:
                        self.progression.append([len(self.queue), self.time])
                else:
                    self.num_dropouts += 1
                self.events.pop(0)
                nex_arrival_event = Arrival(self.time)
                nex_arrival_event.generateTime(self.e_c)
                self.events.append(nex_arrival_event)
                if(len(self.queue) == 1):
                    nex_exit_event = Exit(self.time)
                    nex_exit_event.generateTime(self.e_x)
                    self.events.append(nex_exit_event)
            elif(self.events[0].__class__.__name__ == "Exit"):
                self.time = self.events[0].time
                self.queue[0].exit = self.time
                self.processed_queue.append(self.queue.pop(0))
                self.progression.append([len(self.queue), self.time])
                if(self.queue):
                    self.queue[0].start_processing = self.time
                self.events.pop(0)
                if(len(self.queue) > 0):
                    nex_exit_event = Exit(self.time)
                    nex_exit_event.generateTime(self.e_x)
                    self.events.append(nex_exit_event)
            self.events.sort(key=lambda x: x.time)
        print("-------------------------------------------")
        print(colored("| Número de chegadas: " + str(self.num_arrivals), "blue"))
        print(colored("| Número de atendimentos: " + str(len(self.processed_queue)), "green"))
        print(colored("| Número de desistências: " + str(self.num_dropouts), "red"))
        print("-------------------------------------------")

    def average_time(self):
        w = 0
        for element in self.processed_queue:
            w += element.exit - element.arrival
        print(colored("| Média de tempo na fila: " + str(w/len(self.processed_queue)), "magenta"))
        print("-------------------------------------------")

        average_time_group.append(w/len(self.processed_queue))
        return(w/len(self.processed_queue))

    def dropout_taxe(self):
        print (colored("| Taxa de desistência: " + str(float(self.num_dropouts)/self.num_arrivals), "yellow"))
        print("-------------------------------------------")

        dropout_taxe_group.append(float(self.num_dropouts)/self.num_arrivals)
        return float(self.num_dropouts)/self.num_arrivals

    def use_taxe(self):
        w = 0
        for element in self.processed_queue:
            w += element.exit - element.start_processing
        print(colored("| Taxa de utilização: " + str(w/self.time), "cyan"))
        print("-------------------------------------------")

        use_taxe_group.append(w/self.time)
        return (w/self.time)


    def expected_number_of_elements(self):
        integral = 0
        for i in range(len(self.progression)-1):
            delta = self.progression[i+1][1] - self.progression[i][1]
            integral += self.progression[i][0]*delta

        expected_number = integral/self.simulation_time
        print(colored("| Número Esperado de Elementos na Fila: " + str(expected_number), "blue"))
        print("-------------------------------------------")

        expected_number_of_elements_group.append(expected_number)
        return expected_number

    def analitical_calc(self):
        lamb = 1/self.e_c
        u = self.e_x * (lamb)
        e_w = self.e_x/(1 - u)
        e_n = u/(1 - u)

        average_time_analitic_group.append(e_w)
        use_taxe_analitic_group.append(u)
        expected_number_of_elements_analitic_group.append(e_n)

def console_title():
    print("##############################################################")
    print("#####                                                    #####")
    print("#####        SIMULADOR DE AVALIAÇÃO DE DESEMPENHO        #####")
    print("#####                       GRUPO:                       #####")
    print("#####   LUAN SIMÕES, MATHEUS MAROTTI E THIAGO DO PRADO   #####")
    print("#####                                                    #####")
    print("##############################################################")
    print()

def console_break_line():
    print()
    print("###################################################")
    print()

def test_generator(queue_size, e_c, e_x, simulation_time):
    teste = Simulator(queue_size, e_c, e_x)
    inicial = Arrival(0)
    teste.simulate(inicial, simulation_time)
    teste.average_time()
    teste.dropout_taxe()
    teste.use_taxe()
    teste.expected_number_of_elements()
    teste.analitical_calc()

def err_generator(info_array):
    err_array = []

    for i in info_array:
        err_array.append(0.05 * i)

    return err_array

def graph_one_bar_generator(info_array, name_array, label_x, label_y, title, color):
    barWidth = 0.5
    yerr = err_generator(info_array)
    position_array = range(1, len(info_array)+1)
    plt.bar(position_array, info_array, width = barWidth, color = color, edgecolor = 'black', yerr=yerr, capsize=7, label='experimentos')
    plt.plot(position_array, info_array, color = "black")

    if len(name_array) != 0:
        plt.xticks(position_array, name_array)
    else:
        plt.xticks(position_array, position_array)

    plt.xlabel(label_x)
    plt.ylabel(label_y)
    plt.title(title)

    plt.show()

def graph_two_bar_generator(info_array, analitical_array, name_array, label_x, label_y, title, color):
    barWidth = 0.3
    yerr = err_generator(info_array)
    position_array = range(1, len(info_array)+1)
    

    plt.bar(position_array, info_array, width = barWidth, color = color, edgecolor = 'black', yerr=yerr, capsize=7, label='experimentos')
    plt.plot(position_array, info_array, color = "black")
    plt.bar([position + barWidth for position in position_array], analitical_array, width = barWidth, color = "cyan", edgecolor = 'black', yerr=yerr, capsize=7, label='analítico')
    plt.plot([position + barWidth for position in position_array], analitical_array, color = "black")

    if len(name_array) != 0:
        plt.xticks(position_array, name_array)
    else:
        plt.xticks(position_array, position_array)

    plt.xlabel(label_x)
    plt.ylabel(label_y)
    plt.legend()
    plt.title(title)

    plt.show()

def examples():
    console_title()

    # Exemplo de execução
    test_generator(15, 0.1, 0.09, 3600)
    console_break_line()
    test_generator(15, 0.11, 0.09, 3600)
    console_break_line()
    test_generator(15, 0.12, 0.09, 3600)
    console_break_line()
    test_generator(15, 0.14, 0.09, 3600)
    console_break_line()
    test_generator(15, 0.16, 0.09, 3600)
    console_break_line()
    test_generator(15, 0.18, 0.09, 3600)
    console_break_line()
    test_generator(15, 0.20, 0.09, 3600)
    console_break_line()

    graph_two_bar_generator(average_time_group[0:7], average_time_analitic_group[0:7], [round(1/(0.10), 2), round(1/(0.11), 2), round(1/(0.12), 2), round(1/(0.14), 2), round(1/(0.16), 2), round(1/(0.18), 2), round(1/(0.20), 2)], "1/E[C]", "Média de tempo na fila", "Experimento 1/4", "red")
    graph_one_bar_generator(dropout_taxe_group[0:7], [round(1/(0.10), 2), round(1/(0.11), 2), round(1/(0.12), 2), round(1/(0.14), 2), round(1/(0.16), 2), round(1/(0.18), 2), round(1/(0.20), 2)], "1/E[C]", "Taxa de desistência", "Experimento 2/4", "red")
    graph_two_bar_generator(use_taxe_group[0:7], use_taxe_analitic_group[0:7], [round(1/(0.10), 2), round(1/(0.11), 2), round(1/(0.12), 2), round(1/(0.14), 2), round(1/(0.16), 2), round(1/(0.18), 2), round(1/(0.20), 2)], "1/E[C]", "Taxa de utilização", "Experimento 3/4", "red")
    graph_two_bar_generator(expected_number_of_elements_group[0:7], expected_number_of_elements_analitic_group[0:7], [round(1/(0.10), 2), round(1/(0.11), 2), round(1/(0.12), 2), round(1/(0.14), 2), round(1/(0.16), 2), round(1/(0.18), 2), round(1/(0.20), 2)], "1/E[C]", "Número esperado de elementos na fila", "Experimento 4/4", "red")

    # Exemplo extra
    for i in range(0,16):
        test_generator(15, 0.11, 0.09, 3600)
        console_break_line()

    graph_one_bar_generator(average_time_group[7:23], [], "Experimentos", "Média de tempo na fila", "Experimento Extra 1/4", "blue")
    graph_one_bar_generator(dropout_taxe_group[7:23], [], "Experimentos", "Taxa de desistência", "Experimento Extra 2/4", "blue")
    graph_one_bar_generator(use_taxe_group[7:23], [], "Experimentos", "Taxa de utilização", "Experimento Extra 3/4", "blue")
    graph_one_bar_generator(expected_number_of_elements_group[7:23], [], "Experimentos", "Número esperado de elementos na fila", "Experimento Extra 4/4", "blue")

examples()
