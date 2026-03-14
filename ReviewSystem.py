# By Enrique Martinez
# 3/13/2026
# Description: Not full sure what we are doing, or how we are doing it. So this function is a rough draft for the
# review system aspect of the ecommerce website. For now all data with be stored/read using a text document, similar
# to my experience of working with c++. Since I am new at python.

def review_system() -> None:
    filename = "reviews.txt"                                   # Where any data regarding certified reviews are stored.

    valid_user: bool = True                                    # User already posted a review, or is just generally invalid.
    name_to_find: str = "$" + input("\nEnter username: ")      # User's username is question.

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
            review: str = input("\nEnter the review: ")
            file.write(name_to_find + "\n" + review + "\n\n")
        else:
            print("Invalid user.")     # Invalid users cant leave another or any reviews.

review_system()