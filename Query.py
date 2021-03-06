import psycopg2
from datetime import date

conn = psycopg2.connect(
    host="reddwarf.cs.rit.edu",
    database="p32001c",
    user="p32001c",
    password="Cebai4xoorahquahleuw"
)

cur = conn.cursor()


def create_recipe(recipe_id, name, description, servings, difficulty, steps, cooking_time, rating, username, categories, ingredients):

    cur.execute('INSERT INTO "Recipe" ("Recipe_ID", "Recipe_Name", "Description", "Servings", '
                '"Difficulty", "Steps", "Cooking_Time", "Rating", "Author_Username", "Creation_Date") '
                'VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
                (recipe_id, name, description, servings, difficulty, steps, cooking_time, rating, username, date.today()))

    conn.commit()
    for cat in categories:
        create_category(cat, recipe_id)

    for ing in ingredients:
        item = ing.split(":")
        item_name = item[0]
        quantity = item[1]
        result = get_ingredient(item_name)
        if result != [] and len(result[0]) >= 1:
            item_id = result[0][0]
            create_ingredient(item_id, recipe_id, quantity)


def update_recipe(attribute, change, recipe_id):
    try:
        cur.execute(('UPDATE "Recipe" SET "' + str(attribute) + '" = %s WHERE "Recipe_ID" = %s'), [change, recipe_id])
        conn.commit()

    except Exception as e:
        print(e)
        print("Could not update recipe")


def delete_recipe(recipe_id):

    try:
        cur.execute('DELETE FROM "Recipe" WHERE "Recipe_ID" = %s', [recipe_id])
        conn.commit()

    except Exception:
        print("Could not delete recipe")


def create_user(username, password, id):

    try:
        cur.execute('INSERT INTO "User" ("Username", "Password", "Creation_Date", "Last_Access_Date", "User_ID") '
                    'VALUES (%s, %s, %s, %s, %s)',
                    (username, password, date.today(), date.today(), id))
        conn.commit()
    except:
        print("Can't create user")


def update_user(name):
    try:
        cur.execute('UPDATE "User" SET "Last_Access_Date" = %s where "Username" = %s', [date.today(), name])
        conn.commit()
    except:
        print("Could not update user")


def get_ingredient(ing):
    try:
        cur.execute('SELECT "Item"."Item_ID" FROM "Item" WHERE "Item_Name" = %s', [ing])
        return cur.fetchall()

    except:
        print("Can't grab ingredient")


def create_ingredient(item_id, id, quantity):
    try:
        cur.execute('INSERT INTO "Ingredients" ("Item_ID", "Recipe_ID", "Quantity_Needed") VALUES(%s, %s, %s)', (item_id, id, quantity))
        conn.commit()

    except:
        print("Could not create Ingredient")


def delete_ingredient(id):
    try:
        cur.execute('DELETE FROM "Ingredients" WHERE "Recipe_ID" = %s', id)
        conn.commit()

    except:
        print("Could not delete ingredient")


def create_category(cat, id):
    try:
        cur.execute('INSERT INTO "Categories" ("Category", "Recipe_ID") VALUES(%s, $s)', (cat, id))
        conn.commit()

    except:
        print("Could not create category")


def delete_category(id):
    try:
        cur.execute('DELETE FROM "Categories" WHERE "Recipe_ID" = %s', id)
        conn.commit()

    except:
        print("Could not delete category")


def create_item(id, aisle, name, date):
    try:
        cur.execute('INSERT INTO "Item" ("Item_ID", "Aisle", "Item_Name", "Expiration_Date") VALUES (%s, %s, %s, %s)',
                    (id, aisle, name, date))
        conn.commit()
    except:
        print("Could not create item")


def get_items():
    try:
        cur.execute('SELECT * FROM "Item"')
        return cur.fetchall()
    except:
        print("Could not get Items")


def update_track(id, value):
    try:
        cur.execute('UPDATE "Track" SET "Current_Quantity" = %s where "Item_ID" = %s', [value, id])
        conn.commit()
    except:
        print("Could not update item")

def create_track(quanBought, currQuant, ownerID, itemID):
    try:
        cur.execute('INSERT INTO "Track" ("Purchase_Date", "Quantity_Bought", "Current_Quantity", "Owner_User_ID", "Item_ID" ) VALUES (%s, %s, %s, %s, %s)',
                    (date.today(), quanBought, currQuant, ownerID, itemID ))
        conn.commit()
    except:
        # print("Could not create item")
        pass


def get_track():
    try:
        cur.execute('SELECT * FROM "Track"')
        return cur.fetchall()

    except:
        print("Could not grab tracks")


def get_users():
    try:
        cur.execute('SELECT * FROM "User"')
        return cur.fetchall()
    except:
        print("Could not get Users")


def get_user(username: str):

    cur.execute('SELECT * FROM "User" where "Username" = %s', [username])
    return cur.fetchall()


def get_recipe():
    try:
        cur.execute('SELECT * FROM "Recipe"')
        return cur.fetchall()
    except:
        print("Could not get Recipe")


def get_user_recipe(name: str):
    cur.execute('SELECT * FROM "Recipe" where "Author_Username" = %s', [name])
    return cur.fetchall()


def get_recipe_by_name(name: str):
    cur.execute('SELECT * FROM "Recipe" where "Recipe_Name" ~* %s ORDER BY "Recipe_Name"', [name])
    return cur.fetchall()


def get_recipe_by_cate(cate: str):
    cur.execute('SELECT * FROM "Recipe" where "Recipe_ID" IN '
                '(SELECT "Recipe_ID" FROM "Categories" where "Category" = %s) ORDER BY "Recipe_Name"', [cate])
    return cur.fetchall()


def get_recipe_by_ing(ing: str):
    cur.execute('SELECT * FROM "Recipe" where "Recipe_ID" IN '
                '(SELECT "Recipe_ID" FROM "Ingredients" where "Item_ID" IN'
                '(SELECT "Item_ID" FROM "Item" where "Item_Name" = %s)) ORDER BY "Recipe_Name"', [ing])
    return cur.fetchall()


def sort_recipes_by_category_ASC():
    cur.execute('SELECT * FROM "Recipe" as "r"'
                'JOIN "Categories" as "c" on c."Recipe_ID" = r."Recipe_ID"'
                'ORDER BY "Category" ASC')

    return cur.fetchall()

def sort_recipes_by_category_DESC():
    cur.execute('SELECT * FROM "Recipe" as "r"'
                'JOIN "Categories" as "c" on c."Recipe_ID" = r."Recipe_ID"'
                'ORDER BY "Category" DESC')
    return cur.fetchall()


def sort_recipes_by_alphabetical_ASC():
    cur.execute('SELECT * FROM "Recipe" ORDER BY "Recipe_Name" ASC')
    return cur.fetchall()

def sort_recipes_by_alphabetical_DESC():
    cur.execute('SELECT * FROM "Recipe" ORDER BY "Recipe_Name" DESC')
    return cur.fetchall()

def sort_recipes_by_rating_ASC():
    cur.execute('SELECT * FROM "Recipe" ORDER BY "Rating" ASC')
    return cur.fetchall()

def sort_recipes_by_rating_DESC():
    cur.execute('SELECT * FROM "Recipe" ORDER BY "Rating" DESC')
    return cur.fetchall()


def sort_recipes_by_recency_ASC():

    cur.execute('SELECT * FROM "Recipe" ORDER BY "Creation_Date" DESC')
    return cur.fetchall()

def sort_recipes_by_recency_DESC():
    cur.execute('SELECT * FROM "Recipe" ORDER BY "Creation_Date" ASC')
    return cur.fetchall()


def mark_recipe(userID, recipeID, scale):
    cur.execute('SELECT * FROM "Recipe" WHERE "Recipe_ID" = %s', (recipeID,))
    recipe = cur.fetchone()
    if recipe is None or len(recipe) == 0:
        print("Recipe does not exist")
        return
    else:
        cur.execute('SELECT "Item_ID" FROM "Ingredients" WHERE "Recipe_ID" = %s', (recipeID,))
        ingredientIDs = cur.fetchall()

        for i in ingredientIDs:
            cur.execute('SELECT "Quantity_Needed" FROM "Ingredients" WHERE "Recipe_ID" = %s'
                        'AND "Item_ID" = %s', (recipeID, i[0]))
            neededQuantity = cur.fetchone()[0]
            scaledQuantity = neededQuantity * scale
            cur.execute('SELECT "Current_Quantity" FROM "Track" WHERE "Owner_User_ID" = %s AND "Item_ID" = %s', (userID, i[0]))
            quantityOwned = cur.fetchone()
            if quantityOwned is None or len(quantityOwned) == 0:
                print("Not enough quantity to make recipe.")
                return False
            quantityOwned = int(quantityOwned[0])
            quantityRemaining = quantityOwned - scaledQuantity
            if quantityRemaining >= 0:
                cur.execute('UPDATE "Track" SET "Current_Quantity" = %s'
                            'WHERE "Owner_User_ID" = %s AND "Item_ID" = %s', (quantityRemaining, userID, i))
            else:
                print("Not enough quantity to make recipe.")
                return False

    conn.commit()
    return True


def update_user_name(id: str, name: str) -> bool:
    """
    query to update username
    :param id: id of the user
    :param name: new name to make update
    :return: boolean if the query is successful, false otherwise
    """
    try:
        cur.execute('UPDATE "User" SET "Username" = %s WHERE "User_ID" = %s', (name, id))
        conn.commit()
        return True
    except Exception as e:
        # print(e)
        return False


def update_user_pass(id: str, passw: str) -> bool:
    """
    query that updates user password
    :param id: id of the user
    :param passw: password to make te update
    :return: boolean if the query is successful, false otherwise
    """
    try:
        cur.execute('UPDATE "User" SET "Password" = %s WHERE "User_ID" = %s', (passw, id))
        conn.commit()
        return True
    except Exception as e:
        # print(e)
        return False


def get_categories_of_recipe(id: int) -> []:
    """
    returns a list of categories that a recipe belongs to
    :param id: id of the recipe
    :return: collection of categories; [] if None
    """
    cur.execute('SELECT * From "Categories" WHERE "Recipe_ID" = %s', [id])
    return cur.fetchall()


def get_ingredients_of_recipe(id: int) -> []:
    """
    gets the ingredients of a given recipe
    :param id: id of the recipe
    :return: collection of ingredients; [] if None found
    """
    cur.execute('SELECT * From "Ingredients" WHERE "Recipe_ID" = %s', [id])
    return cur.fetchall()


def get_item_by_id(id: int) -> []:
    """
    finds an item given an ID
    :param id: id of the item
    :return: item if found. Though item is always guaranteed to exist since we have its ID
    """
    cur.execute('SELECT "Item_Name" FROM "Item" WHERE "Item_ID" = %s', [id])
    return cur.fetchall()


def get_item_ID_by_name(name: str):
    cur.execute('SELECT "Item_ID" FROM "Item" WHERE "Item_Name" = %s', [name])
    return cur.fetchall()

def add_to_history(user_id, recipe_id):
    cur.execute('INSERT INTO "History" ("User_ID", "Recipe_ID") VALUES (%s, %s)', [user_id, recipe_id])
    conn.commit()


def get_case_one_rec(username: str):
    """
    Recommends the highest rated recipe from the food category the user likes the most
    :return: TODO
    """
    query = """SELECT *
From "Recipe", "Categories"
WHERE "Author_Username" = %s
  AND "Recipe"."Recipe_ID" = "Categories"."Recipe_ID"
  AND "Category" = (SELECT "Category"
FROM "Categories", "Recipe"
WHERE "Author_Username" = %s AND "Recipe"."Recipe_ID" = "Categories"."Recipe_ID"
GROUP BY "Category"
order by Count("Category") DESC
LIMIT 1)
ORDER BY "Rating" DESC
LIMIT 1"""
    cur.execute(query, [username, username])
    return cur.fetchall()

def get_case_two_rec(username: str):
    query = """
    SELECT *
FROM "Recipe", "History"
WHERE "History"."Recipe_ID" = "Recipe"."Recipe_ID"  AND "History"."User_ID" = (SELECT "User"."User_ID" FROM "User" WHERE "Username" = %s)
ORDER BY "Recipe"."Rating" DESC 
LIMIT 1"""
    cur.execute(query, [username])
    return cur.fetchall()


def get_best_fifty():
    cur.execute('SELECT * FROM "Recipe" ORDER BY "Rating" DESC LIMIT 50')
    return cur.fetchall()

def get_able_to_made_recipe():
    cur.execute('SELECT * FROM "Recipe" WHERE "Recipe_ID" IN (SELECT "Recipe_ID" FROM "Ingredients", "Track" WHERE "Quantity_Needed" = "Track"."Current_Quantity" AND "Ingredients"."Item_ID" = "Track"."Item_ID")')
    return cur.fetchall()
