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
from openerp.http import request

class unefa_redi(osv.osv):
    _name='unefa.redi'
    _description='Registro de REDI'
    
    _columns = {
        'name': fields.char(
                            'REDI', 
                            size=100, 
                            required=True, 
                            help='Nombre  de la REDI'),
        'codigo': fields.char(
                            'Código', 
                            size=10, 
                            required=True, 
                            help='Código  de  Identificación de la REDI'),
        'active': fields.boolean(
                            'Activo',
                            help='Estatus del registro Activado-Desactivado'),
        
    }
    
    _defaults = {
        'active':True, 
        'ip':lambda self,cr,uid,context: request.httprequest.remote_addr
    }
    
    _sql_constraints = [
        ('codigo_uniq', 'unique(codigo)', 'El Código que ingresó ya ha sido registrado.')
        ]
    
    def create(self, cr, uid, vals, context=None):
        vals.update({
            'name':vals['name'].upper(),
            'codigo':vals['codigo'].upper(),
            })
        return super(unefa_redi, self).create(cr, uid, vals, context=context)
        
    def write(self, cr, uid, ids, vals, context=None):
        if 'name' in vals.keys():
            vals.update({'name':vals['name'].upper(),})
        if 'codigo' in vals.keys():
            vals.update({'codigo':vals['codigo'].upper(),})
        return super(unefa_redi, self).write(cr, uid, ids, vals, context=context)
