$(document).ready(function(){

  $('#send_contact').click(function(){
    var nombre = $('#nombre').val()
    var email = $('#email').val()
    var mensaje = $('#mensaje').val()
    $.ajax({
      url: '/contact',
      data: {nombre: nombre, email: email, mensaje: mensaje},
      type: 'POST',
      success: function(response){
        $("#msg_mail").html("Hemos recibido tu mensaje, te contactaremos a la brevedad");
        $("#msg_mail").show();
      },
      error: function(error){
        console.log(error);
      }
    });
  });
  // Add smooth scrolling to all links
  $("a").on('click', function(event) {

    // Make sure this.hash has a value before overriding default behavior
    if (this.hash !== "") {
      // Prevent default anchor click behavior
      event.preventDefault();

      var $this = $(this);
      $this.closest('ul').find('.active').removeClass('active');
      $this.parent().addClass('active');

      // Store hash
      var hash = this.hash;
      // Using jQuery's animate() method to add smooth page scroll
      // The optional number (800) specifies the number of milliseconds it takes to scroll to the specified area
      $('html, body').animate({
        scrollTop: $(hash).offset().top
      }, 800, function(){
   
        // Add hash (#) to URL when done scrolling (default click behavior)
        window.location.hash = hash;
      });
    } // End if
  });
  function setActiveListElements(event){
    // Get the offset of the window from the top of page
    var windowPos = $(window).scrollTop();

        $('#mainav li a[href^="#"]').each(function() { 
            var anchorId = $(this);
      var target = $(anchorId.attr("href"));
      
      if (target.length > 0) {
        if (target.position().top - $('#header').outerHeight() <= windowPos) {
          $('#mainav li').removeClass("active");
          anchorId.parent().addClass('active');
        }
      }
    });
  }
    
  
  $(window).scroll(function() {
    setActiveListElements();
  });
});

// Open the Modal
function openModal(modal) {
  document.getElementById(modal).style.display = "block";
}


// Close the Modal
function closeModal(modal) {
  document.getElementById(modal).style.display = "none";
}

var slideIndex = 1;
//showSlides(slideIndex);

// Next/previous controls
function plusSlides(n, modal) {
  showSlides(slideIndex += n, modal);
}

// Thumbnail image controls
function currentSlide(n, modal) {
  showSlides(slideIndex = n, modal);
}

function showSlides(n, modal) {
  var i;
  var slides = document.getElementById(modal).getElementsByClassName("mySlides");
  var dots = document.getElementById(modal).getElementsByClassName("demo");
  var captionText = document.getElementById("caption_"+modal);
  if (n > slides.length) {slideIndex = 1}
  if (n < 1) {slideIndex = slides.length}
  for (i = 0; i < slides.length; i++) {
    slides[i].style.display = "none";
  }
  for (i = 0; i < dots.length; i++) {
    dots[i].className = dots[i].className.replace(" active", "");
  }
  slides[slideIndex-1].style.display = "block";
  dots[slideIndex-1].className += " active";
  captionText.innerHTML = dots[slideIndex-1].alt;
}