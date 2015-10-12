__author__ = 'mohammad'

import random
from faker import Factory
from deap import base
from deap import creator
from deap import tools
from datetime import datetime,  timedelta
import struct
import time
from itertools import repeat
from collections import Sequence
"""
FIXED ATTRIBUTES
"""
MUTPB = 0.05
routeid = 5
#tripdurationinutes = 30
#buscapacity = 100

creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("Individual", list, fitness=creator.FitnessMin)

toolbox = base.Toolbox()

def strTimeProp(start, end, format, prop):
    """Get a time at a proportion of a range of two formatted times.

    start and end should be strings specifying times formated in the
    given format (strftime-style), giving an interval [start, end].
    prop specifies how a proportion of the interval to be taken after
    start.  The returned time will be in the specified format.
    """

    print start
    stime = time.mktime(time.strptime(start, format))
    etime = time.mktime(time.strptime(end, format))

    ptime = stime + prop * (etime - stime)

    return time.strftime(format, time.localtime(ptime))


def randomDate(start, end, prop):
    return strTimeProp(start, end, '%H:%M:%S', prop)

#print (randomDate("1/1/2015 1:00", "1/1/2015 12:00 AM", random.random()))

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
    #mutLocation = random.randint(0, len(individual)-1)
    mutLocation = 67
    print "Location indices ", mutLocation

    if not isinstance(low, Sequence):
        low = repeat(low, size)
    elif len(low) < size:
        raise IndexError("low must be at least the size of individual: %d < %d" % (len(low), size))
    if not isinstance(up, Sequence):
        up = repeat(up, size)
    elif len(up) < size:
        raise IndexError("up must be at least the size of individual: %d < %d" % (len(up), size))

    # Repairing the mutant
    timeDiff = datetime.strptime(randomDate("00:00:00", "23:59:00", random.random()),'%H:%M:%S')

    individual[mutLocation][2] = timeDiff.time().strftime('%H:%M:%S')
    
    #print (individual[mutLocation][2])

    individual[mutLocation][3] = (timeDiff + timedelta(0, 240)).time().strftime('%H:%M:%S')
    #print (individual[mutLocation][3])
    individual[mutLocation][4] = (timeDiff + timedelta(0, 480)).time().strftime('%H:%M:%S')
    #print (individual[mutLocation][4])
    individual[mutLocation][5] = (timeDiff + timedelta(0, 720)).time().strftime('%H:%M:%S')
    #print (individual[mutLocation][5])
    individual[mutLocation][6] = (timeDiff + timedelta(0, 960)).time().strftime('%H:%M:%S')
    #print (individual[mutLocation][6])

    '''
    for i, xl, xu in zip(range(size), low, up):
        if random.random() < indpb:
            individual[i] = strTimeProp(xl, xu, '%H:%M', random.random())
            #print(individual[i])
    '''

    #print individual
    return individual,

def getfakedata(NoOfBusStops):
    array = [0] * 7
    indx = 3
    faker = Factory.create()
    tripstartingtime1 = faker.time()

    tripstartingtimeObject = datetime.strptime(tripstartingtime1, '%H:%M:%S')
    tripstartingtime = tripstartingtimeObject.time()
    busid = random.randint(0,200)

    array[0] = 5
    array[1] = busid
    array[2] = tripstartingtime1

    for i in range(1,NoOfBusStops):
        nextTime = i * 4
        headway = tripstartingtimeObject + timedelta(minutes=nextTime)
        headwayTime = headway.strftime('%H:%M:%S')
        array[indx] = headwayTime
        indx = indx+1

    '''print ("this is result array")
    print(array)
    '''
    return array

IND_SIZE = 90
POP_SIZE = 1

creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", list, fitness=creator.FitnessMax)

toolbox = base.Toolbox()

toolbox.register("attribute", getfakedata, NoOfBusStops = 5 )
toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attribute, n=IND_SIZE)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)
toolbox.register("select", tools.selTournament, tournsize=3)

pop = toolbox.population(POP_SIZE)
def main():

    result = toolbox.individual()
    '''
    print ("inside the createindividual this is result \t")
    print(result)
    print len(result)
    print ("end of result \n")
    '''

    offspring = toolbox.select(pop, len(pop))
    offspring = list(map(toolbox.clone, offspring))

    '''
    print ("start offspring \t")
    print(offspring[0])
    print ("end offspring \t")
    '''
    toolbox.register("mutate", mutUniformTime, low=1, up=12, indpb=1)

    '''
    for mutant in offspring:
        if random.random() < 1:
            #print "Before \n"
            #print "\n"
            #print offspring[0][67]
            #print mutant
            #print "After \n"
            #print "\n"
            #toolbox.mutate(mutant)
            #print offspring[0][67]
            #del mutant.fitness.values
            '''

    '''
    for child1, child2 in zip(offspring[::2], offspring[1::2]):

            # cross two individuals with probability CXPB
                print(child1)
                print(child2)
                print("Mutation result ")
                print(toolbox.mate(child1[0],child2[0]))
                '''

main()

def timeDiff(time1, time2):
    FMT = '%H:%M:%S'
    return datetime.strptime(time1, FMT) - datetime.strptime(time2, FMT)

def evalIndividual(individual):
    ''' Evaluate an individual in the population. Based on how close the average bus request time is to the actual bus trip time.
    @param an individual in the population
    @return a summation of the difference between past past requests' average trip starting time and actual start time
    according to the evolving timetable.

    Lower values are better.
    '''

    avgBusRequestTime = ['03:52:00', '04:22:00', '04:52:00', '05:07:00', '05:22:00', '05:37:00', '05:52:00', '06:07:00',
            '06:22:00', '06:36:00', '06:47:00', '06:57:00','07:07:00', '07:17:00', '07:27:00', '07:37:00', '07:47:00',
            '07:57:00', '08:07:00', '08:17:00', '08:27:00', '08:37:00', '08:48:00', '09:00:00', '09:10:00', '09:20:00',
            '09:30:00', '09:40:00', '09:50:00', '10:00:00', '10:10:00', '10:20:00', '10:30:00', '10:40:00', '10:50:00',
            '11:00:00', '11:10:00', '11:20:00', '11:30:00', '11:40:00', '11:49:00', '11:59:00', '12:09:00', '12:19:00',
            '12:29:00', '12:39:00', '12:49:00', '12:59:00', '13:09:00', '13:19:00', '13:29:00', '13:39:00', '13:49:00',
            '13:59:00', '14:09:00', '14:19:00', '14:29:00', '14:39:00', '14:49:00', '14:58:00', '15:08:00', '15:18:00',
            '15:28:00', '15:38:00', '15:48:00', '15:58:00', '16:08:00', '16:18:00', '16:28:00', '16:38:00', '16:48:00',
            '16:58:00', '17:08:00', '17:18:00', '17:28:00', '17:38:00', '17:49:00', '18:00:00', '18:10:00', '18:20:00',
            '18:30:00', '18:40:00', '18:50:00', '19:00:00', '19:10:00', '19:30:00', '19:51:00', '20:11:00', '20:31:00',
            '20:51:00'] 

    # The least and most possible time timedelta values 
    timeDelta = timeDiff(individual[0][2], individual[0][2])
    minDiff = timedelta.max

    diffMinutes = 0
    print "...................############......................."

    for reqTime in avgBusRequestTime:
        for i in range(len(individual)):
            timeTableDiff = timeDiff(individual[i][2], reqTime)
            if timeTableDiff >= timedelta(minutes=0) and  timeTableDiff < minDiff:
                waitMin = individual[i][2]
                index = i
                minDiff = timeTableDiff
        print "Average req time (based on past requests)"
        print reqTime
        print "Best departure time"
        print waitMin
        print "Individual gene"
        print individual[index]
        diffMinutes += minDiff.total_seconds() / 60.0
        print diffMinutes
        minDiff = timedelta.max  # Reset minDiff for the next request time

    return diffMinutes,

print evalIndividual(pop[0])
