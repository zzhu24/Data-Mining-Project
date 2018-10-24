"""
Name: Zhiyu Zhu
NetID: zzhu24
"""

"""
Used Python3 in this file:
Command Used as:
python3 RandomForest.py training-file test-file

"""

"""
Used the structure of Binary Tree!!!!
"""



import os
import sys
import time
import random
import threading
from collections import Counter


def single_gini(training_set, count):
    temp = 0
    for i in range(len(training_set)):
        if training_set[i][0] == str((count + 1)):
            temp = temp + 1
    return temp

def gini_index(training_set, total_class):
    whole_gini = []
    for i in range(total_class):
        single_gini_value = single_gini(training_set, i)
        temp_gini = (single_gini_value / len(training_set)) ** 2
        whole_gini.append(temp_gini)
    gini_result = 1 - sum(whole_gini)
    return gini_result

def find_gini(branch, len_data, total_class):
    if len(branch) != 0:
        branch_gini = len(branch) / len_data * gini_index(branch, total_class)
        return branch_gini
    else:
        return 0

def attribute_split(training_set, attribute, total_class):
    current_gini = float('inf')
    current_attribute = ''

    has_attribute = []
    not_for_attribute = []

    for i in range(0, len(attribute)):
        first = []
        second = []
        for j in range(0, len(training_set)):
            if attribute[i] in training_set[j]:
                first.append(training_set[j])
            else:
                second.append(training_set[j])

        gini = 0
        if len(training_set) != 0:
            left_gini = find_gini(first, len(training_set), total_class)
            right_gini = find_gini(second, len(training_set), total_class)
            gini = left_gini + right_gini

        if gini < current_gini:
            # update
            current_gini = gini
            current_attribute = attribute[i]
            has_attribute = first
            not_for_attribute = second

    return current_attribute, has_attribute, not_for_attribute


def majority_vote(training_set, total_class):
    count = []
    for i in range(total_class):
        count.append(0)
    for i in range(0, len(training_set)):
        temp = int(training_set[i][0]) - 1
        count[temp] += 1
    best = str((count.index(max(count))) + 1)
    return best


def all_samle_attribute(training_set):
    temp = training_set[0][0]
    for i in range(0, len(training_set)):
        if temp != training_set[i][0]:
            return False
    return True


class Trees(object):
    def __init__(self):
        self.decision = None
        self.attribute = None
        self.right_tree = None
        self.left_tree = None


def stop_splitting(training_set, attribute, total_class, tree):
    if len(training_set) == 0:
        tree.decision = '1'
        return True

    if len(attribute) == 0:
        tree.decision = majority_vote(training_set, total_class)
        return True

    if all_samle_attribute(training_set) == True:
        tree.decision = training_set[0][0]
        return True

def Tree_Construction(training_set, attribute, total_class):
    tree = Trees()
    
    to_stop = stop_splitting(training_set, attribute, total_class, tree)
    if to_stop:
        return tree
    
    tree.right_tree = None
    tree.left_tree = None

    attr, data_a, data_b = attribute_split(training_set, attribute, total_class)

    attribute_right = []
    for i in range(0, len(attribute)):
        if attribute[i] != attr:
            need_attribute = attribute[i]
            attribute_right.append(need_attribute)

    attribute_left = []
    for i in range(0, len(attribute)):
        if attr[0:2] not in attribute[i]:
            need_attribute = attribute[i]
            attribute_left.append(need_attribute)

    tree.attribute = attr
    tree.left_tree = Tree_Construction(data_a, attribute_left, total_class)
    tree.right_tree = Tree_Construction(data_b, attribute_right, total_class)


    return tree


def find_all_attribute(data):
    all_attribute = []
    for temp_data in data:
        for i in range(1, len(temp_data)):
            all_attribute.append(temp_data[i])
    all_attribute = list(set(all_attribute))
    return all_attribute



def predict_single(root, temp_data):
    tree = root
    while tree.decision == None:
        if tree.attribute in temp_data:
            tree = tree.left_tree
        else:
            tree = tree.right_tree
    return tree.decision


def predict_result(test, root):
    total_right = 0
    predicted = []
    for temp_data in test:
        if int(temp_data[0]) == int(predict_single(root, temp_data)):
            total_right += 1
        predicted.append(predict_single(root, temp_data))
    return predicted, total_right/len(test)



def random_data(data, len_chosen):
    chosen_data = []
    for i in range(0, len_chosen):
        chosen_data.append(random.choice(data))
    return chosen_data





"""
Take in parameter
"""
if len(sys.argv) != 3:
    print("Incorrect input format")

argv2 = sys.argv[1]
argv3 = sys.argv[2]


"""
python3 DecisionTree.py balance.scale.train balance.scale.test
"""
if (argv2 == 'balance.scale.train'):
    dir = os.path.dirname(__file__)
    trainfile_path = os.path.join(dir, 'balance.scale.train')
    testfile_path = os.path.join(dir, argv3)
    training_file = open(trainfile_path, 'r')
    testing_file = open(testfile_path, 'r')

    total_class = 3
    attribute_proportion = 1
    thread_num = 30
    bagging_proportion = 0.1

"""
python3 DecisionTree.py led.train led.test
"""
if (argv2 == 'led.train'):
    dir = os.path.dirname(__file__)
    trainfile_path = os.path.join(dir, 'led.train')
    testfile_path = os.path.join(dir, argv3)
    training_file = open(trainfile_path, 'r')
    testing_file = open(testfile_path, 'r')

    total_class = 2
    attribute_proportion = 1
    thread_num = 4
    bagging_proportion = 0.5

"""
python3 DecisionTree.py nursery.train nursery.test
"""
if (argv2 == 'nursery.train'):
    dir = os.path.dirname(__file__)
    trainfile_path = os.path.join(dir, 'nursery.train')
    testfile_path = os.path.join(dir, argv3)
    training_file = open(trainfile_path, 'r')
    testing_file = open(testfile_path, 'r')

    total_class = 5
    attribute_proportion = 1
    thread_num = 10
    bagging_proportion = 0.5

"""
python3 DecisionTree.py synthetic.social.train synthetic.social.test
"""
if (argv2 == 'synthetic.social.train'):
    dir = os.path.dirname(__file__)
    trainfile_path = os.path.join(dir, 'synthetic.social.train')
    testfile_path = os.path.join(dir, argv3)
    training_file = open(trainfile_path, 'r')
    testing_file = open(testfile_path, 'r')

    total_class = 4
    attribute_proportion = 0.2
    thread_num = 100
    bagging_proportion = 0.1








lock = threading.Lock()
true_prediction = []


class myThread(threading.Thread):
    def __init__(self, threadId, num_class, data, test):
        threading.Thread.__init__(self)
        self.threadId = threadId
        self.num_class = num_class
        self.data = data
        self.test = test
        
    def run(self):
        pred_list = []

        attributes = find_all_attribute(self.data)
        attri_prune = random_data(attributes, int(len(attributes) * attribute_proportion))
        root = Tree_Construction(self.data, attri_prune, self.num_class)
        predictions, accuracy = predict_result(self.test, root)
        pred_list.append(predictions)

        lock.acquire()
        true_prediction.append(pred_list[0])
        lock.release()




all_threads = []


"""
Set all the data:
"""
training_data = training_file.readlines()
testing_data = testing_file.readlines()
for_training = []
for_testing = []
for temp_line in training_data:
    for_training.append(temp_line.split())

for temp_line in testing_data:
    for_testing.append(temp_line.split())




"""
Main Function:
"""

start_time = time.time()

all_data = []
sample_length = int(len(for_training) * bagging_proportion)

for i in range(thread_num):
    all_data.append(random_data(for_training, sample_length))
    thread = myThread(i, total_class, all_data[i], for_testing)
    thread.start()
    all_threads.append(thread)

for i in range(0, len(all_threads)):
    all_threads[i].join()

actual = [for_testing[i][0] for i in range(len(for_testing))]


final_predictions = []
for i in range(0, len(true_prediction[0])):
    x = [true_prediction[j][i] for j in range(len(true_prediction))]
    x = Counter(x).most_common()
    final_predictions.append(x[0][0])



"""
Print the matrix
"""
matrix = []
for i in range(total_class):
    matrix.append([0] * total_class)

for i in range(len(actual)):
    matrix[int(actual[i]) - 1][int(final_predictions[i]) - 1] += 1

for i in range(total_class):
    line = ''
    for j in range(total_class):
        line += str(matrix[i][j]) + ' '
    print(line)


"""
Print the tree and time
"""
correct_num = sum([final_predictions[i] == actual[i] for i in range(len(actual))])
accuracy = correct_num  / len(actual)
print("Total accuracy rate : " + str(accuracy))
total_time = time.time() - start_time
print("Time used  = ", (total_time), " seconds ")








