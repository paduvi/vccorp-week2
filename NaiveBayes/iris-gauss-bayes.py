import tensorflow as tf
import DataUtils
import numpy as np
import random
import math


def calculateProbability(x, mean, stdev):
    exponent = math.exp(-(math.pow(x - mean, 2) / (2 * math.pow(stdev, 2))))
    return exponent / (math.sqrt(2 * math.pi) * stdev)


def calculateClassProbabilities(summaries, inputVector):
    probabilities = {}
    for classValue, classSummaries in summaries.iteritems():
        probabilities[classValue] = 1
        mean = classSummaries["mean"]
        stdev = classSummaries["std"]
        for i in range(len(mean)):
            probabilities[classValue] *= calculateProbability(inputVector[i], mean[i], stdev[i])
    return probabilities


def predict(summaries, inputVector):
    probabilities = calculateClassProbabilities(summaries, inputVector)
    bestLabel, bestProb = None, -1
    for classValue, probability in probabilities.iteritems():
        if bestLabel is None or probability > bestProb:
            bestProb = probability
            bestLabel = classValue
    return bestLabel


def getPredictions(summaries, testSet):
    predictions = []
    for i in range(len(testSet)):
        result = predict(summaries, testSet[i])
        predictions.append(result)
    return predictions


def getAccuracy(testSet, predictions):
    correct = 0
    for i in range(len(testSet)):
        if testSet[i][-1] == predictions[i]:
            correct += 1
    return (correct / float(len(testSet))) * 100.0


if __name__ == '__main__':
    input_data, output_data = DataUtils.load_data("iris.txt")
    z = zip(input_data, output_data)
    random.shuffle(z)

    input_data, output_data = zip(*z)

    training_data = input_data[:80]
    label_data = output_data[:80]

    test_input_data = input_data[-20:]
    test_label_data = output_data[-20:]

    # print test_input_data.shape

    # Iris-setosa: 1
    # Iris-versicolor: 2
    # Iris-virginica: 3

    labels = {
        1: 'Iris-setosa',
        2: 'Iris-versicolor',
        3: 'Iris-virginica'
    }

    separated = {}

    for i in range(80):
        classValue = int(label_data[i][0])
        if classValue not in separated:
            separated[classValue] = []
        separated[classValue].append(training_data[i])

    separated = {classValue: np.asarray(instances) for classValue, instances in separated.iteritems()}

    summaries = {}
    for classValue, instances in separated.iteritems():
        summaries[classValue] = {
            "mean": np.mean(instances, axis=0),
            "std": np.std(instances, axis=0)
        }

    # test model
    predictions = getPredictions(summaries, test_input_data)
    accuracy = getAccuracy(test_label_data, predictions)
    print('\nAccuracy: {0}%').format(accuracy)

    print '\n' + '=' * 20 + '\n'
    inputVector = [6.1, 2.9, 4.5, 1.3]
    predict_label = predict(summaries, inputVector)
    probabilities = calculateClassProbabilities(summaries, inputVector)
    print ('Input vector: {0}').format(inputVector)
    print ('Probabilities for each class: {0}').format(probabilities)
    print ('Predict Class: {0} - {1}\n').format(predict_label, labels[predict_label])
