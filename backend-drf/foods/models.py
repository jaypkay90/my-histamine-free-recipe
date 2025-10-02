from django.db import models
from django.db.models import Q, UniqueConstraint

# Create your models here.
class Food(models.Model):
    pass # nur ID als PK bei dieser Tabelle -> wird automatisch erstellt -> id = AutoField(primary_key=True)

    def __str__(self):
        return f"Food - ID:{self.id}"

class InformationSource(models.Model):
    name = models.CharField(max_length=50, unique=True) # CharField ist standardmäßig null=False

    def __str__(self):
        return self.name

# HistamineInfo
# „Yes / No / Unknown“
# Die auskommentierte Wahl ist schlechter, weil wir keine enums benutzen. Wenn Daten nur über das Admin-Panel eingegeben werden, ist das okay.
# Dort wird nämlich ein Drop-Down angezeigt. Wird die Datenbank aber auch anders gefüllt, ist das schlecht, denn es könnten auch andere Werte 
# eingegeben werden. Aus diesem Grund sollte hier besser ein Enum verwendet werden.
'''YNU_CHOICES = [
    # Tuple mit zwei Einträgen: ('Datenbankwert' - dieser Wert wird in der DB gespeichert , 'Anzeigewert - dieser wird im Frontend angezeigt')
    # Tuple Basics: immutable, indexierbar und iterierbar
    ('true','true'),
    ('false','false'),
    ('unknown','unknown'),
]'''

# Implementation der Auswahlmöglichkeiten als Enum
class YNUChoice(models.TextChoices):
    # Tuple mit zwei Einträgen: ('Datenbankwert' - dieser Wert wird in der DB gespeichert , 'Anzeigewert - dieser wird im Frontend angezeigt')
    TRUE = ('true', 'true')
    FALSE = ('false', 'false')
    UNKNOWN = ('unknown', 'unknown')

class CompatibilityScore(models.TextChoices):
    ZERO = ('0', '0')
    ONE = ('1', '1')
    TWO = ('2', '2')
    THREE = ('3', '3')
    UNKNOWN = ('unknown', 'unknown')


class HistamineInfo(models.Model):
    # Um den Spaltennamen für einen Foreign Key in der DB zu speichern, hängt Django automatisch die "_id" an das Attribut an
    # -> Hier entsteht in der DB also die Spalte food_id
    food = models.OneToOneField(Food, on_delete=models.CASCADE, primary_key=True)

    # choices=im Admin-Interface bzw. in der API-Ansicht wird ein Dropdown-Menü angezeigt
    # Warum CharField? -> es gibt in Django keine direkten Enum-Felder -> das Ganze wird über CharField + TextChoices umgesetzt
    # Im Admin-Interface/Formular wird die Auswahl in einem Dropdown-Menü angezeigt -> so landen letztlich nur gültige Werte in die DB
    compatibility_score = models.CharField(max_length=10, choices=CompatibilityScore.choices, default=CompatibilityScore.UNKNOWN) # CharField ist standardmäßig null=False
    rapid_histamine_formation = models.CharField(max_length=10, choices=YNUChoice.choices, default=YNUChoice.UNKNOWN)
    other_amines = models.CharField(max_length=10, choices=YNUChoice.choices, default=YNUChoice.UNKNOWN)
    liberator = models.CharField(max_length=10, choices=YNUChoice.choices, default=YNUChoice.UNKNOWN)
    blocker = models.CharField(max_length=10, choices=YNUChoice.choices, default=YNUChoice.UNKNOWN)
    notes = models.TextField(blank=True)
    information_source = models.ForeignKey(InformationSource, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"HistamineInfo - food_id: {self.food_id}, compatibility_score: {self.compatibility_score}"

# FoodName
class FoodName(models.Model):
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
    language = models.CharField(max_length=5)
    name = models.CharField(max_length=250)
    is_primary = models.BooleanField(default=False)

    class Meta:
        constraints = [
            # Kombination aus food_id, language und name muss einzigartig sein -> sonst könnte es Duplikate geben
            # Kein doppelter Name in derselben Sprache für dasselbe food
            models.UniqueConstraint(fields=['food','language','name'], name='uniq_foodname'),

            # Es darf für jedes Lebensmittel + Sprache nur ein Primary Name geben (is_primary=True)
            # Beispiel: Apfel ist Primary Name, aber es gibt auch noch Äpfel in der DB unter der gleichen Id
            UniqueConstraint(fields=['food','language'], condition=Q(is_primary=True), name='uniq_primary_foodname')
        ]
    
    def __str__(self):
        return f"{self.name} ({self.language})"
    

# FoodType
class FoodType(models.Model):
    name = models.CharField(max_length=250, unique=True)

    def __str__(self):
        return self.name


# Food_FoodType
class FoodTypeRelation(models.Model):
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
    food_type = models.ForeignKey(FoodType, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            # PK = (food_id, food_type_id)
            # -> Kombination aus food_id und food_type_id muss einzigartig sein -> sonst könnte es Duplikate geben
            models.UniqueConstraint(fields=['food','food_type'], name='uniq_food_foodtype')
        ]
    
    def __str__(self):
        return f"{self.food} -> {self.food_type}"