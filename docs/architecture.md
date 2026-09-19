# FinSight AI — System Architecture

## 1. Project Overview

FinSight AI is a multi-asset quantitative intelligence and backtesting platform designed to analyze:

- NVIDIA
- Bitcoin
- Gold

The system combines historical market data, financial analysis, risk metrics, technical indicators, backtesting, quantitative intelligence, and AI-based explanation.

---

## 2. High-Level Architecture

```text
                    ┌─────────────────────┐
                    │       USER          │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   STREAMLIT UI      │
                    │     Member 3        │
                    └──────────┬──────────┘
                               │
              ┌────────────────┴────────────────┐
              │                                 │
              ▼                                 ▼
   ┌─────────────────────┐           ┌─────────────────────┐
   │ Financial Analysis  │           │    Backtesting      │
   │     Member 4        │           │     Member 2        │
   └──────────┬──────────┘           └──────────┬──────────┘
              │                                 │
              └────────────────┬────────────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Quant Intelligence  │
                    │     Member 1        │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │    AI Explanation   │
                    │     Member 1        │
                    └─────────────────────┘
