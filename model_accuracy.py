import pandas as pd
import pickle
import json
from classify import classify_sentence_test
from sklearn.metrics import accuracy_score, confusion_matrix, precision_score, recall_score, f1_score
import matplotlib.pyplot as plt
import seaborn as sns

with open('updatedlda_model.pkl', 'rb') as f:
    lda = pickle.load(f)

with open('labeled_questions.json', 'r') as json_file:
    labeled_questions = json.load(json_file)

predicted_labels = []
true_labels = []

for question_info in labeled_questions:
    question = question_info['question']
    is_space_related = classify_sentence_test(question)
    predicted_labels.append(is_space_related)
    true_labels.append(question_info['is_space_related'])

accuracy = accuracy_score(true_labels, predicted_labels)
precision = precision_score(true_labels, predicted_labels)
recall = recall_score(true_labels, predicted_labels)
f1 = f1_score(true_labels, predicted_labels)

print("Accuracy:", accuracy)
print("Precision:", precision)
print("Recall:", recall)
print("F1 Score:", f1)

space_count = sum(true_labels)
non_space_count = len(true_labels) - space_count

labels = ['Space-Related', 'Non-Space-Related']
values = [accuracy * space_count, (1 - accuracy) * non_space_count]

plt.bar(labels, values, color=['blue', 'red'])
plt.xlabel('Question Type')
plt.ylabel('Number of Questions')
plt.title('Accuracy of LDA Model on Space Classification')
plt.ylim(0, max(values) + 10)

for i, value in enumerate(values):
    plt.text(i, value + 1, f"{value:.0f}", ha='center')

plt.show()

confusion = confusion_matrix(true_labels, predicted_labels)

plt.figure(figsize=(8, 6))
sns.heatmap(confusion, annot=True, fmt="d", cmap="Blues", xticklabels=["Non-Space", "Space"], yticklabels=["Non-Space", "Space"])
plt.xlabel("Predicted")
plt.ylabel("True")
plt.title("Confusion Matrix")
plt.legend(['True Class', 'Predicted Class'], loc='upper right')
plt.show()
