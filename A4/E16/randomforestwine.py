from sklearn.datasets import load_wine
from sklearn.ensemble import RandomForestClassifier
import pandas as pd
import numpy as np

np.random.seed(42)

dimensions = 13

# Load data
wine = load_wine()
print(wine.feature_names)
df = pd.DataFrame(wine.data, columns=wine.feature_names)

# Set class
df['class'] = pd.Categorical.from_codes(wine.target, wine.target_names)

# Split train and test into two groups of approximately 3/4 and 1/4 size
df['is_train'] = np.random.uniform(0, 1, len(df)) < 0.75
train, test = df[df['is_train'] == True], df[df['is_train'] == False]

# Assign features
features = df.columns[:dimensions]

# Factorize to numbers
y = pd.factorize(train['class'])[0]

# Train classifier
rf_classifier = RandomForestClassifier(n_jobs=-1, n_estimators=6, random_state=42)
rf_classifier.fit(train[features], y)

# Predict test set
prediction = wine.target_names[rf_classifier.predict(test[features])]

# Generate confusion matrix
print(pd.crosstab(test['class'], prediction, rownames=['Actual Class'], colnames=['Predicted Class']))