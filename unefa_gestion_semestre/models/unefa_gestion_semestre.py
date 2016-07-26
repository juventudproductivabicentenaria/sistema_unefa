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
from openerp import SUPERUSER_ID

class unefa_gestion_semestre(osv.osv):
    _name='unefa.gestion_semestre'
    _rec_name='id'
    
    
    _columns={ 
        'asignatura_id':fields.many2one('unefa.asignatura', 'Asignatura',required=True,states={'borrador': [('readonly', True)]}),
        'seccion_id':fields.many2one('unefa.oferta_academica_seccion', 'Sección',required=True,states={'borrador': [('readonly', True)]}),
        'profesor_id':fields.many2one('res.users', 'Pofesor',required=True,states={'borrador': [('readonly', True)]}),
        'periodo_id': fields.many2one('unefa.conf.periodo_academico','Período Académico',required=True,states={'borrador': [('readonly', True)]}),
        'pensum_id':fields.many2one('unefa.pensum', 'Pensum', required=True,states={'borrador': [('readonly', True)]}),
        'carrera_id': fields.many2one('unefa.carrera', 'Carrera',required=True,readonly=True,states={'borrador': [('readonly', True)]}),
        'turno':fields.selection([('nocturno','NOCTURNO'),('diurno','DIURNO')],'Turno', readonly=True,states={'borrador': [('readonly', True)]}),
        'plan_evaluacion_ids':fields.one2many('unefa.planes_evaluaciones','gestion_semestre_id','Plan de Evaluación',states={'terminado': [('readonly', True)]}),
        'actas_ids':fields.one2many('unefa.acta_notas_pensum','gestion_semestre_id','Plan de Evaluación',states={'terminado': [('readonly', True)]}),
        'actas_recuperacion_ids':fields.one2many('unefa.actas_recuperacion_pensum','gestion_semestre_id','Plan de Evaluación',states={'terminado': [('readonly', True)]}),
        'active':fields.boolean('Activo',states={'borrador': [('readonly', True)]}),
        'acta_aprobada':fields.boolean('Acta Aprobada'),
        'acta_recuperacion':fields.boolean('Acta Recuperación Aprobada'),
        'state': fields.selection([
            ('borrador', 'En Proceso'),
            ('culminado', 'Culminado'),
            ],'Estado', readonly=True, copy=False, help="Este es es estado actual de la gestión semestral.", select=True),
        }
    
    _defaults = {
        'active':True,
        }
    
    _order = 'create_date desc, id desc'
    
    _sql_constraints = [('asignatura_id_unique', 'unique(asignatura_id,seccion_id)', 'Ya existe un registro para esta sección y asignatura .')]

            
    def culminar_gestion_semestre(self,cr,uid,ids,context=None):
        return self.write(cr,uid,ids,{'state':'culminado'})
        
        
    def generar_lista_asignatura(self,cr,uid,ids,context=None):
        url='/descargar/listas_estudiantes/%d' %ids[0]
        return {
            'type': 'ir.actions.act_url',
            'url':url,
            'target': 'new',
            }    
            
    def generar_contrato_aprendizaje(self,cr,uid,ids,context=None):
        url='/descargar/contrato_aprendizaje/%d' %ids[0]
        return {
            'type': 'ir.actions.act_url',
            'url':url,
            'target': 'new',
            }    
            
    def generar_plan_evaluacion(self,cr,uid,ids,context=None):
        url='/descargar/plan_evaluacion/%d' %ids[0]
        return {
            'type': 'ir.actions.act_url',
            'url':url,
            'target': 'new',
            }    
            
    def descargar_acta_notas_recuperacion(self,cr,uid,ids,context=None):
        url='/descargar/acta_notas_recuperacion/%d' %ids[0]
        return {
            'type': 'ir.actions.act_url',
            'url':url,
            'target': 'new',
            }    
            
    def aprobar_acta_notas(self,cr,uid,ids,context=None):
        actas_recuperacion_obj=self.pool.get('unefa.actas_recuperacion_pensum')
        actas_obj=self.pool.get('unefa.acta_notas_pensum')
        list_estudiante=[]
        for registro in self.browse(cr,uid,ids):
            for acta in registro.actas_ids:
                actas_obj.write(cr,uid,acta.id,{'state':'aprobado'})
                if registro.asignatura_id.reparacion==False:
                    for notas in acta.notas_ids:
                        if int(notas.definitiva)<10:
                           list_estudiante.append([0,False,{'estudiante_id':notas.estudiante_id.id,}])
                    if len(list_estudiante)>0:
                        vals={
                            'pensum_id':acta.pensum_id.id,
                            'notas_ids':list_estudiante,
                            'gestion_semestre_id':acta.gestion_semestre_id.id,
                            }
                    list_estudiante=[]
                    actas_recuperacion_obj.create(cr,uid,vals,0)
        return self.write(cr,uid,ids,{'acta_aprobada':True})
        
    def aprobar_acta_notas_recuperacion(self,cr,uid,ids,context=None):
        actas_recuperacion_obj=self.pool.get('unefa.actas_recuperacion_pensum')
        actas_recuperacion_obj=self.pool.get('unefa.actas_recuperacion_notas')
        for registro in self.browse(cr,uid,ids):
            for acta in registro.actas_ids:
                actas_recuperacion_obj.write(cr,uid,acta.id,{'state':'aprobado'})
                for notas in acta.notas_ids:
                    actas_recuperacion_obj.write(cr,uid,notas.id,{'state':'aprobado'})
        return self.write(cr,uid,ids,{'acta_recuperacion':True})
    
    def create(self,cr,uid,vals,context=None):
        vals.update({
            'state':'borrador',
            })
        return super(unefa_gestion_semestre,self).create(cr,uid,vals,context=context)

class unefa_plan_evaluacion(osv.osv):
    _name='unefa.planes_evaluaciones'
    _rec_name=''
    
    def get_select_porcentaje(desde,hasta,rango):
        porc=[]
        
        for i in range(desde,hasta,rango):
            porc.append((str(i),str(i)+'%'))
        return porc
    
    _columns={ 
        'gestion_semestre_id':fields.many2one('unefa.gestion_semestre', 'Gestión',),
        'cohorte': fields.selection([
            ('1', '1'),
            ('2', '2'),
            ('3', '3'),
            ('4', '4'),
            ],'Cohorte', readonly=False, required=True, help="Cohorte al cual se realizara la evaluación.", select=True),
        'fecha_evaluacion': fields.date('Fecha',required=True,),
        'semana_evaluacion': fields.integer('Semana',required=True,),
        'actividad_evaluativa': fields.char('Actividad Evaluativa',required=True,),
        'contenido_ids':fields.many2many('unefa.contenido_unidad','plan_evaluacion_contenidos_rel','plan_id','contenido_id','Contenidos',required=True,),
        'ponderacion': fields.selection(get_select_porcentaje(1,26,1),
            'Ponderación', readonly=False, required=True, help="Ponderación de la evaluación", select=True),
         'observaciones': fields.text('Observaciones',required=False,),
        }
    
    def create(self,cr,uid,vals,context=None):
        vals.update({
            'actividad_evaluativa':vals['actividad_evaluativa'].upper(),
            })
        return super(unefa_plan_evaluacion,self).create(cr,uid,vals,context=context)
    
    def write(self, cr, uid, ids, vals, context=None):
        if 'actividad_evaluativa' in vals.keys():
            vals.update({
            'actividad_evaluativa':vals['actividad_evaluativa'].upper(),
            })
        return super(unefa_plan_evaluacion, self).write(cr, uid, ids, vals, context=context)
        
        
        
class unefa_acta_notas_pensum(osv.osv):
    _name='unefa.acta_notas_pensum'
    _rec_name=''
    
   
    _columns={ 
        'gestion_semestre_id':fields.many2one('unefa.gestion_semestre', 'Gestión',),
        'pensum_id':fields.many2one('unefa.pensum', 'Pensum',readonly=False,required=True,states={'borrador': [('readonly', True)]}),
        'notas_ids':fields.one2many('unefa.acta_notas_asignaturas','pensum_acta_id','Notas'),
        'creado':fields.boolean('Acta Creada'), 
        'state': fields.selection([
            ('borrador', 'Borrador'),
            ('aprobado', 'Aprobado'),
            ],'Estado', readonly=True, copy=False, help="Este es es estado actual de la carga de notas.", select=True),
        }
    
    def domain_pensum_inscritos(self,cr,uid,ids,asignatura_id,seccion_id,context=None):
        list_pensum_ids=[]
        asignaturas_inscritas_obj=self.pool.get('unefa.asignatura_inscritas')
        asignaturas_inscritas_ids=asignaturas_inscritas_obj.search(cr,uid,[('asignatura_id','=',int(asignatura_id)),('seccion_id','=',int(seccion_id))])
        asignaturas_inscritas_especial_ids=asignaturas_inscritas_obj.search(cr,uid,[('asignatura_relacion_id','=',int(asignatura_id)),('seccion_id','=',int(seccion_id))])
        asignaturas_inscritas_total_ids=list(set(asignaturas_inscritas_ids) | set(asignaturas_inscritas_especial_ids))
        asignaturas_inscritas_data=asignaturas_inscritas_obj.browse(cr,uid,asignaturas_inscritas_total_ids)
        for asignatura in asignaturas_inscritas_data:
            list_pensum_ids.append(asignatura.inscripcion_id.user_id.pensum_id.id)
        list_pensum_ids=set(list_pensum_ids)
        dominio={'pensum_id': [('id', '=', list(list_pensum_ids))]}
        return {'domain':dominio}
    
    def crear_acta_notas(self,cr,uid,ids,context=None):
        url='/actas/crear/%d' %ids[0]
        return {
            'type': 'ir.actions.act_url',
            'url':url,
            'target': 'new',
            }    
        
    def editar_acta_notas(self,cr,uid,ids,context=None):
        url='/actas/editar/%d' %ids[0]
        return {
            'type': 'ir.actions.act_url',
            'url':url,
            'target': 'new',
            }
        
    def consultar_acta_notas(self,cr,uid,ids,context=None):
        url='/actas/consultar/%d' %ids[0]
        return {
            'type': 'ir.actions.act_url',
            'url':url,
            'target': 'new',
            }
        
    def descargar_acta_notas(self,cr,uid,ids,context=None):
        url='/actas/descargar/%d' %ids[0]
        return {
            'type': 'ir.actions.act_url',
            'url':url,
            'target': 'new',
            }
    
    def create(self,cr,uid,vals,context=None):
        vals.update({
            'state':'borrador',
            })
        return super(unefa_acta_notas_pensum,self).create(cr,uid,vals,context=context)
    
   
class unefa_acta_notas_asignaturas(osv.osv):
    _name='unefa.acta_notas_asignaturas'
    _rec_name=''
    
   
    _columns={ 
        'pensum_acta_id':fields.many2one('unefa.acta_notas_pensum', 'Actas',),
        'estudiante_id':fields.many2one('unefa.usuario_estudiante', 'Estudiante',),
        'primer_cohorte':fields.char('Primer Cohorte'),
        'segundo_cohorte':fields.char('Segundo Cohorte'),
        'tercer_cohorte':fields.char('Tercer Cohorte'),
        'cuarto_cohorte':fields.char('Cuarto Cohorte'),
        'primer_cohorte_parcial':fields.char('Primer Cohorte Parcial'),
        'segundo_cohorte_parcial':fields.char('Segundo Cohorte Parcial'),
        'tercer_cohorte_parcial':fields.char('Tercer Cohorte Parcila'),
        'cuarto_cohorte_parcial':fields.char('Cuarto Cohorte Parcial'),
        'definitiva':fields.char('Nota Definitiva'),
        'definitiva_letras':fields.char('Nota Definitiva Letras'),
        }
        
class unefa_acta_recuperacion_pensum(osv.osv):
    _name='unefa.actas_recuperacion_pensum'
    _rec_name=''
    
   
    _columns={ 
        'gestion_semestre_id':fields.many2one('unefa.gestion_semestre', 'Gestión',),
        'pensum_id':fields.many2one('unefa.pensum', 'Pensum',readonly=True,required=True,),
        'notas_ids':fields.one2many('unefa.actas_recuperacion_notas','gestion_acta_recu_id','Notas'),
        'state': fields.selection([
            ('borrador', 'Borrador'),
            ('aprobado', 'aprobado'),
            ],'Estado', readonly=True, copy=False, help="Este es es estado actual de la carga de notas de reparación.", select=True),
        }
    
    _sql_constraints = [
        ('pensum_uniq', 'unique(pensum_id)', 'Verifique porfavor. Esta intentando generar actas de notas dos veces para un mismo pensum.')
        ]
        
    def create(self,cr,uid,vals,context=None):
        vals.update({
            'state':'borrador',
            })
        return super(unefa_acta_recuperacion_pensum,self).create(cr,uid,vals,context=context)
    
class unefa_acta_recuperacion_notas(osv.osv):
    _name='unefa.actas_recuperacion_notas'
    _rec_name=''
    
   
    _columns={ 
        'gestion_acta_recu_id':fields.many2one('unefa.actas_recuperacion_pensum', 'Gestión',),
        'estudiante_id':fields.many2one('unefa.usuario_estudiante', 'Estudiante', readonly=True),
        'calificacion': fields.selection([
                        ('NP', 'NP'),
                        ('0', '0'),('1', '1'),('2', '2'),('3', '3'),
                        ('4', '4'),('5', '5'),('6', '6'),('7', '7'),
                        ('8', '8'),('9', '9'),('10', '10'),('11', '12'),
                        ('13', '13'),('14', '14'),('15', '15'),('16', '16'),
                        ('17', '17'),('18', '18'),('19', '19'),('20', '20'),
                        ],'Nota', states={'aprobado': [('readonly', True)]}, copy=False, help="Este es la calificación de un estudiante en reparación.", select=True),
        'definitiva_letras':fields.char('Nota Letras', readonly=True),
        'state': fields.selection([
            ('borrador', 'Borrador'),
            ('aprobado', 'aprobado'),
            ],'Estado', readonly=True, copy=False, help="Este es es estado actual de la carga de notas de reparación.", select=True),
        }
    
    def convertir_numero_letras(self,cr,uid,ids,calificacion,context=None):
        dic_numero_letra={
            'NP':'NO PRESENTO','0':'CERO','1':'UNO','2':'DOS','3':'TRES','4':'CUATRO',
            '5':'CINCO','6':'SEIS','7':'SIETE','8':'OCHO','9':'NUEVE',
            '10':'DIEZ','11':'ONCE','12':'DOCE','13':'TRECE','14':'CATORCE',
            '15':'QUINCE','16':'DIESISEIS','17':'DIESISIETE','18':'DISESIOCHO','19':'DIESINUEVE',
            '20':'VEINTE'
            }
        value={
            'definitiva_letras':dic_numero_letra[calificacion]
            }
        return {'value':value}
        
    
    def create(self,cr,uid,vals,externo=None,context=None):
        if externo==0:
            vals.update({
                'definitiva_letras':self.convertir_numero_letras(cr,uid,[],vals['calificacion'])['value']['definitiva_letras'],
                'state':'borrador',
                })
        else:
            vals.update({
                'state':'borrador',
                })
        return super(unefa_acta_recuperacion_notas,self).create(cr,uid,vals,context=context)
        
    def write(self,cr,uid,ids,vals,context=None):
        if 'calificacion' in vals.keys():
            vals.update({
                'definitiva_letras':self.convertir_numero_letras(cr,uid,ids,vals['calificacion'])['value']['definitiva_letras'],
                })
        return super(unefa_acta_recuperacion_notas,self).write(cr,uid,ids,vals,context=context)
    
    
    
