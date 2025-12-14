from django import forms
from .models import Booking


class BookingForm(forms.ModelForm):
    # Override the reservation_slot field with a ChoiceField that accepts integers
    reservation_slot = forms.ChoiceField(
        choices=[],
        widget=forms.Select(attrs={
            'class': 'form-control',
            'id': 'reservation_slot'
        }),
        label='Reservation Slot'
    )
    
    class Meta:
        model = Booking
        fields = ['first_name', 'reservation_date', 'reservation_slot']
        
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your first name',
                'id': 'first_name'
            }),
            'reservation_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
                'id': 'reservation_date'
            }),
        }
        
        labels = {
            'first_name': 'First Name',
            'reservation_date': 'Reservation Date',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set the reservation slot choices with all available slots
        self.fields['reservation_slot'].choices = [
            ('', '-- Select a time slot --'),
            ('10', '10:00 AM'),
            ('11', '11:00 AM'),
            ('12', '12:00 PM'),
            ('13', '1:00 PM'),
            ('14', '2:00 PM'),
            ('15', '3:00 PM'),
            ('16', '4:00 PM'),
            ('17', '5:00 PM'),
            ('18', '6:00 PM'),
            ('19', '7:00 PM'),
            ('20', '8:00 PM'),
        ]
        
        # Make the fields required
        self.fields['first_name'].required = True
        self.fields['reservation_date'].required = True
        self.fields['reservation_slot'].required = True

