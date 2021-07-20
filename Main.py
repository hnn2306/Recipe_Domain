import os
import Query
from User import User
from Recipe import Recipe


def display_personal_recipes(user: User):
    """
    displays all recipes belonging to the provided user
    :param user: user logged in
    :return: True when finished
    """
    query = Query.get_user_recipe(user.username)
    recs = get_all_recipes(query)

    if recs:
        for rec in recs:
            print(rec)

    input("Press any key to close")
    return True


def display_all_recipes():
    """
    displays all recipes from the db
    :return: True when finished
    """
    query = Query.get_recipe()
    recs = get_all_recipes(query)

    if recs:
        for rec in recs:
            print(rec)

    input("Press any key to close")
    return True


def get_all_recipes(query):
    """
    gets all the recipes from the given query and creates object with it
    :param query: query to get recipes from
    :return: array of recipe objects
    """
    recs = []

    if not query:
        print("No recipes to display")
        return None

    for rec in query:
        # print(rec)
        receta = Recipe(int(rec[0]), rec[1], rec[2], int(rec[3]), rec[4], rec[5], int(rec[6]), int(rec[7]), rec[8], [], [])
        # TODO get the ingredients and categories
        recs.append(receta)
    return recs


def create_recipe(user: User):
    """
    creates a recipe and prompts the user for the specific attributes
    :param user: user logged in
    :return: True if creation canceled
    """
    print("Enter 'x' as the Name to cancel.")
    name = input("Name: ")

    if name.strip() == 'x':
        return True

    des = input("Description: ")
    serv = input("Number of Servings: ")
    diff = input("Difficulty: ")
    steps = input("Steps: ")
    time = input("Time: ")
    rating = input("Rating: ")
    ing = input("Enter ingredients separated by ','\n>")
    ingredients = ing.split(",")
    cat = input("Enter categories separated by ','\n>")
    categories = cat.split(",")

    query = Query.get_recipe()

    if query:
        id = len(query) + 1
    else:
        id = 0
    recipe = Recipe(id, name, des, serv, diff, steps, time, rating, user, categories, ingredients)
    Query.create_recipe(id, name, des, serv, diff, steps, time, rating, user.username, categories, ingredients)

    #TODO what to do with the recipe object??


def search_recipes_menu(user:User):
    """
    menu that allows the user to search a recipe given an attribute
    :param user: user logged in
    :return: True if user decides to go back
    """

    print("Search Recipes")
    while True:
        print("Choose an option",
              "================",
              "1. Search by Name",
              "2. Search by Ingredients",
              "3. Search by Category",
              "4. Go Back to Main Menu", sep="\n")

        try:
            op = int(input(">"))

            if op == 1:
                pass
                # TODO
                break
            elif op == 2:
                pass
                # TODO
                break
            elif op == 3:
                pass
                # TODO
                break
            elif op == 4:
                return True
        except ValueError:
            clear()
            print("Incorrect option. Try again\n")
            continue


def sort_recipes_menu(user: User):
    """
    menu that allows the user to sort things
    :param user: user logged in
    :return: True if user decides to go back
    """
    print("Sort Recipes")
    while True:
        print("Choose an option",
              "================",
              "1. Sort by Categories",
              "2. Sort by alphabet",
              "3. Sort by Rating",
              "4. Sort by most Recent", # TODO
              "5. Go Back to Main Menu", sep="\n")

        try:
            op = int(input(">"))

            if op == 1:
                pass
                # TODO
                break
            elif op == 2:
                pass
                # TODO
                break
            elif op == 3:
                pass
                # TODO
                break
            elif op == 4:
                pass
                # TODO
                break
            elif op == 5:
                return True
        except ValueError:
            clear()
            print("Incorrect option. Try again\n")
            continue


def recipe_menu(user: User):
    """
    displays the different thins that can be done with recipes
    :param user: user logged in
    :return: True if user goes back
    """
    while True:
        print("Choose an option",
              "================",
              "1. Create Recipe",
              "2. View all recipes",
              "3. View Personal Recipes",
              "4. Sort Recipe",
              "5. Search Recipe",
              "6. Go Back to Main Menu", sep="\n")

        try:
            op = int(input(">"))

            if op == 1:
                clear()
                if create_recipe(user):
                    clear()
                    continue
                break
            elif op == 2:
                clear()
                display_all_recipes()
                break
            elif op == 3:
                clear()
                if display_personal_recipes(user):
                    clear()
                    continue
                break
            elif op == 4:
                clear()
                if sort_recipes_menu(user):
                    clear()
                    continue
                break
            elif op == 5:
                clear()
                if search_recipes_menu(user):
                    clear()
                    continue
                break
            elif op == 6:
                return True
        except ValueError:
            clear()
            print("Incorrect option. Try again\n")
            continue


def edit_pantry():
    pass


def add_pantry_item():
    pass

def pantry_menu(user: User):
    """
        displays the different things that can be done with pantry items
        :param user: user logged in
        :return: True if user goes back
        """
    while True:
        print("Choose an option",
              "================",
              "1. Edit Pantry",
              "2. Add Items",
              "3. Go Back to Main Menu", sep="\n")

        try:
            op = int(input(">"))

            if op == 1:
                clear()
                #todo
                return True
            elif op == 2:
                clear()
                #todo
                return True
            elif op == 3:
                return True
        except ValueError:
            clear()
            print("Incorrect option. Try again\n")
            continue


def inner_menu(user: User):
    """
    displays menu for uhhh recipes and pantry
    :param user: user logged in
    :return: True if User log out
    """
    clear()
    print("Welcome back {name}".format(name = user.username))
    while True:
        print("Choose an option",
              "================",
              "1. Recipe Book",
              "2. View Pantry",
              "3. Edit User Info", #TODO
              "4. Log Out", sep="\n") #TODO

        try:
            op = int(input(">"))

            if op == 1:
                clear()
                if recipe_menu(user):
                    clear()
                    continue
                break
            elif op == 2:
                clear()
                if pantry_menu(user):
                    clear()
                    continue
                break
            elif op == 3:
                pass
                #TODO: log out user
            elif op == 4:
                clear()
                print("Logging you out") #TODO
        except ValueError:
            clear()
            print("Incorrect option. Try again\n")
            continue


def clear():
    """
    clears the entire terminal and
    and goes back to the top
    """
    os.system('cls' if os.name == 'nt' else 'clear')


def login():
    """
    user login
    """
    print("================", "User Login", sep="\n")
    username = input("Username: ")
    password = input("Password: ")
    query = Query.get_user(username)

    if query == []:
        clear()
        print("User {s} does not exist. Verify or try again".format(s = username))
        menu()
    else:
        if(query[0][1] == password):
            print("Logging you in ...")
            user = User(username, password, query[0][2])
            inner_menu(user)

        else:
            clear()
            print('Incorrect password. Try again.')
            login()


def register():
    """
    user registration
    """
    print("================", "User Registration", sep="\n")
    username = input("Username: ")
    password = input("Password: ")
    query = Query.get_user(username)

    if query != []:
        clear()
        print("User {s} already exists. Try logging in.".format(s = username))
        menu()
    else:
        next_id = len(Query.get_user_count()) + 1
        Query.create_user(username, password, next_id)
        user = User(username, password, next_id)
        print("User Created")
        inner_menu(user)


def menu():
    """
    displays the menu option and directs the user to the next step
    :return: None
    """
    while(True):
        print("Choose an option", "================",
              "1. Login",
              "2. Register",
              "3. Exit",
              "================", sep="\n")

        try:
            op = int(input(">"))

            if op == 1:
                clear()
                login()
                break
            elif op == 2:
                clear()
                register()
                break
            elif op == 3:
                print("Goodbye ..")
                exit(0)
        except ValueError:
            clear()
            print("Incorrect option. Try again\n")
            continue


def main():
    print("Welcome to Recipe Domain by team Gyarados\n")
    menu()

if __name__ == "__main__":
    main()
