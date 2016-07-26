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

import time
from openerp.osv import fields, osv

class nucleo(osv.osv):
    _name='unefa.nucleo'
    _rec_name='nombre'
    
    _columns={
        'nombre':fields.char('Sede',size=80,required=True,help='Aquí se coloca el nombre de la sede'),
        'decano':fields.char('Decano',size=80,required=True,help='Aquí se coloca el nombre del decano de la sede'),
        'unidad_academica':fields.char('Jefe Unidad Académica',size=80,required=True,help='Aquí se coloca el nombre del jefe de la unidad académica'),
        'tipo_sede':fields.selection([('nucleo','NÚCLEO'),('extension','EXTENCIÓN'),('ampliacion','AMPLIACIÓN')],'Tipo de sede',required=True,help='Aquí selecciona el tipo de sede.'),
        'redi_id':fields.many2one('unefa.redi', 'REDI',required=True,help='Aquí se coloca la REDI donde está ubicada el sede'),
        'region_id':fields.many2one('unefa.region_defensa_integral', 'Región Defensa Integral',required=True,help='Aquí se coloca la Región de Defensa Integral donde está ubicada el sede'),
        'direccion':fields.text('Dirección',required=True,help='Aquí se coloca el dirección del núcleo'),
        'universidad_id':fields.many2one('res.company', 'Universidad'),
        'carrera_ids':fields.many2many('unefa.carrera','unefa_nucleo_carrera', 'nucleo_id','carrera_id', 'Carreras'),
        'telefono':fields.char('Teléfono',size=64,required=True,help='Aquí se coloca el Telefono del nucleo'),
        'estado_id':fields.many2one('unefa.estados','Estado', required=True),
        'municipio_id':fields.many2one('unefa.municipios','Municipio', required=True),
        'parroquia_id':fields.many2one('unefa.parroquias','Parroquia', required=True),
        'direccion':fields.char('Dirección',size=80,required=True,help='Aquí se coloca la dirección de la sede'),
        'active':fields.boolean('Activo',help='Si esta activo el motor lo incluira en la vista...'),
        }
    
    _defaults={
        'active':True,
    }
    
    _sql_constraints = [
        ('nucleo_uniq', 'unique(nombre)', 'El Nucleo que ingresó ya ha sido registrado.')
        ]
    
    _order = 'create_date desc, id desc'
    
    def cp_limpiar_campos(self,cr,uid,ids,campo,context=None):
        return {'value':{campo:''}}
    
    def create(self, cr, uid, vals, context=None):
        vals.update({
            'nombre':vals['nombre'].upper(),
            'direccion':vals['direccion'].upper(),
            'decano':vals['direccion'].upper(),
            'unidad_academica':vals['direccion'].upper(),
            })
        return super(nucleo, self).create(cr, uid, vals, context=context)
        
    def write(self, cr, uid, ids, vals, context=None):
        if 'nombre' in vals.keys():
            vals.update({'nombre':vals['nombre'].upper(),})
        if 'direccion' in vals.keys():
            vals.update({'direccion':vals['direccion'].upper(),})
        if 'unidad_academica' in vals.keys():
            vals.update({'unidad_academica':vals['unidad_academica'].upper(),})
        if 'decano' in vals.keys():
            vals.update({'decano':vals['decano'].upper(),})
        return super(nucleo, self).write(cr, uid, ids, vals, context=context)
    
    

    
