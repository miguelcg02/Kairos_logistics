function hideShow(_check,_obj1,_obj2){
    if( _check.checked == true ){
        document.getElementById(_obj1).style.display = "block";
        document.getElementById(_obj2).style.display = "block";
    }
    else{
        document.getElementById(_obj1).style.display = "none";
        document.getElementById(_obj2).style.display = "none";
    }
}