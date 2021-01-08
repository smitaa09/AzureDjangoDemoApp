

 function showModal(id){
     $("#"+id).modal();
}

function expandContent(myClass){
    $('.'+myClass).collapse('show');
}

function closeModal(id){
    $('#'+id).modal('toggle');
}


