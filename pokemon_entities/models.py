from django.db import models  # noqa F401


class Pokemon(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(
        upload_to="images/",
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.title


class PokemonEntity(models.Model):
    lat = models.FloatField()
    lon = models.FloatField()
    pokemon = models.ForeignKey(
        Pokemon,
        on_delete=models.CASCADE,
    )
    appeared_at = models.DateTimeField(blank=True, null=True, )
    disappeared_at = models.DateTimeField(blank=True, null=True, )
    level = models.IntegerField(blank=True, null=True, )
    health = models.IntegerField(blank=True, null=True, )
    strength = models.IntegerField(blank=True, null=True, )
    defence = models.IntegerField(blank=True, null=True, )
    stamina = models.IntegerField(blank=True, null=True, )
