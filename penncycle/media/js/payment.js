$.ajaxSetup({ 
  beforeSend: function(xhr, settings) {
    function getCookie(name) {
      var cookieValue = null;
      if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
          var cookie = jQuery.trim(cookies[i]);
          // Does this cookie string begin with the name we want?
          if (cookie.substring(0, name.length + 1) == (name + '=')) {
            cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
            break;
          }
        }
      }
      return cookieValue;
    }
    if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
      // Only send the token to relative URLs i.e. locally.
      xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
    }
  } 
});

$('#paybycredit').click(function(){
  createPayment();
  $('#payform').submit();
});

$('#paybycash').click(function(){
  var pcnum = $("#id_penncard").val();
  //createPayment();
  var plan = $("form#planform select option:selected");
  var href = '../../pay/cash/' + pcnum + "/" + plan.attr("name");
  window.location = href;
});

$('#paybybursar').click(function(){
  var pcnum = $("#id_penncard").val();
  //createPayment();
  var plan = $("form#planform select option:selected");
  var href = '../../pay/bursar/' + pcnum + "/" + plan.attr("name");
  window.location = href;
});

function appendPcnum (id, pcnum) {
  alert('append');
  var _href = $(id).attr('href');
  $(id).attr('href', _href + pcnum);
  console.log('appended');
}

function createPayment () {
  var pcnum = $("#id_penncard").val();
  var payInfo = {'pennid': pcnum};
  var plan = $("form#planform select option:selected");
  console.log("selected plan: " + plan.text());
  $.extend(payInfo, {'plan': plan.attr("name")});
  console.log(payInfo);

  $.ajax ({
    url: '../addpayment/',
    async: false,
    type: 'POST',
    data: payInfo,
    dataType: 'json',
    error: function(xhr, status, exception) {
      console.log(xhr);
      console.log(status);
      console.log(exception);
      alert('making payment failed');
    },
    success: function(data, status, xhr) {
      console.log('payment creation success');
    },
  });
  console.log("ajax call made");
  $("#amount-id").val(plan.attr("dollar"));
  console.log("replaced dollar form with " + (plan.attr("dollar")));
};
  
$('button#waiver-form').click(function(){
  toTab('pay');
  var pcnum = $("#id_penncard").val();
  console.log(pcnum);

  var payInfo = {'pennid': pcnum};
  var pennidData = $.param(payInfo);
  console.log(payInfo);
  console.log(pennidData);
  $.ajax ({
    url: '../verify_waiver/', 
    type: 'POST',
    data: payInfo,
    dataType: 'json',
    error: function(xhr, status, exception) {
      console.log(xhr);
      console.log(status);
      console.log(exception);
      alert('waiver failed');
    },
    success: function(data, status, xhr) {
      console.log('waiver success');
    },
  });


  var living_location = $("#id_living_location").val();
  console.log(living_location);
  if(living_location == "Stouffer") {
    $('div#pay').replaceWith('<h2>You\'ve already paid. Thanks!</h2>'); 
    console.log("replaced html");
  } else {
    $("#penncardnum-id").val();
    createPayment(payInfo);
  }
}); 
