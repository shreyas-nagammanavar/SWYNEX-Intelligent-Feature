# SWYNEX Intelligent Feature — Support Ticket Classifier

Classifies customer support tickets into **Billing**, **Technical**, **Account**, or **General** using the Hugging Face zero-shot classification API (`facebook/bart-large-mnli`).

---

## Setup

```bash
pip install -r requirements.txt
cp .env.example .env
# Edit .env and add your Hugging Face API token
```

---

## Usage

```bash
python main.py
```

Menu options:
1. **Classify a ticket** — enter any support ticket text and get a category
2. **Run evaluation** — test 12 labeled samples and see accuracy
3. **Quit**

---

## Project Structure

```
classify.py       # Core classifier with error handling
evaluate.py       # Evaluation script with labeled samples
main.py           # CLI menu
.env.example      # Token placeholder
requirements.txt  # Dependencies
```

---

## Failure Cases

| Scenario | Error Raised | User Message |
|---|---|---|
| `HF_API_TOKEN` missing from `.env` | `EnvironmentError` | "HF_API_TOKEN is not set. Add it to your .env file." |
| Empty or whitespace-only ticket | `ValueError` | "Ticket text cannot be empty." |
| No internet / DNS failure | `ConnectionError` | "Network error: could not reach the Hugging Face API." |
| API takes > 30 seconds | `TimeoutError` | "Request timed out. The API took too long to respond." |
| Wrong/expired token | `PermissionError` (401) | "Invalid API token (401). Check your HF_API_TOKEN." |
| Too many requests | `RuntimeError` (429) | "Rate limit exceeded (429). Please wait and try again." |
| Model still loading | `RuntimeError` (503) | "Model is loading (503). Please retry in a few seconds." |

All errors are caught in `main.py` and shown as friendly messages — no tracebacks.

---

## Evaluation Results

Tested on 12 labeled tickets (3 per category, including 2 ambiguous General tickets).

```
Ticket                                                  Actual       Predicted    OK
------------------------------------------------------------------------------------------
I was charged twice for my subscription this month.     Billing      Billing      ✓
My invoice shows an incorrect amount. Please fix it.    Billing      Billing      ✓
I need a refund for the payment made last week.         Billing      Billing      ✓
The app crashes every time I try to upload a file.      Technical    Technical    ✓
I keep getting a 500 error when accessing the dashbo... Technical    Technical    ✓
The integration with Slack stopped working after th...  Technical    Technical    ✓
I can't log in to my account even after resetting m...  Account      Account      ✓
Please update the email address associated with my ...  Account      Account      ✓
I want to delete my account and all my data.            Account      Account      ✓
How do I export my data from the platform?              General      General      ✓
Can you explain what the premium plan includes?         General      General      ✓
Where can I find your documentation and user guides?    General      General      ✓

Overall Accuracy: 12/12 (100.0%)

Per-Category Results:
  Billing     : 3/3 (100.0%)
  Technical   : 3/3 (100.0%)
  Account     : 3/3 (100.0%)
  General     : 3/3 (100.0%)
```

> **Note on ambiguous tickets:** "How do I export my data?" could lean toward Account, and "Can you explain what the premium plan includes?" could lean toward Billing. The model correctly classified both as General based on their informational intent.

---

## API

- Model: `facebook/bart-large-mnli`
- Endpoint: `https://router.huggingface.co/hf-inference/models/facebook/bart-large-mnli`
- Auth: Bearer token via `HF_API_TOKEN` in `.env`
