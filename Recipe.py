class Recipe:
    def __init__(self, recipe_id, name, description, servings, difficulty, steps, cooking_time, rating, username, categories, ingredients):
        self.recipe_id = recipe_id
        self.name = name
        self.description = description
        self.servings = servings
        self.difficulty = difficulty
        self.steps = steps
        self.cooking_time = cooking_time
        self.rating = rating
        self.username = username
        self.categories = categories
        self.ingredients = ingredients

    def __str__(self):
        builder = "Recipe #{id}".format(id = self.recipe_id) + "\n"
        builder += ("Name: {name}".format(name = self.name) + "\n")
        builder += ("Description: " + self.description) + "\n"
        builder += ("{d} servings".format(d = self.servings)) + "\n"
        builder += (self.difficulty + " difficulty") + "\n"
        builder += ("Steps: " + self.steps) + "\n" # TODO: Number the steps??
        builder += ("Time: {time} minutes".format(time = self.cooking_time)) + "\n"
        builder += ("Rating: " + '\u2605'*self.rating) + "\n"
        builder += ("Created by: {user}".format(user = self.username)) + "\n"
        return builder
