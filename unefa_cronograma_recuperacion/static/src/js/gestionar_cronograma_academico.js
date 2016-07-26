$(document).ready(function () {
    
    
    $("#enviar_cronograma_academico" ).click(function() {
        var form='#formcrearcronogramaacademico';
        var gif=$('#gifbusq_avanz');
        var v=$(form).apiform_panel();
        var formCont=v.context(form);
        var panramentros={'gif':gif,'boton':this}
       
        if (formCont.campovacios=='no'){
         v.ajax.enviar(formCont.destino,formCont.datos,panramentros)
            }
        
    });
    
    $("#enviar_cronograma_editado" ).click(function() {
        var form='#formeditarcronogramarecuperacion';
        var gif=$('#gifbusq_avanz');
        var v=$(form).apiform_panel();
        var formCont=v.context(form);
        var panramentros={'gif':gif,'boton':this}
       
        if (formCont.campovacios=='no'){
         v.ajax.enviar(formCont.destino,formCont.datos,panramentros)
            }
        
    });
                    
    
});




           

            
            
