from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Food, FoodName, HistamineInfo, InformationSource, FoodType, FoodTypeRelation

# Inline für FoodName und HistamineInfo, damit alles auf einer Food-Seite bearbeitet werden kann
# Die Felder von FoodName sollen innerhalb des AdminPanels in einem anderen Formular angezeigt werden
# -> TabularInline: FoodName ist sozusagen ein "Child-Formular" -> weiter unten sehen wir, dass es innerhalb des Parents (=Food) angezeigt wird
class FoodNameInline(admin.TabularInline):
    model = FoodName
    extra = 1  # wie viele leere Zeilen zum Hinzufügen neuer Elemente angezeigt werden (Standard ist 3)
    fields = ('language', 'name', 'is_primary')

# das Gleiche wie bei FoodNameInline, nur dass es ein StackedInline ist -> Felder werden untereinander angezeigt
class HistamineInfoInline(admin.StackedInline):
    model = HistamineInfo
    can_delete = False # Löschen von einem Eintrag im Fenster Food nicht möglich
    verbose_name_plural = 'Histamine Info'

# FoodTypeRelation ist die Relationstabelle von Food und FoodType -> wir wollen diese Tabelle in Food als Inline anzeigen
# damit wir die entsprechenden FoodType(s) dort direkt auswählen können
# Wenn man will, dass der Admin für einen Food mehrere FoodTypes auswählen kann, muss man die Relationstabelle als Inline anzeigen, NICHT DIE FOODTYPE TABELLE
class FoodTypeRelationInline(admin.TabularInline):
    model = FoodTypeRelation
    extra = 1

@admin.register(Food)
class FoodAdmin(admin.ModelAdmin): # Parent-Formular
    # Spalten, die in der Listenansicht aller Foods angezeigt werden
    # Primary Name ist eine Custom-Spalte, die nicht im Food-Model auftaucht
    # Was in dieser Spalte angezeigt wird, bestimmen wir in der primary_name()-Methode
    list_display = ('id', 'primary_name')

    # Detailansicht eines Foods: Zeige diese beiden Inlines (Child-Formulare) im Admin-Panel auf der Food-Seite an
    # In der Tabelle food selbst sind keine Felder drin (außer id) -> deswegen müssen wir hier sonst nichts anzeigen
    inlines = [FoodNameInline, HistamineInfoInline, FoodTypeRelationInline]

    # Diese Methode sorgt dafür, dass in der Listenansicht der zum Food zugehörige Primary-Name angezeigt wird
    def primary_name(self, obj):
        # Zieht zur dazugehörigen id den Primary-Name aus der DB
        primary = obj.foodname_set.filter(is_primary=True).first()
        return primary.name if primary else "(no primary name)"


@admin.register(FoodName)
class FoodNameAdmin(admin.ModelAdmin):
    # list_display: Spalten, die in der Listenansicht aller FoodNames angezeigt werden
    list_display = ('name', 'food', 'language', 'is_primary')

    # Spalten, die in der Listenansicht zum filtern genutzt werden können
    list_filter = ('language', 'is_primary')

    # Spalten, die durchsucht werden, wenn etwas ins Suchfeld eingegeben wird
    search_fields = ('name',)

@admin.register(HistamineInfo)
class HistamineInfoAdmin(admin.ModelAdmin):
    list_display = ('food', 'compatibility_score', 'rapid_histamine_formation', 'other_amines', 'liberator', 'blocker')
    list_filter = ('compatibility_score', 'rapid_histamine_formation', 'other_amines', 'liberator', 'blocker')
    search_fields = ('food__foodname__name',)

@admin.register(InformationSource)
class InformationSourceAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

# Adminseite zum Eintragen neuer FoodTypes
@admin.register(FoodType)
class FoodTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)