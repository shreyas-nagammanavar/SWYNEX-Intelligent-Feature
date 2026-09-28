from classify import classify
from evaluate import run_evaluation


def main():
    print("=== Support Ticket Classifier ===")
    while True:
        print("\n1. Classify a ticket\n2. Run evaluation\n3. Quit")
        choice = input("Choose an option: ").strip()

        if choice == "1":
            ticket = input("Enter ticket text: ").strip()
            try:
                label = classify(ticket)
                print(f"Category: {label}")
            except (ValueError, EnvironmentError, PermissionError,
                    ConnectionError, TimeoutError, RuntimeError) as e:
                print(f"Error: {e}")

        elif choice == "2":
            run_evaluation()

        elif choice == "3":
            print("Goodbye!")
            break

        else:
            print("Invalid choice. Enter 1, 2, or 3.")


if __name__ == "__main__":
    main()
