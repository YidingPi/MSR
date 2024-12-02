"""
This program processes score data extracted from two different datasets:
GitHub (GITHUB_OUTPUT_REFINED_SIMILARITY) and Software Heritage (SWH_OUTPUT_SIMILARITY).
The program performs the following tasks:
1. Reads and extracts scores and IDs from text files in the datasets.
2. Normalizes the data for neural network processing.
3. Trains a simple neural network to predict scores based on IDs.
4. Compares actual and predicted scores for both datasets.
5. Visualizes the data using scatter plots, distribution plots, and box plots.
6. Saves the visualizations to an analysis folder for further inspection.
"""
import os
import re
import torch
import torch.nn as nn
import torch.optim as optim
import matplotlib.pyplot as plt
import seaborn as sns  # For more aesthetically pleasing charts
import pandas as pd
os.makedirs(os.path.join('analysis', 'Similarity'), exist_ok=True)

folder_path = os.path.join('refined_data','GITHUB_OUTPUT_REFINED_SIMILARITY')  # Please replace with your actual folder path
file_list = os.listdir(folder_path)

scores = []
ids = []

# Regular expression used to extract ID
pattern = re.compile(r'\d+_(\d+)_.*\.txt')

for filename in file_list:
    filepath = os.path.join(folder_path, filename)
    match = pattern.match(filename)
    if match:
        id_num = int(match.group(1))
        ids.append(id_num)
        # Open file, read first line, extract Score
        with open(filepath, 'r', encoding='utf-8') as file:
            first_line = file.readline().strip()
            score_match = re.match(r'Score:\s*(\d+\.?\d*)', first_line)
            if score_match:
                score = float(score_match.group(1))
                scores.append(score)
            else:
                scores.append(0)
                print(f"File {filename} does not contain valid score information.")
    else:
        scores.append(0)
        print(f"Filename {filename} - score not found.")

# Check if data is complete
if len(ids) != len(scores):
    print("The number of IDs and scores do not match. Please check the data.")
    exit()

# Convert data to Pandas DataFrame for easier analysis
data = pd.DataFrame({
    'ID': ids,
    'Score': scores
})

# Data Normalization
ids_tensor = torch.tensor(ids, dtype=torch.float32).unsqueeze(1)
scores_tensor = torch.tensor(scores, dtype=torch.float32).unsqueeze(1)

ids_mean = ids_tensor.mean()
ids_std = ids_tensor.std()
ids_tensor_norm = (ids_tensor - ids_mean) / ids_std

scores_mean = scores_tensor.mean()
scores_std = scores_tensor.std()
scores_tensor_norm = (scores_tensor - scores_mean) / scores_std

# Build Neural Network Model
class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        self.fc = nn.Sequential(
            nn.Linear(1, 64),
            nn.ReLU(),
            nn.Linear(64, 1)
        )

    def forward(self, x):
        return self.fc(x)

model = Net()

# Define loss function and optimizer
criterion = nn.MSELoss()
optimizer = optim.Adam(model.parameters(), lr=0.01)

# Train the model
epochs = 1000
for epoch in range(epochs):
    model.train()
    optimizer.zero_grad()
    outputs = model(ids_tensor_norm)
    loss = criterion(outputs, scores_tensor_norm)
    loss.backward()
    optimizer.step()
    if (epoch + 1) % 100 == 0:
        print(f'Epoch {epoch + 1}, Loss: {loss.item():.4f}')

# Model Evaluation
model.eval()
with torch.no_grad():
    predicted_norm = model(ids_tensor_norm)
    # Denormalize
    predicted = predicted_norm * scores_std + scores_mean
    actual = scores_tensor

# Add predicted results to DataFrame
data['Predicted_Score'] = predicted.numpy().flatten()

# # Plot Actual Scores
# plt.figure(figsize=(10, 6))
# plt.scatter(data['ID'], data['Score'], label='Actual Score', color='blue')
# plt.xlabel('Student ID')
# plt.ylabel('Score')
# plt.title('Actual Scores')
# plt.legend()
# plt.grid(True)
# plt.show()
#
# # Plot Predicted Scores
# plt.figure(figsize=(10, 6))
# plt.scatter(data['ID'], data['Predicted_Score'], label='Predicted Score', color='orange')
# plt.xlabel('Student ID')
# plt.ylabel('Score')
# plt.title('Predicted Scores')
# plt.legend()
# plt.grid(True)
# plt.show()
#
# # Add Mathematical Analysis
#
# # 1. Distribution Plot
# plt.figure(figsize=(10, 6))
# sns.histplot(data['Score'], kde=True, color='blue', label='Actual Score')
#
# plt.xlabel('Score')
# plt.title('Score Distribution')
# plt.legend()
# plt.show()
#
# # 2. Box Plot
# plt.figure(figsize=(10, 6))
# sns.boxplot(data=data[['Score']], palette=['blue'])
# plt.ylabel('Score')
# plt.title('Score Box Plot')
# plt.show()
#
# # 3. Density Plot
# plt.figure(figsize=(10, 6))
# sns.kdeplot(data['Score'], shade=True, color='blue', label='Actual Score')
#
# plt.xlabel('Score')
# plt.title('Score Density Plot')
# plt.legend()
# plt.show()
#
# # Show all plots
# plt.show()

directory = os.path.join('refined_data','SWH_OUTPUT_SIMILARITY')   # Please replace with your actual folder path
files = os.listdir(directory)

score_list = []
student_ids = []

# Regular expression used to extract student number
regex = re.compile(r'\d+_(\d+)_.*\.txt')

for fname in files:
    full_path = os.path.join(directory, fname)
    match = regex.match(fname)
    if match:
        sid = int(match.group(1))
        student_ids.append(sid)
        # Read file, extract score
        with open(full_path, 'r', encoding='utf-8') as f:
            first_line = f.readline().strip()
            score_match = re.match(r'Score:\s*(\d+\.?\d*)', first_line)
            if score_match:
                sc = float(score_match.group(1))
                score_list.append(sc)
            else:
                score_list.append(0)
                print(f"File {fname} does not contain valid score information.")
    else:
        score_list.append(0)
        print(f"Filename {fname} - score not found.")

# Verify data integrity
if len(student_ids) != len(score_list):
    print("The number of student IDs and scores do not match. Please check the data.")
    exit()

# Create Pandas DataFrame
df = pd.DataFrame({
    'StudentID': student_ids,
    'ActualScore': score_list
})

# Data Standardization
id_tensor = torch.tensor(student_ids, dtype=torch.float32).unsqueeze(1)
score_tensor = torch.tensor(score_list, dtype=torch.float32).unsqueeze(1)

id_mean = id_tensor.mean()
id_std = id_tensor.std()
id_normalized = (id_tensor - id_mean) / id_std

score_mean = score_tensor.mean()
score_std = score_tensor.std()
score_normalized = (score_tensor - score_mean) / score_std


# Define Neural Network Structure
class ScorePredictor(nn.Module):
    def __init__(self):
        super(ScorePredictor, self).__init__()
        self.network = nn.Sequential(
            nn.Linear(1, 64),
            nn.ReLU(),
            nn.Linear(64, 1)
        )

    def forward(self, x):
        return self.network(x)


model = ScorePredictor()

# Set loss function and optimizer
loss_function = nn.MSELoss()
optimizer = optim.Adam(model.parameters(), lr=0.01)

# Train the model
num_epochs = 1000
for epoch in range(num_epochs):
    model.train()
    optimizer.zero_grad()
    predictions = model(id_normalized)
    loss = loss_function(predictions, score_normalized)
    loss.backward()
    optimizer.step()
    if (epoch + 1) % 100 == 0:
        print(f'Epoch {epoch + 1}, Loss: {loss.item():.4f}')

# Evaluate the model
model.eval()
with torch.no_grad():
    predicted_normalized = model(id_normalized)
    # Denormalize
    predicted_scores = predicted_normalized * score_std + score_mean
    actual_scores = score_tensor

# Add predicted results to DataFrame
df['PredictedScore'] = predicted_scores.numpy().flatten()

# Plot Actual Scores
plt.figure(figsize=(10, 6))
plt.scatter(df['StudentID'], df['ActualScore'], label='Github Score', color='blue')
plt.scatter(data['ID'], data['Score'], label='SWH Score', color='green')
plt.xlabel('Index')
plt.ylabel('Score')
plt.title('Actual Score')
plt.legend()
plt.grid(True)
plt.savefig(os.path.join('analysis', 'Similarity','actual_scores.png'))
plt.show()

# Plot Predicted Scores
plt.figure(figsize=(10, 6))
plt.scatter(df['StudentID'], df['PredictedScore'], label='Github Score', color='blue')
plt.scatter(data['ID'], data['Predicted_Score'], label='SWH Score', color='green')
plt.xlabel('Index')
plt.ylabel('Score')
plt.title('Predicted Score')
plt.legend()
plt.grid(True)
plt.savefig(os.path.join('analysis', 'Similarity','predicted_scores.png'))
plt.show()

# Add Data Analysis

# 1. Score Distribution Plot
plt.figure(figsize=(10, 6))
sns.histplot(df['ActualScore'], kde=True, color='blue', label='Github Score')
sns.histplot(data['Score'], kde=True, color='green', label='SWH Score')
plt.xlabel('Score')
plt.title('Score Distribution')
plt.legend()
plt.savefig(os.path.join('analysis','Similarity', 'score_distribution.png'))
plt.show()

# 2. Score Box Plot
plt.figure(figsize=(10, 6))
sns.boxplot(data=df[['ActualScore']], palette=['blue'])
sns.boxplot(data=data[['Score']], palette=['green'])
plt.ylabel('Score')
plt.title('Score Box Plot')
plt.savefig(os.path.join('analysis','Similarity', 'score_boxplot.png'))
plt.show()

# 3. Score Density Plot
# plt.figure(figsize=(10, 6))
# sns.kdeplot(df['ActualScore'], shade=True, color='blue', label='Actual Score')
# sns.kdeplot(data['Score'], shade=True, color='green', label='Actual Score')
#
# plt.xlabel('Score')
# plt.title('Score Density Plot')
# plt.legend()
# plt.show()

# Show all plots
#plt.show()


