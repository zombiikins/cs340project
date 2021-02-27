// help functions to make clicked row editable or deletable

function editClick(event){
  if(event.target.value == "See Patient"){
    event.target.type = "submit";
    var id = "row" + event.target.id;
    var row = document.getElementById(id).elements;
    for(var i=0;i<row.length;i++){
      row[i].disabled = false;
    }
  }
  if(event.target.value == "See Provider"){
    event.target.type = "submit";
    var id = "row" + event.target.id;
    var row = document.getElementById(id).elements;
    for(var i=0;i<row.length;i++){
      row[i].disabled = false;
    }
  }
  else if(event.target.value == "Edit"){
    event.target.type = "submit";
    event.target.value = "Done";
    event.preventDefault();
    var id = "row" + event.target.id;
    var row = document.getElementById(id).elements;
    for(var i=0;i<row.length;i++){
      row[i].disabled = false;
    }
    row[0].readOnly = "true";
  }
  else if(event.target.value == "Delete"){
    event.target.value = "Confirm?";
  }
  else if(event.target.value == "Confirm?"){
    event.target.type = "submit";
    var id = "row" + event.target.id;
    var row = document.getElementById(id).elements;
    for(var i=0;i<row.length;i++){
      row[i].disabled = false;
    }
  }
}