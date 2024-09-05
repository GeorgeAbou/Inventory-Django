
from django import forms
from django.contrib.auth import authenticate
from .models import Producto,Categoria
#


#formulario login
class LoginForm(forms.Form):
    usuario=forms.CharField(label='Usuario',max_length=50)
    contraseña=forms.CharField(  
        label='Contraseña',
        #para que aparesca *** en el form al introducir el passsword
        widget=forms.PasswordInput
    )
    #Implementar la lógica de validación y limpieza personalizada
    def clean(self) :
        cleaned_data = super().clean()
        username = cleaned_data.get('usuario')
        password = cleaned_data.get('contraseña')

        #validar
        if username and password:
            user=authenticate(username=username,password=password)
            if user is None:
                raise forms.ValidationError('Nombre de usuario o contraseña incorrectos.')
            if not user.is_active:
                raise forms.ValidationError('El usuario no está activo.')    
        # datos del formulario después de que se han pasado todas las validaciones y limpieza definidas en el formulario
        return cleaned_data


#formulario Producto

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'descripcion', 'precio', 'categoria']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre del Producto'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Descripción del Producto', 'rows': 4}),
            'precio': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Precio', 'step': '0.01'}),
            'categoria': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        
        #otra manera
        # def __init__(self,*args, **kwargs):
        #  super().__init__(*args, **kwargs)   
        #  for field in iter(self.fields):
        #      self.fields[field].widget.attrs.update({
        #          'class': 'form-control'
        #          })


#formulario categoria

class CategoriaForm(forms.ModelForm):
    class Meta:
        model= Categoria

        fields = ['nombre', 'observacion']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de  Categoria'}),
            'observacion': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Observacion Categoria', 'rows': 4}),
        }

        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

