# -*- coding: utf-8 -*-

from event import Event, Arrival, Exit
from element import Element
from termcolor import colored

class Simulator:
    def __init__(self, queue_size, lamb, lamb_server):
        self.queue_size = queue_size
        self.lamb = lamb
        self.lamb_server = lamb_server
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
                    if(self.num_arrivals == 1):
                        self.queue[0].start_processing = self.time
                    else:
                        self.progression.append([len(self.queue), self.time])
                else:
                    self.num_dropouts += 1
                self.events.pop(0)
                nex_arrival_event = Arrival(self.time)
                nex_arrival_event.generateTime(self.lamb)
                self.events.append(nex_arrival_event)
                if(len(self.queue) == 1):
                    nex_exit_event = Exit(self.time)
                    nex_exit_event.generateTime(self.lamb_server)
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
                    nex_exit_event.generateTime(self.lamb_server)
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
        return(w/len(self.processed_queue))

    def dropout_taxe(self):
        print (colored("| Taxa de desistência: " + str(float(self.num_dropouts)/self.num_arrivals), "yellow"))
        print("-------------------------------------------")
        return float(self.num_dropouts)/self.num_arrivals

    def use_taxe(self):
        w = 0
        for element in self.processed_queue:
            w += element.exit - element.start_processing
        print(colored("| Taxa de utilização: " + str(w/self.simulation_time), "cyan"))
        print("-------------------------------------------")
        return (w/self.simulation_time)


    def expected_number_of_elements(self):
        integral = 0
        for i in range(len(self.progression)-1):
            delta = self.progression[i+1][1] - self.progression[i][1]
            integral += self.progression[i][0]*delta

        expected_number = integral/self.simulation_time
        print(colored("| Número Esperado de Elementos na Fila: " + str(expected_number), "blue"))
        print("-------------------------------------------")
        return expected_number




teste = Simulator(15, 60, 20)
inicial = Arrival(0)
teste.simulate(inicial, 20)
teste.average_time()
teste.dropout_taxe()
teste.use_taxe()
teste.expected_number_of_elements()