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


def search_by_name():
    name = input("Enter name: ")
    query = Query.get_recipe_name(name)

    if not query:
        print("Sorry, there is no " + name)
    else:
        for item in query:
            print(item)

    input("Press any key to close")
    return True

def search_by_category():
    category = input("Enter category: ")
    query = Query.get_recipe_cate(category)

    if not query:
        print("sorry, there are no recipes in " + category)
    else:
        for i in query:
            print(i)
            # print(Query.get_recipe_id(i))

    input("Press any key to close")
    return True

def search_by_ingredients():
    ing = input("Enter one ingredient: ")
    query = Query.get_recipe_ing(ing)

    if not query:
        print("sorry, there are no recipes with " + ing)
    else:
        for i in query:
            print(i)
            # print(Query.get_recipe_id(i))

    input("Press any key to close")
    return True

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
                clear()
                search_by_name()
                break
            elif op == 2:
                clear()
                search_by_ingredients()
                break
            elif op == 3:
                clear()
                search_by_category()
                break
            elif op == 4:
                return True
        except ValueError:
            clear()
            print("Incorrect option. Try again\n")
            continue

def sort(sort_type):
    order = ""
    while True:
        try:
            order = input("ASC or DESC? ")
        except order != "ASC" or "DESC":
            print("Invalid option. Try again.\n")
            continue

    query = None
    if sort_type == "category":
        query = Query.sort_recipes_by_category(order)
    elif sort_type == "alphabetical":
        query = Query.sort_recipes_by_alphabetical(order)
    elif sort_type == "rating":
        query = Query.sort_recipes_by_rating(order)
    elif sort_type == "recency":
        query = Query.sort_recipes_by_recency(order)

    if query is not None:
        for i in query:
            print(i)
    else:
        print("Sort Unsuccessful")

    input("Press any key to close")
    return True

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
              "2. Sort by Alphabetical Order",
              "3. Sort by Rating",
              "4. Sort by Most Recent",
              "5. Go Back to Main Menu", sep="\n")

        try:
            op = int(input("> "))

            if op == 1:
                clear()
                sort("category")
                break
            elif op == 2:
                clear()
                sort("alphabetical")
                break
            elif op == 3:
                clear()
                sort("rating")
                break
            elif op == 4:
                clear()
                sort("recency")
                break
            elif op == 5:
                return True
        except ValueError:
            clear()
            print("Incorrect option. Try again.\n")
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
              "2. View All Recipes",
              "3. View Personal Recipes",
              "4. Sort Recipes",
              "5. Search Recipes",
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
    name = input("Enter name: ")
    aisle = input("Enter aisle: ")
    exdate = input("Enter expire date (YYYY-MM-DD): ")

    query = Query.get_items()


    next_id = len(Query.get_items()) + 1
    Query.create_item(next_id, aisle, name, exdate)
    print("item created")
    # if query != []:
        # todo if the item exist in pantry, update the track



def display_all_items():
    query = Query.get_items()

    print("=== Pantry ===")
    for item in query:
        print("Name: " + item[2])
        print("Aisle: " + str(item[1]))
        print("Expire date: " + item[3])
        print("========")

    input("Press any key to close")
    return True



def pantry_menu(user: User):
    """
        displays the different things that can be done with pantry items
        :param user: user logged in
        :return: True if user goes back
        """
    while True:
        print("Choose an option",
              "================",
              "1. List Items",
              "2. Edit Pantry",
              "3. Add Items",
              "4. Go Back to Main Menu", sep="\n")

        try:
            op = int(input(">"))

            if op == 1:
                clear()
                display_all_items()
                #todo I need to change this to getting pantry of user
            elif op == 2:
                clear()
                #todo
                return True
            elif op == 3:
                clear()
                #todo
                return True
            elif op == 4:
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
        next_id = len(Query.get_users()) + 1
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
