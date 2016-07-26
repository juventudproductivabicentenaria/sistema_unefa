# -*- coding: utf-8 -*-
##############################################################################
#
#    Programa realizado por, Jeison Pernía y Jonathan Reyes en el marco
#    del plan de estudios de la Universidad Nacional Experimental
#    Politécnica de la Fuerza Armada, como TRABAJO ESPECIAL DE GRADO,
#    con el fin de optar al título de Ingeniero de Sistemas.
#    
#    Visitanos en http://juventudproductivabicentenaria.blogspot.com
#
##############################################################################
from openerp.osv import fields, osv
from openerp import SUPERUSER_ID

def filtrar_carreras_regimen_general(self,cr,uid,ids,context=None):
    objeto_users=self.pool.get('res.users')
    id_users=objeto_users.search(cr,uid,[('id','=',uid)])
    data_users=objeto_users.browse(cr,uid,id_users)
    value={}
    value={
        'carrera_id':data_users['coordinacion_id'].carrera_id,
        'turno':data_users['coordinacion_id'].regimen,
        }
    return {'value':value}

class unefa_pensum(osv.osv):
    _name='unefa.pensum'
    _rec_name='pensum'
    
    _columns={ 
        'pensum':fields.char('Pensum',size=40,required=True,help='Nombre del pensum',states={'activo': [('readonly', True)]}),
        'carrera_id': fields.many2one('unefa.carrera', 'Carrerra', required=True,help='Carrera relacionada al pensum', states={'activo': [('readonly', True)]}),
        'turno':fields.selection([('nocturno','NOCTURNO'),('diurno','DIURNO')],'Turno', required=True,states={'activo': [('readonly', True)]}),
        'active':fields.boolean('Activo',help = """Si está activo el motor lo incluira en la vista."""),
        'semestre_ids':fields.one2many('unefa.semestre', 'pensum_id', 'Semestre', states={'activo': [('readonly', True)]}, required=True,help='Semestre relacionado al pensum'),
        'pensum_ids': fields.many2many('ir.attachment', 'pensum_attachment_rel', 'pensun_id', 'attachment_id', 'Descargar Pensum'),
        'state':fields.selection([('inactivo','Inactivo'),('activo','Activo')],'Estatus', help='Estatus del Pensum'),

        }
    
    _defaults = {
        'active':True,
        }
    
    _sql_constraints = [
        ('pensum_uniq', 'unique(pensum,carrera_id,turno)', 'El Pensum que ingresó ya ha sido registrado.')
        ]
    
    _order = 'create_date desc, id desc'
    
    def filtrar_carreras_regimen(self,cr,uid,ids,context=None):
        return filtrar_carreras_regimen_general(self,cr,uid,ids)
    
    def activar_pensum(self,cr,uid,ids,context=None):
        return self.write(cr,uid,ids,{'state':'activo'})
        
    def desactivar_pensum(self,cr,uid,ids,context=None):
        return self.write(cr,uid,ids,{'state':'inactivo'})
    
    def validar_asignatura_semestre_create(self,cr,uid,ids,semestres_ids,context=None):
        #~ list_semestre = []
        #~ list_smst = []
        #~ for c in semestres_ids:
            #~ list_smst.append(c[2]['semestre'])
            #~ if c[2]['asignaturas_ids'][0][2] == []:
                #~ raise osv.except_osv(
                #~ ('Atención!'),
                #~ (u'Agregue asignaturas a los semestres, no pueden estar vacíos.'))
            #~ for ids in c[2]['asignaturas_ids'][0][2]:
                #~ list_semestre.append(ids)
        #~ list_smst_filtrado=list(set(list_smst))
        #~ if len(list_smst)!=len(list_smst_filtrado):
            #~ raise osv.except_osv(
                #~ ('Error!'),
                #~ (u'Verificar, existe dos semestres con el mismo número.'))
        #~ list_semestre_filtrado=list(set(list_semestre))
        #~ if len(list_semestre)!=len(list_semestre_filtrado):
            #~ raise osv.except_osv(
                #~ ('Error!'),
                #~ (u'Verificar, existe una o más asignaturas iguales asignadas a más de un semestre.'))
        return True
        
    def validar_asignatura_semestre_write(self,cr,uid,ids,semestres_ids,context=None):
        list_semestre = []
        list_smst = []
        semetre_obj=self.pool.get('unefa.semestre')
        for c in semestres_ids:
            if c[2]!=False:
                
                if 'semestre' in c[2].keys():
                    list_smst.append(c[2]['semestre'])
                if 'asignaturas_ids' in c[2].keys():
                    for ids in c[2]['asignaturas_ids'][0][2]:
                        list_semestre.append(ids)
            else:
                list_smst.append(semetre_obj.browse(cr,uid,c[1])['semestre'])
                for id_asi in semetre_obj.browse(cr,uid,c[1])['asignaturas_ids']:
                    list_semestre.append(id_asi.id)
        list_smst_filtrado=list(set(list_smst))
        if len(list_smst)!=len(list_smst_filtrado):
            raise osv.except_osv(
                ('Error!'),
                (u'Verificar, existe dos semestres con el mismo número.'))
        list_semestre_filtrado=list(set(list_semestre))
        if len(list_semestre)!=len(list_semestre_filtrado):
            raise osv.except_osv(
                ('Error!'),
                (u'Verificar, existe una o más asignaturas iguales asignadas a más de un semestre.'))
        return True
    
    
    def create(self,cr,uid,vals,context=None):
        vals.update({
            'state':'inactivo',
            })
        validar_asignatura = self.validar_asignatura_semestre_create(cr,uid,[],vals['semestre_ids'])
        pensum_id=super(unefa_pensum,self).create(cr,uid,vals,context=context)
        carrera_obj=self.pool.get('unefa.carrera')
        asignatura_obj=self.pool.get('unefa.asignatura')
        list_carreras=[]
        if vals['semestre_ids'] == []:
            raise osv.except_osv(
                ('Error!'),
                (u'Agregue al menos un semestre.'))
        for sem in  vals['semestre_ids']:
            for id_asig in sem[2]['asignaturas_ids'][0][2]:
                for c in asignatura_obj.browse(cr,uid,id_asig)['carrera_ids']:
                    list_carreras.append(c.id)
                if int(vals['carrera_id']) not in list_carreras:
                    list_carreras.append(int(vals['carrera_id']))
                values={
                    'carrera_ids':[[6, False, []]],
                    }
                asignatura_obj.write(cr,uid,int(id_asig),values)
                value={
                    'carrera_ids':[[6, False, list_carreras]],
                    }
                asignatura_obj.write(cr,uid,int(id_asig),value)
                list_carreras=[]
        pensun_list=[]
        for c in carrera_obj.browse(cr,uid,int(vals['carrera_id']))['pensum_ids']:
            pensun_list.append(c.id)
        if pensum_id not in pensun_list:
            pensun_list.append(pensum_id)
        value={
            'pensum_ids':[[6, False, pensun_list]],
            }
        carrera_obj.write(cr,SUPERUSER_ID,int(vals['carrera_id']),value)
        return pensum_id
    
    def write(self, cr, uid, ids, vals, context=None):
        if 'semestre_ids' in vals.keys():
            validar_asignatura = self.validar_asignatura_semestre_write(cr,uid,[],vals['semestre_ids'])
        list_carreras=[]
        list_asignaturas=[]
        asignaturas_viejas=[]
        carrera_obj=self.pool.get('unefa.carrera')
        if 'semestre_ids' in vals.keys():
            arreglo_list=[]
            for arreglo in vals['semestre_ids']:
                if arreglo == [2, 1, False]:
                    arreglo_list.append(arreglo)
                arreglo_asig_list=[]
                if type(arreglo[2])==dict:
                    if 'asignaturas_ids' in arreglo[2]:
                        for asig in arreglo[2]['asignaturas_ids']:
                            if asig == [6, False, []]:
                                arreglo_asig_list.append(arreglo)
                            if len(arreglo[2]['asignaturas_ids'])==len(arreglo_asig_list):
                                raise osv.except_osv(
                                    ('Error!'),
                                    (u'Agregue al menos una asignatura a cada semestre creado.'))
                            arreglo_asig_list=[]
            if len(vals['semestre_ids'])==len(arreglo_list):
                raise osv.except_osv(
                    ('Error!'),
                    (u'Agregue al menos un semestre.'))
            if 'carrera_id' in vals.keys():
                carrera=vals['carrera_id']
            else:
                carrera=self.browse(cr,uid,ids)['carrera_id'].id
            asignatura_obj=self.pool.get('unefa.asignatura')
            semestre_obj=self.pool.get('unefa.semestre')
            list_sem_eli=[]
            list_id_carre=[]
            for sem in vals['semestre_ids']:
                if sem[0]==2:
                    semestre_eli_data=semestre_obj.browse(cr,uid,int(sem[1]))['asignaturas_ids']
                    for sed in semestre_eli_data:
                        list_sem_eli.append(int(sed))
                    for lse in list_sem_eli:
                        for id_c in asignatura_obj.browse(cr,uid,lse)['carrera_ids']:
                            list_id_carre.append(id_c.id)
                        if carrera in list_id_carre:
                            list_id_carre.remove(carrera)
                        values_eli={
                            'carrera_ids':[[6, False, []]],
                            }
                        asignatura_obj.write(cr,uid,int(lse),values_eli)
                        value_eli={
                            'carrera_ids':[[6, False, list_id_carre]],
                            }
                        asignatura_obj.write(cr,uid,int(lse),value_eli) 
                        list_id_carre=[]
                if sem[2]!=False:
                    semestre_data=semestre_obj.browse(cr,uid,int(sem[1]))['asignaturas_ids']
                    for sd in semestre_data:
                        asignaturas_viejas.append(int(sd))
                    for id_asig in sem[2]['asignaturas_ids'][0][2]:
                        if id_asig in asignaturas_viejas:
                            asignaturas_viejas.remove(id_asig)
                        for c in asignatura_obj.browse(cr,uid,id_asig)['carrera_ids']:
                            list_carreras.append(c.id)
                        if carrera not in list_carreras:
                            list_carreras.append(carrera)
                        values={
                            'carrera_ids':[[6, False, []]],
                            }
                        asignatura_obj.write(cr,uid,int(id_asig),values)
                        value={
                            'carrera_ids':[[6, False, list_carreras]],
                            }
                        asignatura_obj.write(cr,uid,int(id_asig),value) 
                        list_carreras=[]
                    if len (asignaturas_viejas)>0:
                        list_carrera=[]
                        for av in asignaturas_viejas:
                            for ca in asignatura_obj.browse(cr,uid,av)['carrera_ids']:
                                list_carrera.append(ca.id)
                            if carrera in list_carrera:
                                list_carrera.remove(carrera)
                            valus={
                            'carrera_ids':[[6, False, []]],
                            }
                            asignatura_obj.write(cr,uid,int(av),valus)
                            val={
                            'carrera_ids':[[6, False, list_carrera]],
                                }
                            asignatura_obj.write(cr,uid,int(av),val)
        if 'carrera_id' in vals.keys():
            pensun_data=self.browse(cr,uid,ids)
            pensun_list=[]
            pensun_list_viejo=[]
            
            for c in carrera_obj.browse(cr,uid,int(vals['carrera_id']))['pensum_ids']:
                pensun_list.append(c.id)
                
                
            for v in carrera_obj.browse(cr,uid,int(pensun_data['carrera_id']))['pensum_ids']:
                pensun_list_viejo.append(v.id)
            if ids[0] not in pensun_list:
                pensun_list.append(ids[0])
            if ids[0]  in pensun_list_viejo:
                pensun_list_viejo.remove(ids[0])
            value1={
                'pensum_ids':[[6, False, []]],
            }
            carrera_obj.write(cr,SUPERUSER_ID,int(pensun_data['carrera_id']),value1)
            value={
            'pensum_ids':[[6, False, pensun_list_viejo]],
            }
            carrera_obj.write(cr,SUPERUSER_ID,int(pensun_data['carrera_id']),value)
            
            values1={
            'pensum_ids':[[6, False, []]],
            }
            carrera_obj.write(cr,SUPERUSER_ID,int(vals['carrera_id']),values1)
            values={
            'pensum_ids':[[6, False, pensun_list]],
            }
            carrera_obj.write(cr,SUPERUSER_ID,int(vals['carrera_id']),values)
        return super(unefa_pensum, self).write(cr, uid, ids, vals, context=context)

    
class unefa_semestre(osv.osv):
    _name='unefa.semestre'
    _rec_name='semestre'
    
    _columns={ 
        'semestre':fields.integer('Semestre',size=2,required=True,help='Número del Semestre'),
        'pensum_id': fields.many2one('unefa.pensum', 'Pensum', ondelete='cascade', help='Pensum'),
        'asignaturas_ids': fields.many2many('unefa.asignatura', 'unefa_asignatura_semestre_rel', 'semestre_id', 'asignatura_id', 'Asignaturas'),
        'active':fields.boolean('Activo',help = """Si está activo el motor lo incluira en la vista."""),
        }
    
    _defaults = {
        'active':True,
        }

    
class carrera_inherit2(osv.osv):
    
    _inherit='unefa.carrera'
    
    _columns={ 
       'pensum_ids':fields.many2many('unefa.pensum','unefa_carrera_pensum_rel', 'carrera_id','pensum_id', 'Pensum'),
        }
