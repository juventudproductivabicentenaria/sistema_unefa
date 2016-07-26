# -*- coding: utf-8 -*-
##############################################################################
#
#    Programa realizado por, Jeison Pernía y Jonathan Reyes en el marco
#    del plan de estudios de la UNEFA, como TRABAJO ESPECIAL DE GRADO,
#    con el fin de optar al título de Ingeniero de Sistemas.
#    
#    Visitanos en http://juventudproductivabicentenaria.blogspot.com
#
##############################################################################

import inspect, os
from openerp.osv import fields, osv

class unefa_universidad(osv.osv):
    
    _name='res.company'
    _inherit=['res.company']
    
    
    def _default_venezuela(self,cr,uid,ids,context=None):
        res={}
        country_obj=self.pool.get('res.country')
        country_id=country_obj.search(cr,uid,[('name','=','Venezuela')],context=context)
        return country_id[0]
    
    def _get_logo(self, cr, uid, ids):
        ruta_actual=os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
        ruta_actual=ruta_actual.split('models')
        ruta_actual=''.join(ruta_actual)
        return open(os.path.join( 
                                    ruta_actual,
                                    'static',
                                    'img',
                                    'res_company_logo.png'
                                ),'rb') .read().encode('base64')
        
    _columns={
        'rif':fields.char('Rif',
                        size=15,
                        required=True,
                        help='Aquí se coloca el Rif del la universidad'),
        'nucleo_ids':fields.one2many('unefa.nucleo',
                        'universidad_id',
                        'Nucleo'),
        'estado_id':fields.many2one('unefa.estados',
                        'Estado',
                        required=False),
        'municipio_id':fields.many2one('unefa.municipios',
                        'Municipio', 
                        required=False),
        'parroquia_id':fields.many2one('unefa.parroquias',
                        'Parroquia', 
                        required=False),
        'sector':fields.char('Sector', 
                        #~ required=True, 
                        size=30),
        'calle_avenida':fields.char('Calle/Avenida', 
                        #~ required=True, 
                        size=30),
        'casa_apto':fields.char('Casa/Apto', 
                        #~ required=True, 
                        size=30),
        }
    
    _defaults={
        'logo':_get_logo,    
        'country_id':_default_venezuela 
        }
        
    _sql_constraints = [
        ('name_uniq', 'unique(name)', 'La Universidad que ingresó ya ha sido registrada.')
        ]
    
    def cp_limpiar_campos(self,cr,uid,ids,campo,context=None):
        return {'value':{campo:''}}
    
    _order = 'create_date desc, id desc'
    
    def create(self, cr, uid, vals, context=None):
        vals.update({
            'name':vals['name'].upper(),
            })
        return super(unefa_universidad, self).create(cr, uid, vals, context=context)
        
    def write(self, cr, uid, ids, vals, context=None):
        if 'name' in vals.keys():
            vals.update({'name':vals['name'].upper(),})
        return super(unefa_universidad, self).write(cr, uid, ids, vals, context=context)

