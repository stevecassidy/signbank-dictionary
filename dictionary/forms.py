from django import forms
import django
from .models import Dialect, Gloss, Definition, Relation, Region, defn_role_choices,\
    Relationrole
from django.conf import settings
from tagging.models import Tag

CATEGORY_CHOICES = getattr(settings, 'DICTIONARY_FILTER_TAGS', [])
# remove any tags that aren't tags
try:
    CATEGORY_CHOICES = [t for t in CATEGORY_CHOICES if Tag.objects.filter(name=t[0]).count() == 1]
except django.db.utils.OperationalError:
    pass
CATEGORY_CHOICES.insert(0, ('all', 'All'))

class UserSignSearchForm(forms.Form):

    query = forms.CharField(label='Keywords starting with', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'keyword'}), required=False)
    category = forms.ChoiceField(label='Search', choices=CATEGORY_CHOICES, required=False, widget=forms.Select(attrs={'class': 'form-control'}))

class DialectModelChoiceField(forms.ModelChoiceField):
    """Specialisation of ModelChoiceField that overrides the
    label_from_instance method for the Dialect model
    """

    def label_from_instance(self, obj):
        return obj.name

class SetRegionForm(forms.Form):

    region = DialectModelChoiceField(label="Dialect",
                                    queryset=Dialect.objects.all(),
                                    required=True,
                                    empty_label=None,
                                    widget=forms.Select(attrs={'class': 'form-control'}))


class GlossModelForm(forms.ModelForm):
    class Meta:
        model = Gloss
        # fields are defined in settings.py
        fields = settings.QUICK_UPDATE_GLOSS_FIELDS

class GlossCreateForm(forms.ModelForm):
    """Form for creating a new gloss from scratch"""
    class Meta:
        model = Gloss
        fields = ['idgloss', 'annotation_idgloss', 'sn']

    def clean_idgloss(self):
        """Ensure that idgloss has no '/' characters"""

        data = self.cleaned_data['idgloss']
        print("here we are", data)
        if '/' in data:
            raise forms.ValidationError("The '/' character is not allowed in an idgloss")

        return data



class TagUpdateForm(forms.Form):
    """Form to add a new tag to a gloss"""

    tag = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control'}),
                            choices=[(t, t) for t in settings.ALLOWED_TAGS])
    delete = forms.BooleanField(required=False, widget=forms.HiddenInput)

YESNOCHOICES = (("unspecified", "Unspecified" ), ('yes', 'Yes'), ('no', 'No'))


ROLE_CHOICES = [('all', 'All')]
ROLE_CHOICES.extend(defn_role_choices)

class GlossSearchForm(forms.ModelForm):

    search = forms.CharField(label="Search Gloss/SN")
    tags = forms.MultipleChoiceField(choices=[(t, t) for t in settings.ALLOWED_TAGS])
    nottags = forms.MultipleChoiceField(choices=[(t, t) for t in settings.ALLOWED_TAGS])
    keyword = forms.CharField(label='Keyword')
    hasvideo = forms.ChoiceField(label='Has Video', choices=YESNOCHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    defspublished = forms.ChoiceField(label="All Definitions Published", choices=YESNOCHOICES, widget=forms.Select(attrs={'class': 'form-control'}))

    defsearch = forms.CharField(label='Search Definition/Notes')
    defrole = forms.ChoiceField(label='Search Definition/Note Type', choices=ROLE_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = Gloss
        fields = ('idgloss', 'annotation_idgloss', 'morph', 'sense',
                   'sn', 'StemSN', 'comptf', 'compound', 'language', 'dialect',
                   'inWeb', 'isNew',
                   'initial_relative_orientation', 'final_relative_orientation',
                   'initial_palm_orientation', 'final_palm_orientation',
                   'initial_secondary_loc', 'final_secondary_loc',
                   'domhndsh', 'subhndsh', 'locprim', 'locsecond',
                   'final_domhndsh', 'final_subhndsh', 'final_loc'
                   )
        widgets = {
                   'inWeb': forms.Select(choices=YESNOCHOICES,attrs={'class': 'form-control'}),
                   'domhndsh': forms.Select(attrs={'class': 'form-control'}),
                   'subhndsh': forms.Select(attrs={'class': 'form-control'}),
                   'initial_relative_orientation': forms.Select(attrs={'class': 'form-control'}),
                   'final_relative_orientation': forms.Select(attrs={'class': 'form-control'}),
                   'initial_secondary_loc': forms.Select(attrs={'class': 'form-control'}),
                   'final_secondary_loc': forms.Select(attrs={'class': 'form-control'}),
                   'locprim': forms.Select(attrs={'class': 'form-control'}),
                   'final_domhndsh': forms.Select(attrs={'class': 'form-control'}),
                   'final_subhndsh': forms.Select(attrs={'class': 'form-control'}),
                   'final_loc': forms.Select(attrs={'class': 'form-control'}),
                   }


class DefinitionForm(forms.ModelForm):

    # optional video file uploaded with the new definition
    videofile = forms.FileField(label="", required=False)

    class Meta:
        model = Definition
        fields = ('count', 'role', 'text')
        widgets = {
                   'role': forms.Select(attrs={'class': 'form-control'}),
                   }

class RelationForm(forms.Form):

    sourceid = forms.CharField(label='Source Gloss')
    targetid = forms.CharField(label='Target Gloss')
    role = forms.ChoiceField(choices=[],widget=forms.Select(attrs={'class': 'form-control'}))

    def __init__(self, *args, **kwargs):
        super(RelationForm, self).__init__(*args, **kwargs)
        choices = []
        for role in Relationrole.objects.all():
            if role.forwardmessage == role.backwardmessage:
                choices.append(('%s_bidirectional' % role.role, role.forwardmessage))
            else:
                choices.append(('%s_forward' % role.role, role.forwardmessage))
                choices.append(('%s_backward' % role.role, role.backwardmessage))
        self.fields['role'].choices = choices

    class Meta:
        model = Relation
