from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login,logout
from django.views.generic import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from .models import *
from .forms import LoginForm,ProductoForm,CategoriaForm




#Home page
@login_required
def home(request):
    return render(request,'base.html')


def login_view(request):
    if request.method=='POST':

        form=LoginForm(request.POST)
        if form.is_valid():
            #DATOS LIMPIOS DEL FORMULARIO
            #datos de los parametros en LoginForm
            username = form.cleaned_data['usuario']
            password = form.cleaned_data['contraseña']
            # Autenticación del usuario
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request,user)
                messages.success(request, 'Inicio de sesión exitoso.') 
                return redirect(home)#nombre de url
            else:
                 messages.error(request, 'Nombre de usuario o contraseña incorrectos.')

    else:
        form=LoginForm()
    return render(request,'login.html',{'form':form})
    

#logout vista
def logoutView(request):
    logout(request)
    return redirect('login')

############### Productos#################################
#GET
class ProductoListView(LoginRequiredMixin,ListView):
    model = Producto
    template_name = "productos.html"
    context_object_name='productos'

    #contexto para el formulario,si no ,no cargar el formulario 
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ProductoForm()  # Añadimos el formulario al contexto
        return context

#POST Productos
class ProductoCreateView(LoginRequiredMixin, CreateView):#LoginRequiredMixin simula el log_required pero se usa este porque es una lista basada en clases
    model = Producto
    form_class = ProductoForm
    template_name = "productos.html"

    def form_valid(self, form):
        messages.success(self.request, 'Producto agregado exitosamente.')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('productos')


#PUT Producto

class ProductoUpdateView(LoginRequiredMixin,UpdateView):
    model = Producto
    template_name = "update-producto.html"
    form_class=ProductoForm
    context_object_name='productos'

    def form_valid(self, form):
        messages.success(self.request, 'Producto actualizado exitosamente.')
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('productos')


class ProductoDetailView(LoginRequiredMixin,DetailView):
    model = Producto
    template_name = "producto-detalle.html"


#DELETE PRODUCTOS

class ProductoDeleteView(LoginRequiredMixin,DeleteView):
    model = Producto
    template_name = "confirm_delete.html"

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Producto eliminado exitosamente.')
        return super().delete(request, *args, **kwargs)

    def get_success_url(self) :
        return reverse_lazy('productos')
    
#detailview
class ProductoDetailView(LoginRequiredMixin,DetailView):
    model = Producto
    template_name = "detalle_producto.html"
    context_object_name='producto'
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['editar_producto'] = reverse_lazy('editar_producto', kwargs={'pk': self.object.pk})
        context['eliminar_producto'] = reverse_lazy('eliminar_producto', kwargs={'pk': self.object.pk})
        return context
    
#############################categoria#################

#GET
class CategoriaListView(LoginRequiredMixin,ListView):
    model = Categoria
    template_name = "categorias.html"
    context_object_name='categorias'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CategoriaForm()  # Añadimos el formulario al contexto
        return context


#POST
class CategoriaCreateView(CreateView):
    model = Categoria
    form_class=CategoriaForm
    template_name = "categorias.html"

    def form_valid(self, form):
        messages.success(self.request, 'Categoria  agregada exitosamente.')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('categorias')

#PUT    