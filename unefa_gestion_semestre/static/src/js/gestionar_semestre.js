$(document).ready(function () {
        
        
        
        $('.nota').mask("00,00", {reverse: true});
        $('.notaparcial').mask("0,00", {reverse: true});
    
    
        
        
        $('.calculo').on('change', function(event){
            var id=$(this).attr('id')
            var n=id.split('_')[2]
            var idPorcentaje=id+n
            var valor=$(this).val()
            var valor_raplace=valor.replace(',','.')
            
            if ((parseFloat(valor_raplace)>20)  || (parseFloat(valor_raplace)<0 )){
                cuerpo='La nota a registrar debe estar comprendida entre 0 y 20'
                $('.cuerpo').html('<strong class="text-danger">'+cuerpo+'</strong>');
                $('.titulo').html('<strong>Aviso!</strong>')
                $('#AJAX_Modal').modal('show');
                $('#'+id).val(0);
                }
            else{
                var nota = parseFloat(valor_raplace) * 0.25
                console.log(nota)
                console.log(nota)
                console.log(nota)
                console.log(nota)
                console.log(nota)
                console.log(nota)
                var p=idPorcentaje+n;
                $('#'+idPorcentaje).val(nota);
                $('#'+p).text(nota);
                var idp1='primer_cohorte_'+n+n
                var idp2='segundo_cohorte_'+n+n
                var idp3='tercer_cohorte_'+n+n
                var idp4='cuarto_cohorte_'+n+n
                var idnp1='primer_cohorte_'+n
                var idnp2='segundo_cohorte_'+n
                var idnp3='tercer_cohorte_'+n
                var idnp4='cuarto_cohorte_'+n
                var pp1='primer_cohorte_'+n+n+n
                var pp2='segundo_cohorte_'+n+n+n
                var pp3='tercer_cohorte_'+n+n+n
                var pp4='cuarto_cohorte_'+n+n+n
                var p1=$('#'+idp1).val()
                var p1_raplace=p1.replace(',','.')
                var p2=$('#'+idp2).val()
                var p2_raplace=p2.replace(',','.')
                var p3=$('#'+idp3).val()
                var p3_raplace=p3.replace(',','.')
                var p4=$('#'+idp4).val()
                var p4_raplace=p4.replace(',','.')
                if (isNaN(p1_raplace)==true){
                    p1_raplace=0
                    $('#'+idp1).val(0)
                    $('#'+idnp1).val(0)
                    $('#'+pp1).text(0.00);
                    }
                if (isNaN(p2_raplace)==true){
                    
                    p2_raplace=0
                    $('#'+idp2).val(0)
                    $('#'+idnp2).val(0)
                    $('#'+pp2).text(0.00);
                    }
                if (isNaN(p3_raplace)==true){
                    p3_raplace=0
                    $('#'+idp3).val(0)
                    $('#'+idnp3).val(0)
                    $('#'+pp3).text(0.00);
                    }
                if (isNaN(p4_raplace)==true){
                    p4_raplace=0
                    $('#'+idp3).val(0)
                    $('#'+idnp3).val(0)
                    $('#'+pp4).text(0.00);
                    }
                var idDefinitiva='definitiva_'+n
                var pDefinitiva='definitiva_'+n+n
                definitiva=Math.round(parseFloat(p1_raplace)+parseFloat(p2_raplace)+parseFloat(p3_raplace)+parseFloat(p4_raplace))
                $('#'+idDefinitiva).val(definitiva)
                $('#'+pDefinitiva).text(definitiva);
                
                var idDefinitivaLetras='definitiva_letras_'+n
                var idDefinitivaLetrasP='definitiva_letras_'+n+n
                switch(definitiva) {
                  case definitiva=0:
                    $('#'+idDefinitivaLetras).val('Cero')
                    $('#'+idDefinitivaLetrasP).text('Cero');
                    break;
                  case definitiva=1:
                    $('#'+idDefinitivaLetras).val('Uno')
                    $('#'+idDefinitivaLetrasP).text('Uno');
                    break;
                  case definitiva=2:
                    $('#'+idDefinitivaLetras).val('Dos')
                    $('#'+idDefinitivaLetrasP).text('Dos');
                    break;
                  case definitiva=3:
                    $('#'+idDefinitivaLetras).val('Tres')
                    $('#'+idDefinitivaLetrasP).text('Tres');
                    break;
                  case definitiva=4:
                    $('#'+idDefinitivaLetras).val('Cuatro')
                    $('#'+idDefinitivaLetrasP).text('Cuatro');
                    break;
                  case definitiva=5:
                    $('#'+idDefinitivaLetras).val('Cinco')
                    $('#'+idDefinitivaLetrasP).text('Cinco');
                    break;
                  case definitiva=6:
                    $('#'+idDefinitivaLetras).val('Seis')
                    $('#'+idDefinitivaLetrasP).text('Seis');
                    break;
                  case definitiva=7:
                    $('#'+idDefinitivaLetras).val('Siete')
                    $('#'+idDefinitivaLetrasP).text('Siete');
                    break;
                  case definitiva=8:
                    $('#'+idDefinitivaLetras).val('Ocho')
                    $('#'+idDefinitivaLetrasP).text('Ocho');
                    break;
                  case definitiva=9:
                    $('#'+idDefinitivaLetras).val('Nueve')
                    $('#'+idDefinitivaLetrasP).text('Nueve');
                    break;
                  case definitiva=10:
                    $('#'+idDefinitivaLetras).val('Diez')
                    $('#'+idDefinitivaLetrasP).text('Diez');
                    break;
                  case definitiva=11:
                    $('#'+idDefinitivaLetras).val('Once')
                    $('#'+idDefinitivaLetrasP).text('Once');
                    break;
                  case definitiva=12:
                    $('#'+idDefinitivaLetras).val('Doce')
                    $('#'+idDefinitivaLetrasP).text('Doce');
                    break;
                  case definitiva=13:
                    $('#'+idDefinitivaLetras).val('Trece')
                    $('#'+idDefinitivaLetrasP).text('Trece');
                    break;
                  case definitiva=14:
                    $('#'+idDefinitivaLetras).val('Catorce')
                    $('#'+idDefinitivaLetrasP).text('Catorce');
                    break;
                  case definitiva=15:
                    $('#'+idDefinitivaLetras).val('Quince')
                    $('#'+idDefinitivaLetrasP).text('Quince');
                    break;
                  case definitiva=16:
                    $('#'+idDefinitivaLetras).val('Dieciséis')
                    $('#'+idDefinitivaLetrasP).text('Dieciséis');
                    break;
                  case definitiva=17:
                    $('#'+idDefinitivaLetras).val('Diecisiete')
                    $('#'+idDefinitivaLetrasP).text('Diecisiete');
                    break;
                  case definitiva=18:
                    $('#'+idDefinitivaLetras).val('Dieciocho')
                    $('#'+idDefinitivaLetrasP).text('Dieciocho');
                    break;
                  case definitiva=19:
                    $('#'+idDefinitivaLetras).val('Diecinueve')
                    $('#'+idDefinitivaLetrasP).text('Diecinueve');
                    break;
                  case definitiva=20:
                    $('#'+idDefinitivaLetras).val('Veinte')
                    $('#'+idDefinitivaLetrasP).text('Veinte');
                    break;
                    }
                }
        });
    
    $("#enviar_acta_notas" ).click(function() {
        
        var form='#formcrearactasnotas';
        var gif=$('#gifbusq_avanz');
        var v=$(form).apiform_panel();
        var formCont=v.context(form);
        var panramentros={'gif':gif,'boton':this}
       
        if (formCont.campovacios=='no'){
         v.ajax.enviar(formCont.destino,formCont.datos,panramentros)
            }
        
    });
    
    $("#editar_acta_notas").click(function() {
        var form='#formeditaractasnotas';
        var gif=$('#gifbusq_avanz');
        var v=$(form).apiform_panel();
        var formCont=v.context(form);
        var panramentros={'gif':gif,'boton':this}
       
        if (formCont.campovacios=='no'){
         v.ajax.enviar(formCont.destino,formCont.datos,panramentros)
            }
        
    });
                    
    
});




           

            
            
