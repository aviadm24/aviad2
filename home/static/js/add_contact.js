
  $("#addContactForm").submit(function(event){
      event.preventDefault(); // prevent default submit behaviour
      // get values from FORM
      var user_name = $("input#user_name").val();
      var contact_name = $("input#contact_name").val();
      var email = $("input#email").val();
      var phone = $("input#phone").val();
      var user_name = user_name; // For Success/Failure Message
      // Check for white space in name for Success/Fail message
      if (user_name.indexOf(' ') >= 0) {
        user_name = user_name.split(' ').slice(0, -1).join(' ');
      }
      $this = $("#sendMessageButton");
      $this.prop("disabled", true); // Disable submit button until AJAX call is complete to prevent duplicate messages
//      console.log('name = '+user_name)
      $.ajax({
        url: "/add_contact",
        type: "POST",
        data: {
          user_name: user_name,
          contact_name: contact_name,
          phone: phone,
          email: email
        },
        cache: false,
        success: function() {
          // Success message
          console.log('Success')
          $('#success').html("<div class='alert alert-success'>");
          $('#success > .alert-success').html("<button type='button' class='close' data-dismiss='alert' aria-hidden='true'>&times;")
            .append("</button>");
          $('#success > .alert-success')
            .append("<strong>Your message has been sent. </strong>");
          $('#success > .alert-success')
            .append('</div>');
          //clear all fields
          $('#contactForm').trigger("reset");
        },
        error: function() {
          // Fail message
          console.log('Fail')
          $('#success').html("<div class='alert alert-danger'>");
          $('#success > .alert-danger').html("<button type='button' class='close' data-dismiss='alert' aria-hidden='true'>&times;")
            .append("</button>");
          $('#success > .alert-danger').append($("<strong>").text("Sorry " + firstName + ", it seems that my mail server is not responding. Please try again later!"));
          $('#success > .alert-danger').append('</div>');
          //clear all fields
          $('#contactForm').trigger("reset");
        },
        complete: function() {
          setTimeout(function() {
            $this.prop("disabled", false); // Re-enable submit button when AJAX call is complete
          }, 1000);
        }
      });
    });


/*When clicking on Full hide fail/success boxes */
$('#name').focus(function() {
  $('#success').html('');
});

// https://dev.to/mandaputtra/click-to-send-on-whatsapp-with-javascript-2anm
//// https://api.whatsapp.com/send?phone=+{{ *YOURNUMBER* }}&text=%20{{ *YOUR MESSAGE* }}

var yourNumber = "{{}}"
var yourMessage = "{{ your message in string }}"

// %20 mean space in link
// If you already had an array then you just join them with '%20'
// easy right

function getLinkWhastapp(number, message) {
  number = this.yourNumber
  message = this.yourMessage.split(' ').join('%20')
  url = 'https://api.whatsapp.com/send?phone=' + number + '&text=%20' + message;
  window.open(url, '_blank');
  return console.log('https://api.whatsapp.com/send?phone=' + number + '&text=%20' + message)
}

getLinkWhastapp()