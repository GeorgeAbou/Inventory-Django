from django.db import models

#modelo de categorias
class Categoria(models.Model):
  
    nombre=models.CharField("Nombre de Catedogia",max_length=150)
    observacion=models.CharField(("Observacion"), max_length=150)
    
    def __str__(self):
        return self.nombre
    
    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'

        

#modelo productos


class Producto(models.Model):
    
    nombre=models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    categoria = models.ForeignKey(Categoria, related_name='productos',on_delete=models.CASCADE)#no se agrega el on cascade para no eliminar categria con todos sus productos
    
    def __str__(self):
        return self.nombre+" "+"Precio: "+str(self.precio)
    
    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'

        
