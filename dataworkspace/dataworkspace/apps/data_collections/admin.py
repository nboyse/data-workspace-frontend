from django.contrib import admin
from dataworkspace.apps.core.admin import DeletableTimeStampedUserAdmin

from dataworkspace.apps.data_collections.models import (
    Collection,
    CollectionDatasetMembership,
    CollectionVisualisationCatalogueItemMembership,
)


class CollectionDatasetMembershipAdmin(admin.TabularInline):
    model = CollectionDatasetMembership
    extra = 1
    autocomplete_fields = ("collection",)


class CollectionVisualisationCatalogueItemMembershipAdmin(admin.TabularInline):
    model = CollectionVisualisationCatalogueItemMembership
    extra = 1
    autocomplete_fields = ("collection",)


class CollectionAdmin(DeletableTimeStampedUserAdmin):
    list_display = ("name", "description", "owner")
    search_fields = ["name"]
    fieldsets = [
        (
            None,
<<<<<<< HEAD
            {"fields": ["name", "description", "owner", "id"]},
=======
            {"fields": ["published", "name", "description", "owner", "id", "notes"]},
>>>>>>> 678e892c (adding notes feature to django admin)
        ),
    ]
    readonly_fields = ["id"]
    inlines = (
        CollectionDatasetMembershipAdmin,
        CollectionVisualisationCatalogueItemMembershipAdmin,
    )


admin.site.register(Collection, CollectionAdmin)
