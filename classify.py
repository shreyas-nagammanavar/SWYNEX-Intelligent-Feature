import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_URL = "https://router.huggingface.co/hf-inference/models/facebook/bart-large-mnli"
LABELS = [
    "billing, payment, invoice, refund, charge",
    "technical issue, bug, error, crash, integration",
    "account management, login access, password reset, email update, delete account, sign in problem",
    "general question, information, documentation, how to",
]
LABEL_MAP = {
    "billing, payment, invoice, refund, charge": "Billing",
    "technical issue, bug, error, crash, integration": "Technical",
    "account management, login access, password reset, email update, delete account, sign in problem": "Account",
    "general question, information, documentation, how to": "General",
}


def classify(ticket: str) -> str:
    token = os.getenv("HF_API_TOKEN")
    if not token:
        raise EnvironmentError("HF_API_TOKEN is not set. Add it to your .env file.")

    ticket = ticket.strip()
    if not ticket:
        raise ValueError("Ticket text cannot be empty.")

    headers = {"Authorization": f"Bearer {token}"}
    payload = {"inputs": ticket, "parameters": {"candidate_labels": LABELS}}

    try:
        response = requests.post(API_URL, headers=headers, json=payload, timeout=30)
    except requests.exceptions.ConnectionError:
        raise ConnectionError("Network error: could not reach the Hugging Face API.")
    except requests.exceptions.Timeout:
        raise TimeoutError("Request timed out. The API took too long to respond.")

    if response.status_code == 401:
        raise PermissionError("Invalid API token (401). Check your HF_API_TOKEN.")
    if response.status_code == 429:
        raise RuntimeError("Rate limit exceeded (429). Please wait and try again.")
    if response.status_code == 503:
        raise RuntimeError("Model is loading (503). Please retry in a few seconds.")
    if not response.ok:
        raise RuntimeError(f"API error {response.status_code}: {response.text}")

    result = response.json()
    if isinstance(result, list):
        top = max(result, key=lambda x: x["score"])["label"]
    else:
        top = result["labels"][0]
    return LABEL_MAP.get(top, top)
