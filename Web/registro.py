from django import forms
from . models import Usuario,Agencia

class RegistroFrom(forms.ModelForm):
    agencia = forms.ModelChoiceField(queryset=Agencia.objects.all())
    class Meta:
        model = Usuario
        fields = [
            'user', 
            'password', 
            'nombre', 
            'apellido', 
            'mail',
            'agencia',
        ]
class RegistroAgencia(forms.ModelForm):
    class Meta:
        model=Agencia
        fields=[
            'nombre',
            'direccion',
            'piso',
        ]
class LoginForm(forms.Form):
    user = forms.CharField(max_length=30, required=True)
    password = forms.CharField(widget=forms.PasswordInput, max_length=10, required=True)


     
