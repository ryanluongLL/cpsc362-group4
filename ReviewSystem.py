# By Enrique Martinez
# 3/13/2026
# Description: Not full sure what we are doing, or how we are doing it. So this function is a rough draft for the
# review system aspect of the ecommerce website. For now all data with be stored/read using a text document, similar
# to my experience of working with c++. Since I am new at python.

def review_system() -> None:
    filename = "reviews.txt"                                   # Where any data regarding certified reviews are stored.

    MAX_LENGTH = 100                                           # The constant max length for a user review-text string.
    valid_user: bool = True                                    # User already posted a review, or is just generally invalid.
    name_to_find: str = "*" + input("\nEnter username: ")      # User's username is question.

    # **** USER/ACCOUNT DETAILS NEEDED TO BE IMPLEMENTED ELSE WHERE, THEN ADDED HERE WITH MODIFICATIONS.
    # TO BE ABLE TO IMPLEMENT SECURITY CHECKS/ETC. For now this will be a temporary solution.
    try:
        with open(filename, "r") as file:
            for line in file:                                  # Search the file for the user's username.
                if name_to_find.lower() in line.lower():
                    valid_user = False
                else:
                    pass
    except FileNotFoundError:
        print("File not found.")

    # NOW THAT THE CHECKS ARE DONE, WE WRITE THE USER INFO AND REVIEW INTO FILE.
    # The data from the file can be implemented in separate functions/etc that deal with UI.
    with open(filename, "a") as file:  # Opens the data store, and or create it if needed.
        if valid_user:
            
            # Try to get integer input for rating of product.
            while True:
                try:
                    star_rating = int(input("Enter a number (0–5) for the product's rating: "))
                    if 0 <= star_rating <= 5:
                        break
                    else:
                        print("Invalid input. Must be between 0 and 5.")
                except ValueError:
                    print("Invalid input. Please enter an integer.")

            # Try to get text of review within the set length constraint.
            while True:
                    review: str = input("\nEnter the review: ")
                    if len(review) <= MAX_LENGTH:
                        break
                    else:
                        print(f"Review too long! Max length is {MAX_LENGTH} characters.")

            file.write('\n' + name_to_find + "\n*" + str(star_rating) + '\n' + review + "*\n")    
        else:
            print("Invalid user.")     # Invalid users cant leave another or any reviews.

review_system()

# The * symbol was added an additional indicator to format. So we know when to stop reading certain info at a time.
# Overall Format: \n *username
#                \n *star_rating
#                \n review* \n
