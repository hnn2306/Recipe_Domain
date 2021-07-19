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