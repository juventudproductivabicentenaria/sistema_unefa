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
from openerp.osv import fields, osv
from openerp.tools.translate import _

class unefa_asignatura(osv.osv):
    _name='unefa.asignatura'
    _rec_name='asignatura'
    
    def calculo_total_horas_materias(self, cr, uid, ids,arg,fieldname, context=None):
        res={}
        print ids
        for i in self.browse(cr,uid,ids):
            total=i.hora_teorica+i.hora_practica+i.hora_laboratorio
        res[i.id]=total
        return res
    
    _columns={ 
        'asignatura':fields.char('Asignatura',size=40,required=True,states={'activo': [('readonly', True)]},help='Nombre de la asignatura'),
        'codigo_asignatura':fields.char('Código',size=15,required=True,states={'activo': [('readonly', True)]},help='Código de la asignatura'),
        'unidad_credito':fields.integer('Unidades de Crédito',size=2,required=True,states={'activo': [('readonly', True)]},help='Unidades de crédto que posee la asignatura'),
        'hora_teorica':fields.integer('Horas teóricas',size=2,required=True,states={'activo': [('readonly', True)]},help='Horas de teoría que posee la asignatura'),
        'hora_practica':fields.integer('Horas prácticas',size=2,required=True,states={'activo': [('readonly', True)]},help='Horas prácticas que posee la asignatura'),
        'hora_laboratorio':fields.integer('Horas de laboratorio',size=2,required=True,states={'activo': [('readonly', True)]},help='Horas de laboratorio que posee la asignatura'),
        'active':fields.boolean('Activo',help = """Si está activo el motor lo incluira en la vista."""),
        'asignaturas_ids': fields.many2many('unefa.asignatura', 'unefa_asignatura_prelacion', 'asignatura_id', 'prelacion_id', 'Prelaciones', states={'activo': [('readonly', True)]}),
        'carrera_ids': fields.many2many('unefa.carrera', 'unefa_asignatura_carrera_rel', 'asignatura_id', 'carrera_id', 'Carrera'),
        'state':fields.selection([('inactivo','Inactivo'),('activo','Activo')],'Estatus', help='Estatus de la Asignatura'),
        'oferta_asig_id':fields.many2one('unefa.oferta_academica_semestre', 'Asignatura',),
        'semestres_ids': fields.many2many('unefa.semestre', 'unefa_asignatura_semestre_rel', 'asignatura_id', 'semestre_id', 'Semestres'),
        'total_horas':fields.function(calculo_total_horas_materias, 'Total Horas',type="integer",),
        'reparacion':fields.boolean('No se recupera.')
        }
    
    _defaults = {
        'active':True,
        }
    
    _order = 'create_date desc, id desc'
    
    _sql_constraints = [
        ('codigo_uniq', 'unique(asignatura,codigo_asignatura)', 'El código que ingresó ya ha sido registrado.'),
        ]
        
    def activar_asignatura(self,cr,uid,ids,context=None):
        return self.write(cr,uid,ids,{'state':'activo'})
        
    def desactivar_asignatura(self,cr,uid,ids,context=None):
        return self.write(cr,uid,ids,{'state':'inactivo'})
    
    def create(self, cr, uid, vals, context=None):
        vals.update({
            'asignatura':vals['asignatura'].upper(),
            'codigo_asignatura':vals['codigo_asignatura'].upper(),
            'state':'inactivo',
            })
        if vals['hora_teorica'] == 0:
            raise osv.except_osv(_('Error'), _("La materia no puede contener cero (0) Horas Prácticas."))
        return super(unefa_asignatura, self).create(cr, uid, vals, context=context)
    
    def write(self, cr, uid, ids, vals, context=None):
        if 'asignatura' in vals.keys():
            vals.update({
            'asignatura':vals['asignatura'].upper()
            })
        if 'codigo_asignatura' in vals.keys():
            vals.update({
            'codigo_asignatura':vals['codigo_asignatura'].upper()
            })
        if 'hora_teorica' in vals.keys():
            if vals['hora_teorica'] == 0:
                raise osv.except_osv(_('Error'), _("La Asignatura no puede contener cero (0) Horas Prácticas."))
        return super(unefa_asignatura, self).write(cr, uid, ids, vals, context=context)

class carrera_inherit(osv.osv):
    
    _inherit='unefa.carrera'
    
    _columns={ 
       'asignaturas_ids': fields.many2many('unefa.asignatura', 'unefa_asignatura_carrera_rel', 'carrera_id', 'asignatura_id', 'Carrera'),
        }
