from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login,logout
from django.views.generic import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from .models import *
from .forms import LoginForm,ProductoForm,CategoriaForm
from datetime import datetime




#Home page
@login_required
def home(request):

   
    productos=Producto.objects.all()
    usuario = request.user.username.capitalize()  
    categorias=Categoria.objects.all()
    fecha_hora_actual = datetime.now() 

    context = {
        'categorias': categorias,
        'productos': productos,
        'usuario': usuario,
        'fecha_hora': fecha_hora_actual,  # Agrega la fecha y hora al contexto
    }
    
    return render(request, 'home.html', context)

#vista de link a mi linkedin
def redirect_to_linkedin(request):
    return redirect('https://www.linkedin.com/in/george-abou-chanab-a998a9216/')


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
    template_name = "productos/productos.html"
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
    template_name = "productos/productos.html"

    def form_valid(self, form):
        messages.success(self.request, 'Producto agregado exitosamente.')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('productos')


#PUT Producto

class ProductoUpdateView(LoginRequiredMixin,UpdateView):
    model = Producto
    template_name = "productos/detalle_producto.html"
    form_class=ProductoForm
    context_object_name='producto'

    def form_valid(self, form):
        messages.success(self.request, 'Producto actualizado exitosamente.')
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('productos')
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ProductoForm(instance=self.object)  


class ProductoDetailView(LoginRequiredMixin,DetailView):
    model = Producto
    template_name = "productos/detalle_producto.html"
    context_object_name='producto'
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['editar_producto'] = reverse_lazy('editar_producto', kwargs={'pk': self.object.pk})
        context['eliminar_producto'] = reverse_lazy('eliminar_producto', kwargs={'pk': self.object.pk})
        context['categorias'] = Categoria.objects.all() 
        return context

#DELETE PRODUCTOS

class ProductoDeleteView(LoginRequiredMixin, DeleteView):
    model = Producto
    template_name = "productos/productos.html"  
    
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        messages.success(request, 'Producto eliminado exitosamente.')
        return redirect('productos')  # Redirige a la lista de productos

    def get_success_url(self):
        return reverse_lazy('productos')  
#detailview

    
#############################categoria#################

#GET
class CategoriaListView(LoginRequiredMixin,ListView):
    model = Categoria
    template_name = "categorias/categorias.html"
    context_object_name='categorias'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CategoriaForm()  # Añadimos el formulario al contexto
        return context

class CategoriaDetailView(LoginRequiredMixin,DetailView):
    model = Producto
    template_name = "categorias/detalle_categoria.html"
    context_object_name='categorias'
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['editar_producto'] = reverse_lazy('editar_producto', kwargs={'pk': self.object.pk})
        context['eliminar_producto'] = reverse_lazy('eliminar_producto', kwargs={'pk': self.object.pk})
        return context

#POST
class CategoriaCreateView(CreateView):
    model = Categoria
    form_class=CategoriaForm
    template_name = "categorias/categorias.html"
 

    def form_valid(self, form):
        messages.success(self.request, 'Categoria  agregada exitosamente.')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('categorias')

#PUT    

class CategoriaUpdateView(LoginRequiredMixin,UpdateView):
    model = Categoria
    template_name = "categorias/detalle_categoria.html"
    form_class=CategoriaForm
    context_object_name='categorias'

    def form_valid(self, form):
        messages.success(self.request, 'Categoria actualizada exitosamente.')
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('categorias')

#DELETE Categoria

class CategoriaDeleteView(LoginRequiredMixin,DeleteView):
    model = Categoria
    template_name = "categorias/detalle_categoria.html"

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Categoria eliminada exitosamente.')
        return super().delete(request, *args, **kwargs)

    def get_success_url(self) :
        return reverse_lazy('categorias')