# -*- coding: utf-8 -*-
##############################################################################
#    
#    Modulo Desarrollado por Juventud Productiva (Victor Davila)
#    Visitanos en http://juventudproductivabicentenaria.blogspot.com/
#    Nuestro Correo juventudproductivabicentenaria@gmail.com
#
##############################################################################

from openerp.osv import fields, osv

class unefa_cantidad_estudiantes(osv.osv):
    _name='unefa.cantidad_estudiantes'
    _description='Cantidad de minima y maxima inscritos en una seccion'
    
    _columns = {
        'cantidad_minima': fields.integer(
                            'Cantidad mínima', 
                            size=2, 
                            required=True, 
                            help='Cantidad mínima de estudiantes para una sección'),
        'cantidad_maxima': fields.integer(
                            'Cantidad máxima', 
                            size=2, 
                            required=True, 
                            help='Cantidad máxima de estudiantes para una sección'),
        'carrera_id':fields.many2one('unefa.carrera','Carrera', required=True,readonly=False,),
        'turno':fields.selection([('nocturno','NOCTURNO'),('diurno','DIURNO'),],'Turno', required=True,readonly=False),
    }
    
    
    _sql_constraints = [
        ('limite_alumnos_uniq', 'unique(carrera_id,turno)', 'Ya existe una registro para esta carrera y este turno.')
        ]
