# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#    
#    Modulo Desarrollado por Juventud Productiva (Victor Davila)
#    Visitanos en http://juventudproductivabicentenaria.blogspot.com/
#    Nuestro Correo juventudproductivabicentenaria@gmail.com
#
##############################################################################

from openerp.osv import fields, osv

class unefa_cantidad_unidades_credito(osv.osv):
    _name='unefa.cantidad_unidades_credito'
    _description='Cantidad de  maxima de unidades de credito a cursar por periodo'
    
    _columns = {
        'cantidad_uc': fields.integer(
                            'Cantidad Unidades de Crédito', 
                            size=2, 
                            required=True, 
                            help='Cantidad mínima de estudiantes para una sección'),
        'periodo_id':fields.many2one(
                            'unefa.conf.periodo_academico',
                            'Período académico', 
                            required=False),
        'carrera_id':fields.many2one('unefa.carrera','Carrera', required=True,readonly=False,),
        'turno':fields.selection([('nocturno','NOCTURNO'),('diurno','DIURNO'),],'Turno', required=True,readonly=False),
        
        
    }
    
    
