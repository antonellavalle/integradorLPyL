from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

"""La clase SignUpForm es un formulario personalizado basado en UserCreationForm que se utiliza para registrar nuevos usuarios.
    Incluye campos adicionales para el correo electrónico, nombre de usuario, primer nombre y apellido. La clase define un 
    método clean para validar que las contraseñas coincidan y un método save para guardar los datos del formulario en la base 
    de datos."""
class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Enter a valid email address.')  # Campo para el correo electrónico con validación de longitud máxima y mensaje de ayuda
    username = forms.CharField(max_length=30, required=True, help_text='Required.')  # Campo para el nombre de usuario con validación de longitud máxima y mensaje de ayuda
    first_name = forms.CharField(max_length=30, required=True, help_text='Required.')  # Campo para el primer nombre con validación de longitud máxima y mensaje de ayuda
    last_name = forms.CharField(max_length=30, required=True, help_text='Required.')  # Campo para el apellido con validación de longitud máxima y mensaje de ayuda

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2',)  # Meta clase para definir el modelo asociado y los campos que se van a utilizar en el formulario

    def clean(self):
        """Método para limpiar y validar los datos del formulario"""
        cleaned_data = super().clean()  # Llama al método clean del formulario padre para obtener los datos ya limpiados
        password1 = cleaned_data.get("password1")  # Obtiene el valor del campo password1
        password2 = cleaned_data.get("password2")  # Obtiene el valor del campo password2

        if password1 and password2 and password1 != password2:  # Verifica si las contraseñas coinciden, si no, lanza una excepción de validación
            raise forms.ValidationError("Las contraseñas no coinciden.")

        return cleaned_data  # Retorna los datos limpiados y validados

    def save(self, commit=True):
        """Método para guardar los datos del formulario en la base de datos"""
        user = super(UserCreationForm, self).save(commit=False)  # Llama al método save del formulario padre (UserCreationForm) sin guardar aún en la base de datos
        user.username = self.cleaned_data['username']  # Asigna los valores limpiados del formulario a los campos correspondientes del modelo User
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']

        if commit:  # Si commit es True, guarda el usuario en la base de datos
            user.save()
        return user  # Retorna la instancia del usuario


