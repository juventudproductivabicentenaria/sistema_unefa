$(document).ready(function () {
    
    
    $("#enviar_horario" ).click(function() {
        
        var form='#formcrearhorarios';
        var gif=$('#gifbusq_avanz');
        var v=$(form).apiform_panel();
        var formCont=v.context(form);
        var panramentros={'gif':gif,'boton':this}
       
        if (formCont.campovacios=='no'){
         v.ajax.enviar(formCont.destino,formCont.datos,panramentros)
            }
        
    });
    
    $("#enviar_horario_editado" ).click(function() {
        var form='#formeditarhorario';
        var gif=$('#gifbusq_avanz');
        var v=$(form).apiform_panel();
        var formCont=v.context(form);
        var panramentros={'gif':gif,'boton':this}
       
        if (formCont.campovacios=='no'){
         v.ajax.enviar(formCont.destino,formCont.datos,panramentros)
            }
        
    });
                    
    
});




           

            
            
