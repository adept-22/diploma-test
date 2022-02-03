from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator

User = get_user_model()

# Ингридиенты
class Ingredient(models.Model):
    name = models.CharField(
        max_length=200,
        unique=True,
        db_index=True,
        verbose_name='Название'
    )
    unit = models.CharField(
        max_length=200,
        verbose_name='Еденица измерения'
    )

    class Meta:
        ordering = ['id']
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return self.name

# Теги
class Tag(models.Model):
    name = models.CharField(
        max_length=200,
        unique=True,
        db_index=True,
        verbose_name='Тег'
    )
    color = models.CharField(
        max_length=7,
        blank=True,
        verbose_name='Цвет'
    )
    slug = models.CharField(
        max_length=200,
        unique=True,
        blank=True,
        verbose_name='Слаг'
    )

    class Meta:
        ordering = ['id']
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name

# Рецепты
class Recipe(models.Model):
    name = models.CharField(
        max_length=200,
        unique=True,
        db_index=True,
        verbose_name='Название'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='user_recipes',
        verbose_name='Автор'
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='RecipeIngredients',
        related_name='recipes', #наверно удалить надо
        verbose_name='Ингридиенты'
    )
    tags = models.ManyToManyField(
        Tag,
        through='RecipeTags',
        related_name='recipes', #наверно удалить надо
        verbose_name='Тег'
    )
    picture = models.ImageField(
        upload_to='picture/',
        verbose_name='Изображение'
    )
    text = models.TextField(
        verbose_name='Описание'
    )
    cooking_time = models.IntegerField(
        verbose_name='Время приготовления',
        validators = [
            MinValueValidator(
                1, message='Время приготовления должно не меньше 1 минуты!'
            )
        ]
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации'
    )

    class Meta:
        ordering = ['id']
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name

# Ингридиенты рецептов
class RecipeIngredients(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        db_index=True,
        related_name='ingredient_list',
        verbose_name='Рецепт'
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='recipes_list',
        verbose_name='Ингридиент'
    )
    number = models.PositiveSmallIntegerField(
        verbose_name='количество',
        validators=[
            MinValueValidator(
                1, message='Количество ингридиента не менее 1!'
            )
        ]
    )

    class Meta:
        ordering = ['recipe', 'ingredient']
        unique_together = ('recipe', 'ingredient')
        verbose_name = 'Ингридиент рецепта'
        verbose_name_plural = 'Ингридиенты рецептов'

    def __str__(self):
        return f'рецепт: {self.recipe.name} ингридиент: {self.ingredient.name} количество: {self.number}'

# Теги рецептов
class RecipeTags(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='tags_list',
        verbose_name='Рецепт'
    )
    tag = models.ForeignKey(
        Tag,
        on_delete=models.CASCADE,
        related_name='recipes_list',
        verbose_name='Тег'
    )

    class Meta:
        ordering = ['id']
        unique_together = ('recipe', 'tag')
        verbose_name = 'Тег рецепта'
        verbose_name_plural = 'Теги рецептов'

    def __str__(self):
        return f'рецепт: {self.recipe.name} таг: {self.tag.name}'

# Список покупок
class ShoppingList(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='shopping_list',
        verbose_name='Пользователь'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='shopping_lists',
        verbose_name='Рецепт'
    )

    class Meta:
        ordering = ['id']
        unique_together = ('user', 'recipe')
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Списки покупок'

    def __str__(self):
        return self.recipe.name

# Подписки
class Subscription(models.Model):
     user = models.ForeignKey(
         User,
         on_delete=models.CASCADE,
         related_name='following',
         verbose_name='Пользователь'
     )
     author = models.ForeignKey(
         User,
         on_delete=models.CASCADE,
         related_name='followed',
         verbose_name='Автор'
     )

     class Meta:
         ordering = ['id']
         unique_together = ('user', 'author')
         verbose_name = 'Подписка'
         verbose_name_plural = 'Подписки'

     def __str__(self):
         return f'{self.user.username} подписан на {self.author.username}'

# Избранное
class Favorites(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='selected_recipes',
        verbose_name='Пользователь'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='selected_users',
        verbose_name='Рецепт'
    )

    class Meta:
        ordering = ['id']
        unique_together = ('user', 'recipe')
        verbose_name = 'Избранное'
        verbose_name_plural = 'Списки избранного'

    def __str__(self):
        return f'{self.recipe.name} в избранном {self.user.username}'