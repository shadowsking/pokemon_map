from django.db import models  # noqa F401


class Pokemon(models.Model):
    title = models.CharField(verbose_name="Название", max_length=200)
    title_en = models.CharField(verbose_name="Название на английском", max_length=200, blank=True)
    title_jp = models.CharField(verbose_name="Название на японском", max_length=200, blank=True)
    description = models.TextField(verbose_name="Описание", blank=True)
    previous_evolution = models.ForeignKey(
        "self",
        verbose_name="Предыдущая эволюция",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="next_evolutions"
    )
    image = models.ImageField(
        verbose_name="Изображение",
        upload_to="images/",
        blank=True,
        null=True
    )

    def __str__(self):
        return self.title


class PokemonEntity(models.Model):
    lat = models.FloatField(verbose_name="Широта")
    lon = models.FloatField(verbose_name="Долгота")
    pokemon = models.ForeignKey(
        Pokemon,
        verbose_name="Покемон",
        on_delete=models.CASCADE,
        related_name="entities"
    )
    appeared_at = models.DateTimeField(verbose_name="Дата и время появления", blank=True, null=True)
    disappeared_at = models.DateTimeField(verbose_name="Дата и время исчезновения", blank=True, null=True)
    level = models.IntegerField(verbose_name="Уровень", blank=True, null=True)
    health = models.IntegerField(verbose_name="Здоровье", blank=True, null=True)
    strength = models.IntegerField(verbose_name="Сила", blank=True, null=True)
    defence = models.IntegerField(verbose_name="Защита", blank=True, null=True)
    stamina = models.IntegerField(verbose_name="Выносливость", blank=True, null=True)

    def __str__(self):
        return "{title} - {level} lvl".format(
            title=self.pokemon.title,
            level=self.level
        )
