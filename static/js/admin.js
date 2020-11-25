$(document).ready(function(){
	$('input[type="checkbox"]').on('change', function(){
	    this.value ^= 1;
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