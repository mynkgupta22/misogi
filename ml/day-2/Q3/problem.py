# spam_probability.py
# Calculate P(Spam | Email contains "free") using Bayes' Theorem

def get_positive_integer(prompt):
    """Helper function to get and validate positive integer input."""
    while True:
        try:
            value = int(input(prompt))
            if value < 0:
                print("Please enter a non-negative integer.")
            else:
                return value
        except ValueError:
            print("Invalid input. Please enter an integer.")


# Get validated input from user
total_emails = get_positive_integer("Enter total number of emails: ")
emails_with_free = get_positive_integer("Enter number of emails with the word 'free': ")
spam_emails = get_positive_integer("Enter number of spam emails: ")
spam_and_free = get_positive_integer("Enter number of emails that are spam and contain 'free': ")

# Validate logical consistency of inputs
if (emails_with_free > total_emails or
    spam_emails > total_emails or
    spam_and_free > spam_emails or
    spam_and_free > emails_with_free):
    print("Input values are not logically consistent. Please check your numbers.")
else:
    # Calculate the probabilities
    P_spam = spam_emails / total_emails
    P_free = emails_with_free / total_emails
    P_free_given_spam = spam_and_free / spam_emails if spam_emails != 0 else 0

    # Apply Bayes’ Theorem
    if P_free == 0:
        print("Cannot compute P(Spam | Free): P(Free) is zero.")
    else:
        P_spam_given_free = (P_free_given_spam * P_spam) / P_free
        print(f"\nP(Spam | Email contains 'free') = {P_spam_given_free:.4f}")
