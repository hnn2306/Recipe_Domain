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
        result = get_ingredient(ing)
        if result.rows.length >= 1:
            item_id = result.rows[0].Item_ID
            create_ingredient(item_id, recipe_id)


def update_recipe(attribute, change, recipe_id):
    try:
        cur.execute('UPDATE "Recipe" SET "%s" = "%s" WHERE "Recipe_ID" = %s', attribute, change, recipe_id)
        conn.commit()

    except:
        print("Could not update recipe")


def delete_recipe(recipe_id):
    delete_category(recipe_id)
    delete_ingredient(recipe_id)
    try:
        cur.execute('DELETE FROM "Recipe" WHERE "Recipe_ID" = %s', recipe_id)
        conn.commit()

    except:
        print("Could not delete recipe")


def create_user(username, password, id):

    try:
        cur.execute('INSERT INTO "User" ("Username", "Password", "Creation_Date", "Last_Access_Date", "User_ID") '
                    'VALUES (%s, %s, %s, %s, %s)',
                    (username, password, date.today(), date.today(), id))
        conn.commit()
    except:
        print("Can't create user")


def update_user(id):
    try:
        cur.execute('UPDATE "User" SET "Last_Access_Date" = %s where "User_ID" = %s', date.today(), id)
        conn.commit()
    except:
        print("Could not update user")


def get_ingredient(ing):
    try:
        cur.execute('SELECT "Item"."Item_ID" FROM "Item", "Ingredients" WHERE "Ingredients"."Item_ID" = '
                    '"Item"."Item_ID" AND "Item"."Item_Name" = %s', ing)
        return cur.fetchall()

    except:
        print("Can't grab ingredient")


def create_ingredient(item_id, id):
    try:
        cur.execute("INSERT INTO 'Ingredients' ('Item_ID', 'Recipe_ID') VALUES(%s, %s)", (item_id, id))
        conn.commit()

    except:
        print("Could not create Ingredient")


def delete_ingredient(id):
    try:
        cur.execute("DELETE FROM 'Ingredients' WHERE 'Recipe_ID' = %s", id)
        conn.commit()

    except:
        print("Could not delete ingredient")


def create_category(cat, id):
    try:
        cur.execute("INSERT INTO 'Categories' ('Category', 'Recipe_ID') VALUES(%s, $s)", (cat, id))
        conn.commit()

    except:
        print("Could not create category")


def delete_category(id):
    try:
        cur.execute("DELETE FROM 'Categories' WHERE 'Recipe_ID' = %s", id)
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


def update_track():
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
        print("Could not get Recipes")


def get_user_recipe(name: str):
    cur.execute('SELECT * FROM "Recipe" where "Author_Username" = %s', [name])
    return cur.fetchall()
