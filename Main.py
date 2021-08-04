import os
import Query
from User import User
from Recipe import Recipe
import time


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
    clear()
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
    clear()
    return True


def get_all_recipes(query):
    """
    gets all the recipes from the given query and creates object with it
    by calling another method
    pre: this receives multiple recipes within the same query
    :param query: query containing multiple recipes
    :return: array of recipe objects
    """
    recs = []

    if not query:
        print("No recipes to display")
        return None

    for rec in query:
        # print(rec)
        receta = create_recipe_from_query(rec)
        recs.append(receta)
    return recs


def create_recipe(user: User):  # TODO
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
    diff = input("Difficulty (Easy, Medium, Hard): ")
    steps = input("Steps: ")
    time = input("Time: ")
    rating = input("Rating (1-5): ")
    ing = input("Enter ingredients in the format <Name:quantity> and separate with ','\n>")
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


def search_by_name(user:User):
    name = input("Enter name: ")
    query = Query.get_recipe_by_name(name)

    if not query:
        print("Sorry, there is no " + name)
    else:
        for item in query:
            recipe = create_recipe_from_query(item)
            Query.add_to_history(user.ID, recipe.recipe_id)
            print(recipe)

    input("Press any key to close")
    clear()
    return True


def search_by_category():
    category = input("Enter category: ")
    query = Query.get_recipe_by_cate(category)

    if not query:
        print("sorry, there are no recipes in " + category)
    else:
        print("These are the recipes within the " + category + " category: \n")
        for i in query:
            print(create_recipe_from_query(i))
            # print(Query.get_recipe_id(i))

    input("Press any key to close")
    clear()
    return True


def search_by_ingredients():
    ing = input("Enter one ingredient: ")
    query = Query.get_recipe_by_ing(ing)

    if not query:
        print("sorry, there are no recipes with " + ing)
    else:
        clear()
        print("These recipes contain " + ing + ":\n")
        for i in query:
            print(create_recipe_from_query(i))
            # print(Query.get_recipe_id(i))

    input("Press any key to close")
    clear()
    return True


def search_recipes_menu(user: User):
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
              "4. Go Back to Recipe Menu", sep="\n")

        try:
            op = int(input(">"))

            if op == 1:
                clear()
                search_by_name(user)
                continue
            elif op == 2:
                clear()
                search_by_ingredients()
                continue
            elif op == 3:
                clear()
                search_by_category()
                continue
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
        if order == "ASC":
            if sort_type == "category":
                query = Query.sort_recipes_by_category_ASC()
            elif sort_type == "alphabetical":
                query = Query.sort_recipes_by_alphabetical_ASC()
            elif sort_type == "rating":
                query = Query.sort_recipes_by_rating_ASC()
            elif sort_type == "recency":
                query = Query.sort_recipes_by_recency_ASC()
        elif order == "DESC":
            if sort_type == "category":
                query = Query.sort_recipes_by_category_DESC()
            elif sort_type == "alphabetical":
                query = Query.sort_recipes_by_alphabetical_DESC()
            elif sort_type == "rating":
                query = Query.sort_recipes_by_rating_DESC()
            elif sort_type == "recency":
                query = Query.sort_recipes_by_recency_DESC()

        if query is not None:
            for i in query:
                print(create_recipe_from_query(i))
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
                if sort("category"):
                    clear()
                    continue
                break
            elif op == 2:
                clear()
                if sort("alphabetical"):
                    clear()
                    continue
                break
            elif op == 3:
                clear()
                if sort("rating"):
                    clear()
                    continue
                break
            elif op == 4:
                clear()
                if sort("recency"):
                    clear()
                    continue
                break
            elif op == 5:
                return True
        except ValueError:
            clear()
            print("Incorrect option. Try again.\n")
            continue


def cook_recipe(user: User):
    # changed this to prompt for the name instead
    # while True:
    #     try:
    #         recipeID = int(input("Enter the recipe ID of the recipe you would like to cook: "))
    #         break
    #     except ValueError:
    #         print("Invalid input. Try again.")
    recipe = find_recipe_to_edit()
    while True:
        try:
            scale = int(input("Enter the scale of how much you would like to cook of this recipe: "))
            break
        except ValueError:
            print("Invalid input. Try again.")

    Query.mark_recipe(user.ID, recipe.recipe_id, scale)
    return True


def create_recipe_from_query(query: tuple) -> Recipe:
    """
    creates a recipe object from a given query element
    pre: the query is expected to be a single recipe. If the
    recipe might contain more than one recipe, it must be looped an
    passed one by one. see method get_all_recipes()
    :param query: query string
    :return: the recipe object
    """

    id = int(query[0])

    # get all the categories that correspond to this recipe
    cat_query = Query.get_categories_of_recipe(id)
    cats = []  # categories of this recipe
    if cat_query is not []:
        for cat in cat_query:
            cats.append(cat[1])

    # get all the ingredients that correspond to this recipe
    ing_query = Query.get_ingredients_of_recipe(id)
    ing = dict()  # dictionary that will contain all ingredients and quantity needed
    if ing_query is not None:
        for i in ing_query:
            item_name = Query.get_item_by_id(i[0])[0][0]
            amount = i[2]
            ing[item_name] = amount

    # create the item
    receta = Recipe(id, query[1], query[2], int(query[3]), query[4], query[5], int(query[6]),
            int(query[7]), query[8], cats, ing)

    return receta


def find_recipe_to_edit() -> Recipe:
    """
    gives the user options of finding a recipe so they can edit it
    :return: the recipe once found or None if none selected
    """

    while True:
        print("Chose an option",
              "================",
              "1. Find recipe by name",
              "2. Go Back", sep="\n")

        try:
            op = int(input("> ").strip())

            if op == 1:
                clear()
                name = input("Enter recipe Name: ").strip()
                recipe_query = Query.get_recipe_by_name(name)

                if recipe_query != [] and len(recipe_query) >= 1:
                    # only one recipe expected from query since name is unique
                    recipe_obj = create_recipe_from_query(recipe_query[0])
                    return recipe_obj
                else:
                    clear()
                    print("Recipe {n} does not exist. Try again".format(n=name))
                    return None

            elif op == 2:
                # goes back with no recipe
                return None

        except ValueError:
            clear()
            print("Incorrect option. Try again\n")
            continue


def edit_a_recipe_menu(recipe: Recipe, user: User):
    """
    allows the user to edit attributes of a recipe
    :return:
    """
    while True:
        print("Recipe Selected: ")
        print(recipe)

        print("Chose an option",
              "================",
              "1. Edit Recipe Name",
              "2. Edit Description",
              "3. Edit Serving Quantity",
              "4. Edit Difficulty Level (Easy, Medium, Hard)",
              "5. Edit Steps",
              "6. Edit Cooking Time",
              "7. Edit Rating (1-5)",
              "8. Delete Recipe",
              "9. Go Back to Recipe Menu", sep="\n")

        try:
            op = int(input("> ").strip())

            if op == 1:
                clear()
                name = input("Enter new name: ").strip()

                if name == "" or name == recipe.name:
                    clear()
                    print("Name Attribute did not change.")
                    continue

                else:
                    Query.update_recipe("Recipe_Name", name, recipe.recipe_id)
                    clear()
                    print("Recipe Name changed from {rec_name} to {new_name}.\n".format(rec_name=recipe.name, new_name=name))
                    recipe.name = name
                    continue

            elif op == 2:
                clear()
                desc = input("Enter new description: ").strip()

                if desc == "" or desc == recipe.description:
                    clear()
                    print("Description Attribute did not change.")
                    continue

                else:
                    Query.update_recipe("Description", desc, recipe.recipe_id)
                    clear()
                    print("Recipe description has changed.\n")
                    recipe.description = desc
                    continue

            elif op == 3:
                clear()
                serv = input("Enter new serving quantity: ").strip()

                if serv == "" or serv == recipe.servings:
                    clear()
                    print("Servings Attribute did not change.")
                    continue

                else:
                    Query.update_recipe("Servings", serv, recipe.recipe_id)
                    clear()
                    print("Recipe Servings changed from {old_serv} to {new_serv}.\n".format(old_serv=recipe.servings, new_serv=serv))
                    recipe.servings = serv
                    continue

            elif op == 4:
                clear()
                diff = input("Enter new difficulty: ")

                if diff == "" or diff == recipe == recipe.difficulty:
                    clear()
                    print("Difficulty Attribute did not change.")
                    continue

                else:
                    Query.update_recipe("Difficulty", diff, recipe.recipe_id)
                    clear()
                    print("Recipe Difficulty changed from {old_diff} to {new_diff}.\n".format(old_diff=recipe.difficulty, new_diff=diff))
                    recipe.difficulty = diff
                    continue

            elif op == 5:
                clear()
                steps = input("Enter new Steps: ").strip()

                if steps == "" or steps == recipe.steps:
                    clear()
                    print("Steps Attribute did not change.")
                    continue

                else:
                    Query.update_recipe("Steps", steps, recipe.recipe_id)
                    clear()
                    print("Recipe Steps have changed.\n")
                    recipe.steps = steps
                    continue

            elif op == 6:
                clear()
                time = input("Enter new Cooking Time: ").strip()

                if time == "" or time == str(recipe.cooking_time):
                    clear()
                    print("Cooking Time Attribute did not change.")
                    continue

                else:
                    Query.update_recipe("Cooking_Time", time, recipe.recipe_id)
                    clear()
                    print("Recipe Name changed from {old_time} to {new_time}.\n".format(old_time=recipe.cooking_time, new_time=time))
                    recipe.cooking_time = time
                    continue

            elif op == 7:
                clear()
                rat = input("Enter new Rating: ").strip()

                if rat == "" or rat == str(recipe.rating):
                    clear()
                    print("Rating Attribute did not change.")
                    continue

                else:
                    Query.update_recipe("Rating", rat, recipe.recipe_id)
                    clear()
                    print("Recipe Rating changed from {old_rat} to {new_rat}.\n".format(old_rat=recipe.rating, new_rat=rat))
                    recipe.rating = rat
                    continue

            elif op == 8:
                clear()
                if recipe.username != user.username:
                    print("You cannot delete this recipe.")
                else:
                    Query.delete_recipe(recipe.recipe_id)
                    return True
                continue

            elif op == 9:
                clear()
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
              "2. View All Recipes",
              "3. View Personal Recipes",
              "4. Sort Recipes",
              "5. Search Recipes",
              "6. Cook Recipe",
              "7. Edit a Recipe",
              "8. TOP 50 Recommended",
              "9. Get Recommendation",
              "10. Go Back to Main Menu", sep="\n")

        try:
            op = int(input(">"))

            if op == 1:
                clear()
                create_recipe(user)
                clear()
                continue

            elif op == 2:
                clear()
                display_all_recipes()
                continue
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
                clear()
                if cook_recipe(user):
                    clear()
                    continue
                break
            elif op == 7:
                clear()
                # get the recipe and pass to edit menu
                recipe = find_recipe_to_edit()
                if recipe is None:
                    continue
                elif isinstance(recipe, Recipe):
                    clear()
                    if edit_a_recipe_menu(recipe, user):
                        continue

            elif op == 8:
                clear()
                q = Query.get_best_fifty()
                for rec in q:
                    print(create_recipe_from_query(rec))
                input("press any key to close")
                return True
                clear()
            elif op == 9:
                clear()
                if get_a_recommendation(user):
                    continue
                break
            elif op == 10:
                continue

        except ValueError:
            clear()
            print("Incorrect option. Try again\n")
            continue


def get_a_recommendation(user: User):
    rec = Query.get_case_two_rec(user.username)
    if rec != []:
        print("We recommend: ")
        print(create_recipe_from_query(rec[0]))
    else:
        print("there are no recommendations available")
    input("Press any key to close")
    clear()
    return True

def add_pantry_item(user: User):
    name = input("Enter name: ")
    aisle = input("Enter aisle: ")
    exdate = input("Enter expire date (YYYY-MM-DD): ")
    quanity = input("Enter how item quantity: ")


    next_id = len(Query.get_items()) + 1
    Query.create_item(next_id, aisle, name, exdate)
    print("item created")
    Query.create_track(quanity, quanity, user.id, next_id)

    input("Press any key to close")
    clear()
    return True


def edit_pantry():
    name = input("Enter name of item you want to update: ")
    quantity = input("Enter the item quantity that you want to update: ")

    query = Query.get_item_ID_by_name(name)
    if query != []:
        Query.update_track(query[0], quantity)
        print("Updated the item quantity")
    else:
        print("Item doesn't exit")

    input("Press any key to close")
    clear()
    return True


def display_all_items():
    query = Query.get_items()

    print("=== Pantry ===")
    for item in query:
        print("Name: " + item[2])
        print("Aisle: " + str(item[1]))
        print("Expire date: " + item[3])
        print("========")

    input("Press any key to close")
    clear()
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
            elif op == 2:
                clear()
                edit_pantry()
            elif op == 3:
                clear()
                add_pantry_item(user)
            elif op == 4:
                return True
        except ValueError:
            clear()
            print("Incorrect option. Try again\n")
            continue


def user_edit_menu(user: User):
    while True:
        print("Choose an option",
              "================",
              "1. Edit Username",
              "2. Edit Password",
              "3. Go Back", sep="\n") #TODO

        try:
            op = int(input("> "))

            if op == 1:
                clear()
                name = input("Enter new Username or leave blank to cancel: ").strip()
                if name == "":
                    clear()
                    continue
                else:
                    if Query.update_user_name(user.ID, name):
                        clear()
                        print("Username Changed to {n}".format(n=name))
                        user.username = name
                        return True  # brings user back to previous menu
                    else:
                        print("That username is not available. Try again.")
                        continue

            elif op == 2:
                clear()
                passw = input("Enter new new Password or leave blank to cancel: ").strip()
                if passw == "":
                    clear()
                    continue
                else:
                    if Query.update_user_pass(user.ID, passw):
                        clear()
                        print("Password changed")
                        user.password = passw
                        # print(user)
                        return True  # go back to main menu

            elif op == 3:
                clear()
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
    print("Welcome back {name}!".format(name = user.username))
    while True:
        print("Choose an option",
              "================",
              "1. Recipe Book",
              "2. View Pantry",
              "3. Edit User Info", #TODO
              "4. Log Out", sep="\n") #TODO

        try:
            op = int(input("> "))

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
                clear()
                if user_edit_menu(user):
                    continue
            elif op == 4:

                clear()
                const = ". . . "
                message = "Logging you out"
                message = message + const
                print(message)

                for i in range(3):
                    time.sleep(0.5)
                    # remove a dot form message
                    message = message[:-2]
                    # clear and reprint message
                    clear()
                    print(message)
                time.sleep(0.5)
                # at the end clear and return
                clear()
                return True

        except ValueError:
            clear()
            print("Incorrect option. Try again.\n")
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
    returns True if user has logged out
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
            # print(query)
            # time.sleep(5)
            user = User(username, password, query[0][4])
            Query.update_user(username)
            if inner_menu(user):
                return True

        else:
            clear()
            print('Incorrect password. Try again.')
            login()


def register():
    """
    user registration
    returns True if user has logged out
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
        if inner_menu(user):
            return True


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
            op = int(input("> "))

            if op == 1:
                clear()
                if login():
                    continue
                break
            elif op == 2:
                clear()
                if register():
                    continue
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
