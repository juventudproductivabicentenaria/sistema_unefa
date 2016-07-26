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

class pisos(osv.osv):
    _name='unefa.pisos'
    _rec_name='numero'
    
    _columns={
        'numero':fields.char('Numero de Piso',
                            size=80,
                            states={'activo': [('readonly', True)]},
                            required=True,
                            help='Aquí se coloca el nombre del nucleo'),
        'cant_banios':fields.integer('Cantidad de Baños',
                            states={'activo': [('readonly', True)]},),
        'cant_filtros':fields.integer('Cantidad de Filtros',
                            states={'activo': [('readonly', True)]},),
        'aulas_id':fields.one2many('unefa.aulas','piso_id','Aulas',
                            states={'activo': [('readonly', True)]},),
        'coordinaciones_ids': fields.many2many('unefa.coordinacion', 
                            'unefa_piso_coordinacion_rel', 'piso_id',
                            'coordinacion_id', 'Coordinacion (es)',
                            states={'activo': [('readonly', True)]},),
        'active':fields.boolean('Activo',
                            help='Si esta activo el motor lo incluira en la vista...'),
        'state':fields.selection([('inactivo','Inactivo'),
                            ('activo','Activo')],'Estatus', 
                            required=False, help='Estatus del piso'),
    }
    
    _defaults={
        'active':True,
    }
    
    _sql_constraints = [
        ('numero_uniq', 'unique(numero)', 'El Piso que ingresó ya ha sido registrado.')
        ]
    
    def activar_piso(self,cr,uid,ids,context=None):
        return self.write(cr,uid,ids,{'state':'activo'})
        
    def desactivar_piso(self,cr,uid,ids,context=None):
        return self.write(cr,uid,ids,{'state':'inactivo'})
    
    def create(self, cr, uid, vals, context=None):
        vals.update({
            #~ 'state':'inactivo',
            })
        return super(pisos, self).create(cr, uid, vals, context=context)
    
    

class aulas(osv.osv):
    _name='unefa.aulas'
    _rec_name='numero'
    
    _columns={
        'numero':fields.char('Numero de Aula',
                            size=80,
                            required=True,
                            help='Aquí se coloca el nombre del nucleo'),
        'tipo':fields.selection([('normal','Normal'),
                            ('conferencia','Conferencia')],
                            'Tipo de Aula', 
                            required=True, 
                            help='Normal o de Conferencia'),
        'cant_pupitres':fields.integer('Cantidad de Pupitres', 
                            help="Cantidad de Pupitres que posee"),
        'cant_pizarras':fields.integer('Cantidad de Pizarras', 
                            help="Cantidad de Pizarras que posee"),
        'piso_id':fields.many2one('unefa.pisos',
                            'Piso'),
        'active':fields.boolean('Activo',
                            help='Si esta activo el motor lo incluira en la vista...'),
    }
    
    _defaults={
        'active':True,
    }
    
    _sql_constraints = [
        ('numero_uniq', 'unique(numero)', 'El Aula que ingresó ya ha sido registrada.')
        ]
    
