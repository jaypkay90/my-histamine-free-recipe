from rest_framework import serializers
from foods.models import Food, FoodName, HistamineInfo, FoodTypeRelation

'''Serialization: Objekte aus der Datenbank, werden in ein Format umgewandelt, 
    das an das Frontend geschickt werden kann, meist JSON. Serializer sind sozusagen Übersetzer.
    Desireralization: Das Frontend schickt Daten im JSON-Format, die hier von einem Desirializer in Python-Objekte umgewandelt werden, 
    damit sie weiterverarbeitet werden können. 
    Manual Serialization: Der Code, der die Objekte in JSON umwandelt und ans Frontend weitergibt, wird selbst geschrieben
    Django Serializers: Django bietet Serializer an, die komplexe Datentypen in JSON oder XML umwandeln können. Am gängisten ist der Model-Serializer, 
    der Model-Objekte/Datenbankfelder in JSON oder XML umwandelt'''

# Die Klasse ModelSerializer schaut sich das Model in der Meta-Klasse und die spezifizierten Felder an
# Sie erstellt dann automatisch die Felder für den Serializer inkl. Validierungsregeln basierend auf den Model-Definitionen (z. B. blank=False, unique=True, max_length=250).
# Wenn Daten vom Backend ans Frontend geschickt werden (Serialization), wandelt der Serializer die Python-Objekte/Models in z. B. JSON um.
# Wenn Daten vom Frontend ans Backend geschickt werden (Deserialization), validiert der Serializer die Daten und ruft – falls alles gültig ist – create() oder update() auf, 
# um die Daten ins Model zu speichern.
class FoodNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodName

        # Der Serializer definiert explizit, welche Felder der Models in über die API-Schnittstelle abrufbar sein sollen
        # die Id anzuzeigen macht hier z.B. wenig Sinn
        fields = ['language', 'name', 'is_primary']


class HistamineInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistamineInfo
        fields = [
            'compatibility_score',
            'rapid_histamine_formation',
            'other_amines',
            'liberator',
            'blocker',
            'notes'
        ]

# Seiralizer für die Tabelle Matching-Tabelle Food - FoodType
class FoodTypeRelationSerializer(serializers.ModelSerializer):
    # Die Relationstabelle selbst hat kein Feld food_type_name, aber genau den Namen des FoodTypes wollen wir beim API-Call anzeigen
    # source='food_type.name' sagt DRF: "Zieh den Wert aus der Tabelle food_type, Spalte name"
    food_type_name = serializers.CharField(source='food_type.name', read_only=True)

    class Meta:
        model = FoodTypeRelation
        fields = ['food_type_name']


class FoodSerializer(serializers.ModelSerializer):
    # Nested Serializer: Die Informationen zu HistamineInfo und FoodName sollen im Food abgebildet werden
    # Normalerweise müsste man im Food-Model ein related_name Attribut definieren
    # Allerdings erzeugt Django bei ForeignKey-Feldern und OneToOne-Feldern automatisch ein set, das alle Infos erhält -> Klassenname + _set
    # Beispiel: Klasse FoodName: foodname_set -> Das geben wir hier als source an
    food_names = FoodNameSerializer(source='foodname_set', many=True, read_only=True)
    food_types = FoodTypeRelationSerializer(source='foodtyperelation_set', many=True, read_only=True)

    # Bei OneToOne-Feldern erzeugt Django Folgendes: Name der Klasse am anderen Ende der Beziehung -> hier histamineinfo
    histamine_info = HistamineInfoSerializer(source='histamineinfo', read_only=True)

    class Meta:
        model = Food
        fields = ['id', 'food_names', 'histamine_info', 'food_types']
