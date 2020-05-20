import csv
import sys

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data(sys.argv[1])
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

    # Train model and make predictions
    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)
    sensitivity, specificity = evaluate(y_test, predictions)

    # Print results
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")


def load_data(filename):
    """
    Load shopping data from a CSV file `filename` and convert into a list of
    evidence lists and a list of labels. Return a tuple (evidence, labels).

    evidence should be a list of lists, where each list contains the
    following values, in order:
        - Administrative, an integer
        - Administrative_Duration, a floating point number
        - Informational, an integer
        - Informational_Duration, a floating point number
        - ProductRelated, an integer
        - ProductRelated_Duration, a floating point number
        - BounceRates, a floating point number
        - ExitRates, a floating point number
        - PageValues, a floating point number
        - SpecialDay, a floating point number
        - Month, an index from 0 (January) to 11 (December)
        - OperatingSystems, an integer
        - Browser, an integer
        - Region, an integer
        - TrafficType, an integer
        - VisitorType, an integer 0 (not returning) or 1 (returning)
        - Weekend, an integer 0 (if false) or 1 (if true)

    labels should be the corresponding list of labels, where each label
    is 1 if Revenue is true, and 0 otherwise.
    """
    return_value = tuple()
    evidence = list()
    labels = list()

    with open(filename) as csvfile:
        filereader = csv.DictReader(csvfile)
        for row in filereader:
            evidence_row = list()
            evidence_row.append(int(row['Administrative']))
            evidence_row.append(float(row['Administrative_Duration']))
            evidence_row.append(int(row['Informational']))
            evidence_row.append(float(row['Informational_Duration']))
            evidence_row.append(int(row['ProductRelated']))
            evidence_row.append(float(row['ProductRelated_Duration']))
            evidence_row.append(float(row['BounceRates']))
            evidence_row.append(float(row['ExitRates'])) 
            evidence_row.append(float(row['PageValues']))
            evidence_row.append(float(row['SpecialDay']))
            if row['Month'] == 'Jan':
                month = 0
            elif row['Month'] == 'Feb':
                month = 1
            elif row['Month'] == 'Mar':
                month = 2
            elif row['Month'] == 'Apr':
                month = 3
            elif row['Month'] == 'May':
                month = 4
            elif row['Month'] == 'Jun':
                month = 5
            elif row['Month'] == 'Jul':
                month = 6
            elif row['Month'] == 'Aug':
                month = 7
            elif row['Month'] == 'Sep':
                month = 8
            elif row['Month'] == 'Oct':
                month = 9
            elif row['Month'] == 'Nov':
                month = 10
            elif row['Month'] == 'Dec':
                month = 11       
            evidence_row.append(month)
            evidence_row.append(int(row['OperatingSystems']))
            evidence_row.append(int(row['Browser']))
            evidence_row.append(int(row['Region']))
            evidence_row.append(int(row['TrafficType']))
            if row['VisitorType'] == 'Returning_Visitor':
                Visitor = 1
            else:
                Visitor = 0
            evidence_row.append(Visitor) 
            if row['Weekend'] == 'FALSE':
                Weekend = 0
            else:
                Weekend = 1
            evidence_row.append(Weekend)

            if row['Revenue'] == 'TRUE':
                Revenue = 1
            else:
                Revenue = 0
            labels.append(Revenue)

            evidence.append(evidence_row)

    
    return_value = (evidence, labels)
    
    return return_value


def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """
    model = KNeighborsClassifier(n_neighbors=1)
    model.fit(evidence, labels)

    return model


def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificty).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """
    return_tuple = tuple()

    

    positive = 0
    correct_positives = 0

    for i in range(0, len(labels)):
        if labels[i] == 1:
            positive += 1
        if labels[i] == 1 and predictions[i] == 1:
            correct_positives += 1
    
    sensitivity = correct_positives / positive

    negative = 0
    correct_negatives = 0

    for i in range(0, len(labels)):
        if labels[i] == 0:
            negative += 1
        if labels[i] == 0 and predictions[i] == 0:
            correct_negatives += 1
    
    specificity = correct_negatives / negative

    return_tuple = (sensitivity,specificity)
    
    return return_tuple


if __name__ == "__main__":
    main()
