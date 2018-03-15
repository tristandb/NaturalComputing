from sklearn.datasets import load_digits
from sklearn.ensemble import RandomForestClassifier
import pandas as pd
import numpy as np

np.random.seed(9)

dimensions = 13

# Load data
wine = load_digits()
df = pd.DataFrame(wine.data)

# Set class
df['class'] = pd.Categorical.from_codes(wine.target, wine.target_names)

# Split train and test into two groups of approximately 3/4 and 1/4 size
df['is_train'] = np.random.uniform(0, 1, len(df)) < 0.75
train, test = df[df['is_train'] == True], df[df['is_train'] == False]

# Assign features
features = df.columns[:dimensions]

# Factorize to numbers
y = pd.factorize(train['class'])[0]

y_test = pd.factorize(test['class'])[0]

# Train classifier
rf_classifier = RandomForestClassifier(n_jobs=-1, n_estimators=10, random_state=42)
rf_classifier.fit(train[features], y)

# Predict test set
prediction = wine.target_names[rf_classifier.predict(test[features])]

print(rf_classifier.score(train[features], y))

print(len(test))
# Generate confusion matrix
print(pd.crosstab(test['class'], prediction, rownames=['Actual Class'], colnames=['Predicted Class']))