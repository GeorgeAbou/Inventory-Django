from django.urls import path
from .views import *

urlpatterns = [
    path('', login_view, name='login'),  # Página de inicio de sesión como página principal
    path('home/', home, name='home'),  # Página principal después de iniciar sesión
    path('home/logout/', logoutView, name='logout'),
    path('home/productos/', ProductoListView.as_view(), name='productos'),
    path('home/productos/agregar/', ProductoCreateView.as_view(), name='agregar_producto'),
    path('home/productos/<int:pk>/',ProductoDetailView.as_view(), name='detalle_producto'),
    path('home/productos/<int:pk>/editar/', ProductoUpdateView.as_view(), name='editar_producto'),
    path('home/productos/<int:pk>/eliminar/',ProductoDeleteView.as_view(), name='eliminar_producto'),
]
