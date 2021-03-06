from django.contrib import admin
from .models import *
from reversion.admin import VersionAdmin


class KeywordAdmin(VersionAdmin):
    search_fields = ['^text']


class TranslationInline(admin.TabularInline):
    model = Translation
    extra = 1
    raw_id_fields = ['translation']


class DefinitionInline(admin.TabularInline):
    model = Definition
    extra = 1

class RelationInline(admin.TabularInline):
    model = Relation
    fk_name = 'source'
    raw_id_fields = ['source', 'target']
    verbose_name_plural = "Relations to other Glosses"
    extra = 1


from django.utils.translation import ugettext_lazy as _
from django.contrib.admin import SimpleListFilter


class SenseNumberListFilter(SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = _('number of senses')

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'senses'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        return (('none', _('No Senses')),
                ('morethanone', _('More than one')),
               )

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        # Decide how to filter the queryset based on the request
        if self.value() == 'none':
            return queryset.filter(sense__isnull=True)
        if self.value() == 'morethanone':
            return queryset.filter(sense__gte=1)


class RegionInline(admin.TabularInline):
    model = Gloss.dialect.through
    verbose_name_plural = "Regional information on dialects"


class GlossAdmin(VersionAdmin):
    fieldsets = ((None, {'fields': ('idgloss', 'annotation_idgloss', 'morph', 'sense',
                                    'sn', 'StemSN', 'comptf', 'compound', 'language', 'regional_template' )}, ),
                 ('Publication Status', {'fields': ('inWeb',  'isNew',  ),
                                       'classes': ('collapse',)}, ),
                 ('Phonology', {'fields': ('initial_palm_orientation', 'final_palm_orientation',
                                           'initial_relative_orientation', 'final_relative_orientation',
                                           'initial_secondary_loc', 'final_secondary_loc',
                                            'locprim', 'locsecond',  'final_loc',
                                            'domhndsh', 'subhndsh', 'final_domhndsh', 'final_subhndsh', ), 'classes': ('collapse',)}, ),
                 ('Obsolete Fields', {'fields': ('inittext', ), 'classes': ('collapse',)}),
              )
    save_on_top = True
    save_as = True
    list_display = ['idgloss', 'annotation_idgloss', 'morph', 'sense', 'sn']
    search_fields = ['^idgloss', '=sn', '^annotation_idgloss']
    list_filter = ['language', 'dialect', SenseNumberListFilter, 'inWeb', 'domhndsh']
    inlines = [ RegionInline, RelationInline, DefinitionInline, TranslationInline ]


class RegistrationProfileAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'activation_key_expired', )
    search_fields = ('user__username', 'user__first_name', )


class DialectInline(admin.TabularInline):
    model = Dialect


class DialectAdmin(VersionAdmin):
    model = Dialect
    list_display = ['name', 'index', 'language']


class LanguageAdmin(VersionAdmin):
    model = Language
    inlines = [DialectInline]


admin.site.register(Dialect, DialectAdmin)
admin.site.register(Language, LanguageAdmin)
admin.site.register(Gloss, GlossAdmin)
admin.site.register(Keyword, KeywordAdmin)
