$(document).ready(function(){
	$('input[type="checkbox"]').on('change', function(){
	    this.value ^= 1;
	});


  $('#carpeta').on('change', function(){
      var carpeta = this.value;
      if (carpeta=="servicios") {
        $("#select_servicio").show();
        $("#select_slider").show();
      }
      else{
        $("#select_servicio").hide();
        $("#select_slider").hide();
      }
  });
});

updateList = function() {
  var input = document.getElementById('files');
  var output = document.getElementById('fileList');

  output.innerHTML = '<ul>';
  for (var i = 0; i < input.files.length; ++i) {
    output.innerHTML += '<li>' + input.files.item(i).name + '</li>';
  }
  output.innerHTML += '</ul>';
}