from classify import classify

SAMPLES = [
    # Billing (3)
    ("I was charged twice for my subscription this month.", "Billing"),
    ("My invoice shows an incorrect amount. Please fix it.", "Billing"),
    ("I need a refund for the payment made last week.", "Billing"),
    # Technical (3)
    ("The app crashes every time I try to upload a file.", "Technical"),
    ("I keep getting a 500 error when accessing the dashboard.", "Technical"),
    ("The integration with Slack stopped working after the update.", "Technical"),
    # Account (3)
    ("I can't log in to my account even after resetting my password.", "Account"),
    ("Please update the email address associated with my account.", "Account"),
    ("I want to delete my account and all my data.", "Account"),
    # General (3, including 2 ambiguous)
    ("How do I export my data from the platform?", "General"),          # ambiguous: could be Account
    ("Can you explain what the premium plan includes?", "General"),     # ambiguous: could be Billing
    ("Where can I find your documentation and user guides?", "General"),
]


def run_evaluation():
    print(f"{'Ticket':<55} {'Actual':<12} {'Predicted':<12} {'OK'}")
    print("-" * 90)

    per_category = {label: {"correct": 0, "total": 0} for label in ["Billing", "Technical", "Account", "General"]}
    correct_total = 0

    for ticket, actual in SAMPLES:
        try:
            predicted = classify(ticket)
        except Exception as e:
            predicted = "ERROR"
            print(f"  Error on ticket: {e}")

        ok = "OK" if predicted == actual else "FAIL"
        if predicted == actual:
            correct_total += 1
            per_category[actual]["correct"] += 1
        per_category[actual]["total"] += 1

        short = ticket[:52] + "..." if len(ticket) > 52 else ticket
        print(f"{short:<55} {actual:<12} {predicted:<12} {ok}")

    total = len(SAMPLES)
    print(f"\nOverall Accuracy: {correct_total}/{total} ({correct_total/total*100:.1f}%)\n")
    print("Per-Category Results:")
    for cat, stats in per_category.items():
        c, t = stats["correct"], stats["total"]
        print(f"  {cat:<12}: {c}/{t} ({c/t*100:.1f}%)")


if __name__ == "__main__":
    run_evaluation()
