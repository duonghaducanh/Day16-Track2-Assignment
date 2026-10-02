#!/usr/bin/env python3
"""LightGBM benchmark tren dataset credit card fraud (mlg-ulb/creditcardfraud).

Thiet ke do luong (theo bang CP3):
  - Load data      : do pd.read_csv() bang time.perf_counter()
  - Split          : tach Class khoi features; stratify + seed co dinh; test chi dung danh gia cuoi
  - Training       : do rieng thoi gian .fit()
  - Chon so vong   : early stopping tren validation (KHONG dung test)
  - Danh gia       : AUC dung xac suat; acc/f1/precision/recall dung nhan du doan
  - Latency        : warm-up, do du doan 1 dong x 100 lan
  - Throughput     : batch 1000 dong; 1000 / thoi_gian_giay
  - Luu            : benchmark_result.json + in terminal
"""
import json
import time
import warnings
from pathlib import Path

warnings.filterwarnings("ignore")

import lightgbm as lgb
import pandas as pd
from sklearn.metrics import (
    accuracy_score,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.model_selection import train_test_split

DATA = Path.home() / "ml-benchmark" / "creditcard.csv"
OUTPUT = Path("benchmark_result.json")
SEED = 42
INSTANCE = "t3.medium"
REGION = "us-east-1"

# --- Load ---
t0 = time.perf_counter()
df = pd.read_csv(DATA)
data_load_seconds = time.perf_counter() - t0

# --- Split: Class tach khoi features; stratify + seed co dinh ---
y = df["Class"]
X = df.drop(columns=["Class"])
# 20% giu lai lam test, chi dung danh gia cuoi
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=SEED, stratify=y
)
# 0.25 cua phan train = 20% toan bo -> chia 60/20/20
X_fit, X_val, y_fit, y_val = train_test_split(
    X_train, y_train, test_size=0.25, random_state=SEED, stratify=y_train
)

# --- Train ---
# Dataset cuc mat can bang (~0.17% positive). num_leaves=31 mac dinh overfit
# nang (AUC giam dan khi them cay), nen dung cay don gian hon + min_child_samples
# lon de moi la co du mau duong. Early stopping tren validation, khong dung test.
model = lgb.LGBMClassifier(
    n_estimators=1000,
    learning_rate=0.05,
    num_leaves=8,
    min_child_samples=100,
    random_state=SEED,
    n_jobs=2,
    verbosity=-1,
)
t0 = time.perf_counter()
model.fit(
    X_fit,
    y_fit,
    eval_set=[(X_val, y_val)],
    eval_metric="auc",
    callbacks=[lgb.early_stopping(50, verbose=False)],
)
training_seconds = time.perf_counter() - t0

# --- Evaluate tren test ---
proba = model.predict_proba(X_test)[:, 1]      # AUC dung xac suat
pred = (proba >= 0.5).astype(int)              # nhan cho acc/f1/precision/recall

# --- Latency: warm-up roi do du doan 1 dong nhieu lan ---
single_row = X_test.iloc[[0]]
model.predict_proba(single_row)                # warm-up (khong tinh vao ket qua)
runs = 100
t0 = time.perf_counter()
for _ in range(runs):
    model.predict_proba(single_row)
latency_1_row_ms = (time.perf_counter() - t0) * 1000 / runs

# --- Throughput: batch 1000 dong ---
batch = X_test.iloc[:1000]
t0 = time.perf_counter()
model.predict_proba(batch)
batch_seconds = time.perf_counter() - t0
throughput_1000_rows_per_second = 1000 / batch_seconds

results = {
    "instance": INSTANCE,
    "region": REGION,
    "seed": SEED,
    "dataset_rows": int(len(df)),
    "data_load_seconds": round(data_load_seconds, 4),
    "train_rows": int(len(X_fit)),
    "validation_rows": int(len(X_val)),
    "test_rows": int(len(X_test)),
    "training_seconds": round(training_seconds, 4),
    "best_iteration": int(model.best_iteration_ or model.n_estimators),
    "auc_roc": round(float(roc_auc_score(y_test, proba)), 6),
    "accuracy": round(float(accuracy_score(y_test, pred)), 6),
    "f1": round(float(f1_score(y_test, pred, zero_division=0)), 6),
    "precision": round(float(precision_score(y_test, pred, zero_division=0)), 6),
    "recall": round(float(recall_score(y_test, pred, zero_division=0)), 6),
    "latency_1_row_ms": round(latency_1_row_ms, 4),
    "latency_runs": runs,
    "throughput_1000_rows_per_second": round(throughput_1000_rows_per_second, 2),
}

OUTPUT.write_text(json.dumps(results, indent=2) + "\n", encoding="utf-8")
print(json.dumps(results, indent=2))
print(f"\nSaved results to {OUTPUT.resolve()}")
