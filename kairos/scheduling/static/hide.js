function DoCheckUncheckDisplay(d,dchecked1,dchecked2){
    if( d.checked == true ){
        document.getElementById(dchecked1).style.display = "block";
        document.getElementById(dchecked2).style.display = "block";
    }
    else{
        document.getElementById(dchecked1).style.display = "none";
        document.getElementById(dchecked2).style.display = "none";
    }
}