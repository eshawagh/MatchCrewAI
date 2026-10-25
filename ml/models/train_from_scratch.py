"""
MatchCrewAI - ML model written from scratch (numpy only).
Task: predict a student's primary domain from their skills.
Algorithm: softmax regression trained with gradient descent.
"""
import ast
import numpy as np
import pandas as pd

np.random.seed(42)

# ---------- 1. Build the dataset ----------
df = pd.read_csv("data/students_clean.csv")
df["skills"] = df["Technical Skills"].apply(lambda x: [s.strip().lower() for s in ast.literal_eval(x)])
df["domain"] = df["Preferred Domain(s)"].apply(lambda x: ast.literal_eval(x)[0].strip())

vocab = sorted({s for row in df["skills"] for s in row})
classes = sorted(df["domain"].unique())
s_idx = {s: i for i, s in enumerate(vocab)}
c_idx = {c: i for i, c in enumerate(classes)}

X = np.zeros((len(df), len(vocab)))
for i, row in enumerate(df["skills"]):
    for s in row:
        X[i, s_idx[s]] = 1
y = np.array([c_idx[d] for d in df["domain"]])

print(f"Students: {len(df)}   Skills (features): {len(vocab)}   Domains (classes): {len(classes)}")

# ---------- 2. Train / test split (80 / 20) ----------
order = np.random.permutation(len(X))
cut = int(0.8 * len(X))
X_tr, y_tr = X[order[:cut]], y[order[:cut]]
X_te, y_te = X[order[cut:]], y[order[cut:]]
print(f"Training: {len(X_tr)}   Testing: {len(X_te)}\n")

# ---------- 3. The model ----------
def softmax(z):
    z = z - z.max(axis=1, keepdims=True)
    e = np.exp(z)
    return e / e.sum(axis=1, keepdims=True)

W = np.zeros((X.shape[1], len(classes)))
b = np.zeros(len(classes))
Y_tr = np.eye(len(classes))[y_tr]

# ---------- 4. Training loop (gradient descent) ----------
lr, epochs = 0.5, 500
for epoch in range(epochs):
    probs = softmax(X_tr @ W + b)
    loss = -np.mean(np.sum(Y_tr * np.log(probs + 1e-9), axis=1))
    grad = probs - Y_tr
    W -= lr * (X_tr.T @ grad) / len(X_tr)
    b -= lr * grad.mean(axis=0)
    if epoch % 100 == 0 or epoch == epochs - 1:
        print(f"epoch {epoch:3d}   loss {loss:.4f}")

# ---------- 5. Evaluate ----------
def predict(M):
    return np.argmax(softmax(M @ W + b), axis=1)

train_acc = (predict(X_tr) == y_tr).mean()
test_acc = (predict(X_te) == y_te).mean()
baseline = (y_te == np.bincount(y_tr).argmax()).mean()

print(f"\nTrain accuracy: {train_acc * 100:.1f}%")
print(f"Test accuracy : {test_acc * 100:.1f}%")
print(f"Baseline (always guess most common domain): {baseline * 100:.1f}%")

# ---------- 6. Sample predictions on unseen students ----------
print("\nSample predictions on test students:")
test_rows = df.iloc[order[cut:]]
for (_, r), p in list(zip(test_rows.iterrows(), predict(X_te)))[:5]:
    print(f"  {', '.join(r['skills']):<42} actual: {r['domain']:<18} predicted: {classes[p]}")

# ---------- 7. Predict for a brand-new student ----------
new_skills = ["python", "machine learning", "tensorflow"]
v = np.zeros((1, len(vocab)))
for s in new_skills:
    if s in s_idx:
        v[0, s_idx[s]] = 1
probs = softmax(v @ W + b)[0]
print(f"\nNew student with skills {new_skills}:")
for i in np.argsort(probs)[::-1][:3]:
    print(f"  {classes[i]:<20} {probs[i] * 100:5.1f}%")

# ---------- 8. Save the trained model ----------
np.savez("ml/models/domain_model.npz", W=W, b=b, vocab=vocab, classes=classes)
print("\nModel saved to ml/models/domain_model.npz")