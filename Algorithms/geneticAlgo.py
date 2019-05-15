import random
import math
from algorithms import randomAlgo as ra
from classes import trainlining
from classes import trajectory
from algorithms import hillclimberAlgo as ha

def genetic(trainlining,railroad):
    populationSize = 40
    generations = 1000
    recombinationCoefficient = 0.5
    mutationRate = 1
    population = makePopulation(trainlining, populationSize, railroad)
    highestScore = 0
    besttrainlining = []
    counter = 0

    for i in range(generations):
        counter += 1
        scores = scorePopulation(trainlining, population)
        standardizedScores = standardize(scores)
        probabilityScores = calculateProbabilities(standardizedScores, population)
        mutatedChildren = []
        mutatedchildrenscore = 0
        for j in range(populationSize):
            number = 2
            parents = chooseParents(population, probabilityScores, number)
            crossoverChild = crossover(parents, recombinationCoefficient)
            mutatedChild = mutate(crossoverChild, railroad, trainlining, mutationRate)
            trainlining.trajectories = mutatedChild
            mutatedChildScore = trainlining.calculateScore()
            mutatedchildrenscore += mutatedChildScore

            if mutatedChildScore > highestScore:
                highestScore = mutatedChildScore
                besttrainlining = mutatedChild
            mutatedChildren.append(mutatedChild)

        newPopulation = tournament(trainlining, population, mutatedChildren)

        if (counter % 100) == 0:
            print(f"counter: {counter} score: {highestScore}")
            trainlining.trajectories = besttrainlining
            trainlining.calculateScore()
            print(len(trainlining.visitedCriticalConnections))

            sum = 0
            for individual in newPopulation:
                trainlining.trajectories = individual
                score = trainlining.calculateScore()
                sum += score
            print(sum/len(newPopulation))

            # print(mutatedchildrenscore/ 10))
            # sum = 0
            # for child in mutatedChildren:
            #     sum += int(len(child))
            # print(sum/len(mutatedChildren))

        population = newPopulation
    trainlining.trajectories = besttrainlining
    for trajectory in trainlining.trajectories:
        print(trajectory.visitedStations)



def makePopulation(trainlining, populationSize, railroad):
    populationList = []
    for i in range(populationSize):
        individual = []
        for i in range(trainlining.maxTrajectories):
            trajectory = ra.make_random_route(railroad, trainlining.maxLength)
            individual.append(trajectory)
        populationList.append(individual)

    return populationList

def scorePopulation(trainlining, population):
    scoreList = []
    for individual in population:
        trainlining.trajectories = individual
        score = trainlining.calculateScore()
        scoreList.append(score)
    return(scoreList)

def standardize(scores):
    lowScore = 10000
    for score in scores:
        if score < lowScore:
            lowScore = score

    standardizedScores = []
    for score in scores:
        standardizedScore = score - lowScore
        standardizedScores.append(standardizedScore)

    return standardizedScores

def calculateProbabilities(standardizedScores, population):
    scoreSum = 0
    for score in standardizedScores:
        scoreSum += score

    probabilities = []
    for score in standardizedScores:
        probability = score/scoreSum
        probabilities.append(probability)

    return probabilities


def chooseParents(population, probabilityScores, number):
    mergedList = list(zip(population, probabilityScores))
    r = random.random()
    ParentsTrajectories = []
    for i in range(int(number)):
        for (possibleParent, probability) in mergedList:
            if r < probability:
                ParentsTrajectories.append(possibleParent)
                break
            else:
                r -= probability

    return ParentsTrajectories

def tournament(trainlining, parentpopulation, mutatedchildren):
    participants = []
    participants += parentpopulation
    participants += mutatedchildren
    newpopulation = []
    while len(participants) > 0:
        participant1 = random.choice(participants)
        trainlining.trajectories = participant1
        score1 = trainlining.calculateScore()
        participants.remove(participant1)
        participant2 = random.choice(participants)
        participants.remove(participant2)
        trainlining.trajectories = participant2
        score2 = trainlining.calculateScore()

        if score1 > score2:
            newpopulation.append(participant1)
        else:
            newpopulation.append(participant2)

    return newpopulation

def crossover(parents, recombinationCoefficient):
    r = random.randint(0,1)
    length = int(len(parents[r])-(len(parents[r]) * recombinationCoefficient))

    child = []
    child += addCrossoverChild(int(len(parents[r]) - length), parents[r])

    if r == 1:
        child += addCrossoverChild(length, parents[0])
    else:
        child += addCrossoverChild(length, parents[1])

    return child

def addCrossoverChild(length, parent):
    child = []
    for i in range(length):
        trajectory = random.choice(parent)
        while trajectory in child:
            trajectory = random.choice(parent)
            break
        child.append(trajectory)

    return child

def mutate(crossoverChild, railroad, trainlining, mutationRate):
    trainlining.trajectories = crossoverChild
    for i in range(mutationRate):
        ha.hillclimber(trainlining, railroad)
    mutatedChild = trainlining.trajectories

    return mutatedChild

def mutate2(crossoverChild,railroad, trainlining, mutationRate):
    r = random.randint(1,3)
    if r == 1:
        crossoverChild.remove(random.choice(crossoverChild))

    elif r == 2 and len(crossoverChild) < 20:
        crossoverChild.append(make_random_route(railroad, trainlining.maxLength))

    else:
        crossoverChild.remove(random.choice(crossoverChild))
        crossoverChild.append(make_random_route(railroad, trainlining.maxLength))

    return crossoverChild
