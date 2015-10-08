import random
from faker import Factory
from deap import base
from deap import creator
from deap import tools
from datetime import datetime, timedelta, date
import struct
import time
from itertools import repeat
from collections import Sequence

"""
FIXED ATTRIBUTES
"""
routeid = 5
tripdurationinutes = 30
buscapacity = 100


def strTimeProp(start, end, format, prop):
    """Get a time at a proportion of a range of two formatted times.

    start and end should be strings specifying times formated in the
    given format (strftime-style), giving an interval [start, end].
    prop specifies how a proportion of the interval to be taken after
    start.  The returned time will be in the specified format.
    """

    stime = time.mktime(time.strptime(start, format))
    etime = time.mktime(time.strptime(end, format))

    ptime = stime + prop * (etime - stime)

    return time.strftime(format, time.localtime(ptime))

def randomDate(start, end, prop):
    return strTimeProp(start, end, '%H:%M', prop)


def mutUniformTime(individual, low, up, indpb):
    """Mutate an individual by replacing attributes, with probability *indpb*,
    by a integer uniformly drawn between *low* and *up* inclusively.

    :param individual: :term:`Sequence <sequence>` individual to be mutated.
    :param low: The lower bound or a :term:`python:sequence` of
                of lower bounds of the range from wich to draw the new
                integer.
    :param up: The upper bound or a :term:`python:sequence` of
               of upper bounds of the range from wich to draw the new
               integer.
    :param indpb: Independent probability for each attribute to be mutated.
    :returns: A tuple of one individual.
    """
    size = len(individual)
    if not isinstance(low, Sequence):
        low = repeat(low, size)
    elif len(low) < size:
        raise IndexError("low must be at least the size of individual: %d < %d" % (len(low), size))
    if not isinstance(up, Sequence):
        up = repeat(up, size)
    elif len(up) < size:
        raise IndexError("up must be at least the size of individual: %d < %d" % (len(up), size))

    for i in range(len(individual)):
        individual[i] = randomDate("00:00", "23:59", random.random())

    '''
    for i, xl, xu in zip(range(size), low, up):
        if random.random() < indpb:
            individual[i] = strTimeProp(xl, xu, '%H:%M', random.random())
            #print(individual[i])
    '''

    return individual,


def createindividual():

    creator.create("FitnessMax", base.Fitness, weights=(1.0,))
    creator.create("Individual", list, fitness=creator.FitnessMax)

    IND_SIZE = 1
    POP_SIZE = 2

    toolbox = base.Toolbox()

    toolbox.register("attribute", getfakedata)
    toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attribute, n=IND_SIZE)


    toolbox.register("population", tools.initRepeat, list, toolbox.individual,  n=POP_SIZE)

    result = toolbox.population()
    toolbox.register("mate", tools.cxOnePoint)
    toolbox.register("mutate", mutUniformTime, low=1, up=12, indpb=1)



    #ind1 = toolbox.individual()
    #ind2 = toolbox.individual()

    #print ((toolbox.mate(ind1, ind2)))

#    print(result)
'''
    for bla in result:
        print (bla)
        print("\n")

'''
def getfakedata():

    array = []

    onetotwentyfour = range(1, 24)
    faker = Factory.create()
    tripstartingtime1 = faker.time()
    tripstartingtimeObject = datetime.strptime(tripstartingtime1, '%H:%M:%S')
    tripstartingtime = tripstartingtimeObject.time()

    busid = faker.building_number()
    array.append(tripstartingtime1)

    for i in onetotwentyfour:

        headway = tripstartingtimeObject + timedelta(hours=i)
        headwayTime = headway.strftime('%H:%M:%S')
        array.append(headwayTime)

    result = routeid, tripdurationinutes, buscapacity, busid, sorted(array)

    return result

createindividual()

# Individuals in the population
ind1 = [5, '03:52:00','03:56:00','04:00:00','04:05:00','04:15:00','04:19:00','04:25:00','04:31:00']
ind2 = [5, '04:22:00','04:26:00','04:30:00','04:35:00','04:45:00','04:49:00','04:55:00','05:01:00']
ind3 = [5, '04:52:00','04:56:00','05:00:00','05:05:00','05:15:00','05:19:00','05:25:00','05:31:00']
ind4 = [5, '05:07:00','05:11:00','05:15:00','05:20:00','05:30:00','05:34:00','05:40:00','05:46:00']
ind5 = [5, '05:22:00','05:26:00','05:30:00','05:35:00','05:45:00','05:49:00','05:55:00','06:01:00']
 

def timeDiff(time1, time2):
    FMT = '%H:%M:%S'
    diff = datetime.strptime(time1, FMT) - datetime.strptime(time2, FMT)
    return diff

def evalIndividual(individual):
    ''' Evaluate an individual in the population. Based on how close the average bus request time is to the actual bus trip time.
    Lower values are better.
    '''
    avgBusRequestTime = ['03:30:00', '03:45:00', '04:28:00', '05:05:00', '05:222:00']
    j = 0
    timeDelta = timeDiff(individual[1], individual[1])

    while (j < len(avgBusRequestTime) - 1) and timeDiff(individual[1], avgBusRequestTime[j]) > timeDelta:
        j += 1
        print j

    print timeDiff(individual[1], avgBusRequestTime[j])

evalIndividual(ind1)
