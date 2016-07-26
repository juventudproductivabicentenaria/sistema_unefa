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
    
    
def filtrar_carreras_regimen_general(self,cr,uid,ids,context=None):
    value={}
    objeto_users=self.pool.get('res.users')
    id_users=objeto_users.search(cr,uid,[('id','=',int(uid))])
    data_users=objeto_users.browse(cr,uid,id_users)
    for name in data_users:
        if name.is_estudiante == True:
            obj_users_estudiante=self.pool.get('unefa.usuario_estudiante')
            id_users_estudiante=obj_users_estudiante.search(cr,uid,[('user_id','=',uid)])
            data_users_estudiante=obj_users_estudiante.browse(cr,uid,id_users_estudiante)
            estudiante = data_users_estudiante['id']
            value={
                'carrera_id':data_users['carrera_id'],
                'turno':data_users['regimen'],
                'user_id':estudiante,
            }
        else:
            if name.is_coordinador == True or name.is_asistente == True:
                value={
                        'carrera_id':data_users['coordinacion_id']['carrera_id'],
                        'turno':data_users['coordinacion_id']['regimen'],
                }
    return {'value':value}
    
    
    
class unefa_contenido_programatico(osv.osv):
    _name='unefa.contenido_programatico'
    _rec_name='asignatura_id'
    
    _columns={ 
        'pensum_id':fields.many2one('unefa.pensum', 'Pensum',required=True,states={'activo': [('readonly', True)]}),
        'carrera_id':fields.many2one('unefa.carrera', 'Carrera',required=True,states={'activo': [('readonly', True)]}),
        'asignatura_id':fields.many2one('unefa.asignatura', 'Asignatura',required=True,states={'activo': [('readonly', True)]}),
        'semestre_id':fields.many2one('unefa.semestre', 'Semestre',required=True,states={'activo': [('readonly', True)]}),
        'contenido_ids': fields.many2many('ir.attachment', 'unefa_contenido_attachment_rel', 'contenido_id', 'attachment_id', 'Descargar Contenido Programático'),
        'turno':fields.selection([('nocturno','NOCTURNO'),('diurno','DIURNO')],'Turno', required=True,),
        'active':fields.boolean('Activo',help = """Si está activo el motor lo incluira en la vista."""),
        'unidades_ids': fields.one2many(
                                    'unefa.contenido_unidad', 
                                    'unidad_id', 
                                    'Unidad',
                                    required=False),
        'state':fields.selection([('inactivo','Inactivo'),
                                ('activo','Activo')],'Estatus',
                                help='Estatus del Pensum'),
        }
    
    _defaults = {
        'active':True,
        }
    
    _sql_constraints = [
        ('unique_asig_uniq', 'unique(asignatura_id,pensum_id,carrera_id,turno)', 'La asignatura que ingresó ya ha sido registrada para la carrera seleccionada.'),
        ]
    
    def activar_contenido_programatico(self,cr,uid,ids,context=None):
        return self.write(cr,uid,ids,{'state':'activo'})
        
    def desactivar_contenido_programatico(self,cr,uid,ids,context=None):
        return self.write(cr,uid,ids,{'state':'inactivo'})
    
    def filtrar_carreras_regimen(self,cr,uid,ids,context=None):
        return filtrar_carreras_regimen_general(self,cr,uid,ids)
    
    def create(self,cr,uid,vals,context=None):
        filtro_carrera=filtrar_carreras_regimen_general(self,cr,uid,[])
        vals.update({
            'carrera_id':filtro_carrera['value']['carrera_id'].id,
            'turno':filtro_carrera['value']['turno'],
            'state':'inactivo',
            })
        return super(unefa_contenido_programatico,self).create(cr,uid,vals,context=context)
    
class unefa_contenido_unidad(osv.osv):
    _name='unefa.contenido_unidad'
    _rec_name='unidad'
    
    _columns={ 
        'unidad_id':fields.many2one('unefa.contenido_programatico', 'Unidad',ondelete='cascade',),
        'asignatura_id':fields.many2one('unefa.asignatura', 'Asignatura',required=True,),
        'unidad':fields.char('Unidad',size=40,required=True,help='Nombre de la unidad'),
        'descipcion': fields.text('Descripción',required=True,),
        'objetivos_ids': fields.one2many(
                                    'unefa.contenido_objetivo', 
                                    'objetivo_id', 
                                    'Objetivos',
                                    required=True),
        
        }
    
    def create(self, cr, uid, vals, context=None):
        vals.update({
            'unidad':vals['unidad'].upper(),
            })
        return super(unefa_contenido_unidad, self).create(cr, uid, vals, context=context)
    
    def write(self, cr, uid, ids, vals, context=None):
        if 'unidad' in vals.keys():
            vals.update({
            'unidad':vals['unidad'].upper(),
            })
        return super(unefa_contenido_unidad, self).write(cr, uid, ids, vals, context=context)
class unefa_contenido_objetivo(osv.osv):
    _name='unefa.contenido_objetivo'
    _rec_name='objetivo'
    
    _columns={ 
        'objetivo_id':fields.many2one('unefa.contenido_unidad', 'Objetivo',ondelete='cascade',),
        'objetivo':fields.char('Objetivo',size=40,required=True,help='Nombre del objetivo'),
        'descipcion': fields.text('Descripción',required=True,),
               
        }
    
    
