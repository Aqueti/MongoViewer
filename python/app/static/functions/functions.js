function count (obj) {
  var count = 0;
  for (var property in obj) {
      if (Object.prototype.hasOwnProperty.call(obj, property)) {
          count++;
      }
  }
  return count;
}

// Or you could just steal from compass? 

function DBSButtons(dbs, colls, location) {
  var container = document.getElementById("dropdown");

  while (container.hasChildNodes()) {
    container.removeChild(container.lastChild);
  }

  for(i=0;i<count(dbs);i++){

    var dbdropdown = document.createElement("BUTTON");
    dbdropdown.name = dbs[i];
    dbdropdown.innerHTML = dbs[i];
    dbdropdown.id = 'dropbtn';
    container.appendChild(dbdropdown);

    for(j=0;j<colls[i].length;j++){
      var newcontainer = dbdropdown;
      var collection = document.createElement("A");
      collection.innerHTML = colls[i][j];
      collection.id = 'dropdown-content';

      if( location == "database"){
        collection.href = '/database/' + dbs[i] + '/' + colls[i][j];
      }
      else if( location == "schema"){
        collection.href = '/schema/' + dbs[i] + '/' + colls[i][j];
      }
      else{
        collection.href = '/database/' + dbs[i] + '/' + colls[i][j];
      }
      newcontainer.appendChild(collection);
    }
  }
}

function showData(data) {
  var container = document.getElementById("submain");
  for(var index in data){
    spacecounter = 0;
    objdiv = document.createElement("DIV");
    objdiv.id = "objdiv";
    dbdiv(data[index], objdiv,spacecounter);
    container.appendChild(objdiv);
  }
}

function dbdiv(dbobject, container, spacecounter){
  var space = "";
  for(var i = 0; i<spacecounter; i++){
      space += "\xa0";
  }
  for( var key in dbobject){
    kvdiv = document.createElement("DIV");
    kvdiv.id = "kvdiv";
    if(typeof(dbobject[key])== "object"){
      if(spacecounter > 0){
        kvdiv.innerHTML = (space + "> " + key + " : object" );
      }
      else{
        kvdiv.innerHTML = (">" + key + " : object" );
      }
      innerdiv = document.createElement("DIV");
      innerdiv.id = "innerdiv";
      spacecounter ++;
      kvdiv.appendChild(innerdiv);
      container.appendChild(kvdiv);
      dbdiv(dbobject[key], innerdiv, spacecounter);
    }
    else{
        kvdiv.innerHTML = (space + key + " : " + dbobject[key]);
        container.appendChild(kvdiv);
    }
  }
}

function assignbuttonhref(db,coll){
  tabcont = document.getElementById('tabs');

  dbbutton = document.getElementById('dbbutton'); 
  schbutton = document.getElementById('schbutton');

  if(db == ""){
    dbbutton.href = "#";
    schbutton.href = "#";
  }
  else{
    dbbutton.href = "/database/" + db + "/" + coll;
    schbutton.href = "/schema/" + db + "/" + coll;
  }
}

function showSchema(schema) {

  container = document.getElementById('submain');

  // list of required (schema.required)

  try{
    for( var pitem in schema.properties){

      var schemadiv = document.createElement("DIV"); 
      schemadiv.id = "schemadiv";
      
      var propdiv = document.createElement("DIV");
      var descdiv = document.createElement("DIV");
      var typediv = document.createElement("DIV");
      var optionsdiv = document.createElement("DIV"); 
      var reqdiv = document.createElement("DIV");

      propdiv.id = "labeldiv";
      propdiv.innerHTML = ("Name : " + pitem);
      
      descdiv.id = "descdiv";
      descdiv.innerHTML = ("Description : " + schema.properties[pitem].description);
      
      typediv.id = "typediv";
      typediv.innerHTML = ("Type : " + schema.properties[pitem].bsonType);

      optionsdiv.id = "optionsdiv";
      optionsdiv.innerHTML = ("Options: ");

      
      for( var oitem in schema.properties[pitem])
      {

        if( oitem == "description" ){
        }else if (oitem == "bsonType"){
        }else{
          var inneroptions = document.createElement("DIV");
          inneroptions.innerHTML = ("\xa0" + oitem +" : "+  schema.properties[pitem][oitem]);
          optionsdiv.appendChild(inneroptions);
        }
      }
      
      if( schema.required.includes(pitem)){
        reqdiv.innerHTML = ("Required : YES");
      }else{
        reqdiv.innerHTML = ("Required : NO");
      }

      schemadiv.appendChild(propdiv);
      schemadiv.appendChild(typediv);
      schemadiv.appendChild(reqdiv);
      schemadiv.appendChild(descdiv);
      schemadiv.appendChild(optionsdiv);
      container.appendChild(schemadiv);
    }
  }
  catch(e){
    console.log(e);
    console.log("It's likely this collection has no schema");
    noschdiv = document.createElement("DIV");
    noschdiv.innerHTML = "No Schema Found";
    container.appendChild(noschdiv);
  }
}

function fillfieldbox(data){

  fieldboxinfo = [];
  fieldbox = document.getElementById("fieldboxdl");

  while(fieldbox.hasChildNodes()){
    fieldbox.removeChild(fieldbox.lastChild);
  }

  for(var item in data){
    for(var key in data[item]){
      if(!(fieldboxinfo.includes(key))){
        fieldboxinfo.push(key);
        option = document.createElement("OPTION");
        option.innerHTML = key;
        fieldbox.appendChild(option);
      }
    }
  }
}


function openeditschema(db, coll){

  var container = document.getElementById("submain");
  var schematext = document.getElementById("sneakyschema").innerHTML;

  while(container.hasChildNodes()){
    container.removeChild(container.lastChild);
  }

  var editbox = document.createElement("TEXTAREA");
  editbox.id = "schemaeditbox";
  editbox.cols = 90;
  editbox.rows = 45;
  editbox.innerHTML = schematext;

  document.getElementById("editbutton").onclick = function()  {submitSchema(db, coll);};
  document.getElementById("editbutton").innerHTML = "Submit";
  
  container.appendChild(editbox);
}

function submitSchema(db, coll){

  console.log(db);
  console.log(coll);
  
  schema = document.getElementById("schemaeditbox").innerHTML;
  
  reciever = ("/reciever/schema/" + db + "/" + coll);
  
  $.post(reciever, JSON.stringify(schema));
  
  document.location.reload(true);
}








// The following code does not work. I ran out of time trying to implement some kind of querying
//  up and running but it just didn't pan out. This code is not functional but might serve as a good point to
//  start from when trying to implement your own search function.

function filterKeyResults(){

  input = document.getElementById("fieldbox");
  submain = document.getElementById("submain");

  console.log(submain);

  divs = submain.getElementsByTagName('div');

  for(var thing in divs){
    try{
      if(divs[thing].id == "objdiv"){
        for(var item in divs[thing]){
          console.log(divs[thing][item].innerHTML);
          if(divs[thing][item].id == "kvdiv"){
            console.log("found kvdiv");
            if(divs[thing][item].innerHTML.indexOf("Child") !== -1){
              console.log(divs[thing][item]);
              submain.removeChild(divs[thing]);
            }
          }
        }
      }
    }
    catch(e){}
  }
  

/* 
  for each objdiv get value from fieldbox
    look through all keys 
    hide all objdivs that don't include that key


*/ 

}

function filterQueryResults(){

}