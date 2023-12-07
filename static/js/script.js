function closePhotos(){
    var btn = document.querySelector("#close-photos");
    btn.addEventListener('click', (e)=>{
        var container = document.querySelector("#container-content");
        container.removeChild(document.querySelector("#photos"));
        var records = document.querySelector("#records");
        records.classList.remove("col-lg-9");
    })
}

function atualizeContent(contentId) {
    $.ajax({
      url: window.location.href,
      method: 'GET',
      success: function (success) {
        replaceContent(success, '#' + contentId);
      },
    });
  }

function setForrmType(){
    var adminRadio = document.querySelector("#admin-radio");
    var clientRadio = document.querySelector("#client-radio");

    adminRadio.addEventListener('click', (event)=>{
       changeVal('d-block', 'd-none');
    })

    clientRadio.addEventListener('click', (event)=>{
        changeVal('d-none', 'd-block');
    })
}

function changeVal(toRemove, toAdd){
    const clientInputs = document.querySelectorAll(".client-form");

    for(var clientInput of clientInputs){
        clientInput.classList.remove(toRemove);
        clientInput.classList.add(toAdd);
    }
}

function resetForm(closeClass, modalId, formId, func = ()=>{} ) {
  
    $(document).on('click', closeClass, function (event) {
      $('.invalid-feedback').empty();
      $('#message').hide();
      $('.form-control').removeClass('is-invalid');
      let form = document.getElementById(formId);
      form.reset();
      func();
    });
  
    window.addEventListener('click', function (event) {
      var modal = document.getElementById(modalId);
      var form = document.getElementById(formId);
  
      if (event.target === modal) {
        func();
        $('#message').hide();
        form.reset();
      }
    });  
}


function formartCPF(element){
    $(document).ready(function() {
        $('#' + element).on('input', function() {
            var cpf = $(this).val();
            cpf = cpf.replace(/\D/g, '');
    
            if (cpf.length === 11) {
                cpf = cpf.replace(/(\d{3})(\d{3})(\d{3})(\d{2})/, '$1.$2.$3-$4');
            }

            console.log(cpf.length);
            $(this).val(cpf);
        });
    });
}

function formartPhone(element){
    $(document).ready(function() {
        $('#' + element).on('input', function() {
            var phone = $(this).val();
            phone = phone.replace(/\D/g, '');
    
            if (phone.length >= 11) {
                phone = phone.replace(/(\d{2})(\d{2})(\d{5})(\d{4})/, '+$1 ($2) $3-$4');
            } else if (phone.length > 2) {
                phone = phone.replace(/(\d{2})/, '+$1');
            }
    
            if (phone.length >= 19) {
                phone = phone.substring(0, 19);
            }
    
            $(this).val(phone);
        });
    });
}



function verifyResponse(formId, contentId, modalId, idModalMessage = null, func = ()=> {}, reset=true) {
    event.preventDefault(); // Evita o comportamento padrão do clique no botão
  
    $('.invalid-feedback').empty();
    $('.form-control').removeClass('is-invalid');
  
    var form = $('#' + formId)[0]; // Obtém o formulário
    var formData = new FormData(form); // Obtém os dados do formulário serializados
    console.log(formData);
    $.ajax({
      url: form.getAttribute('action'),
      type: 'POST',
      data: formData, // Envia os dados do formulário
      success: function (response) {
        try {
          var box = document.querySelector(".wrapper");
          box.classList.remove("show");
        } catch (error) {
    
        }
        
        // Manipula a resposta da solicitação AJAX
        if (response.success) {
          $("#" + modalId).modal('hide');
          let form = document.getElementById(formId);
          if(reset == true){
            form.reset();
          }
          $('.invalid-feedback').empty();
          $('.form-control').removeClass('is-invalid');
          $('#error-message-modal').hide();
          $('#error-message-modal-edit').hide();

          if((func.length < 0)){
            func();
          }

          setTimeout(function () {
            atualizeContent(contentId);
          }, 500);


          if(func.length > 0 && func.length < 3){
            func(response.success, response.message);
          }
          else if(func.length > 2){
            func(response.success, response.message, response);
          }
        } else {
  
          if (response.alert_in_modal) {
            var divContain = document.getElementById(idModalMessage);
  
            var message = "<div class='mt-4 alert alert-danger alert-white rounded d-flex justify-content-between'>" +
              "<div class='d-flex align-items-center'>" +
              "<span class='icon me-1'>" +
              "<i class='fa-solid fa-circle-exclamation'></i>" +
              "</span>" +
              "<strong class='me-2'>Erro! </strong>" +
              response.error +
              "</div>" +
              "<div class='text-center align-self-center'>" +
              "<button class='modal-close-alert btn-sm btn-danger text-light rounded-circle'><i class='fa fa-times-circle text-light'></i></button>" +
              "</div>" +
              "</div>";
  
            divContain.innerHTML = message;
            divContain.style.cssText = 'display: block !important;';
          }
          else if (response.alert) {
  
            $("#" + modalId).modal('hide');
            let form = document.getElementById(formId);
            form.reset();
            $('.invalid-feedback').empty();
            $('.form-control').removeClass('is-invalid');
  
            var divContain = document.getElementById("error-message");
  
            var message = "<div class='mt-4 alert alert-danger alert-white rounded d-flex justify-content-between'>" +
              "<div>" +
              "<div class='icon'>" +
              "<i class='fa-solid fa-circle-exclamation'></i>" +
              "</div>" +
              "<strong>Erro! </strong>" +
              response.error +
              "</div>" +
              "<div class='text-center align-self-center'>" +
              "<button id='close-alert' class='btn-sm btn-danger text-light rounded-circle'><i class='fa fa-times-circle'></i></button>" +
              "</div>" +
              "</div>";
  
            divContain.innerHTML = message;
            divContain.style.cssText = 'display: block !important;';
  
          }
          else {
            var errors = JSON.parse(response.errors);
            var formData = response.form_data;
  
            // Limpar erros de validação existentes
            $('.invalid-feedback').empty();
  
            // Exibir erros de validação no formulário
            $.each(errors, function (field, errorList) {
              var formControl = $('#' + formId + ' [name="' + field + '"]').closest('.form-control');
              var formGroup = formControl.closest('.form-group');
  
              $.each(errorList, function (index, error) {
                var errorMessage = error.message || '';
                var errorElement = $('<div class="invalid-feedback"></div>').text(errorMessage);
                formGroup.append(errorElement);
              });
  
              formControl.addClass('is-invalid');
              formControl.after(formGroup.find('.invalid-feedback'));
            });
  
            // Preencher os campos do formulário com os dados do formulário
            $.each(formData, function (name, value) {
              $('#' + formId + ' [name="' + name + '"]').val(value);
            });
  
          }
        }
      },
      error: function (xhr, status, error) {
        alert(error)
      },
      cache: false,
      contentType: false,
      processData: false
    });
  }

$(document).on('click', '.modal-close-alert', function (event) {
  event.preventDefault();
  var divContain = $(this).closest('[id*="error-message"]');
  divContain.hide();
});

function replaceContent(success, content, contentReplace = content) {
  let htmlData = $(success);
  let requestElement = htmlData.find(content);  
  let pageElement = $(contentReplace);  
  pageElement.replaceWith(requestElement);
}

function triggerAction(element, content, csrfToken, func = ()=>{}){
  $(document).on('click', '.' + element, function(event) {
    event.preventDefault();
  
    var url = $(this).attr('href');

    $.post(url,{csrfmiddlewaretoken: csrfToken}, function(data) {
      func(data.success, data.message);
      setTimeout(function () {
        atualizeContent(content);
      }, 100);
     
    });
  });
}

function closeMessage(){
  var button = document.querySelector("#close-message");
  button.addEventListener('click', (e)=>{
      var message = document.querySelector("#message");
      message.classList.remove('d-flex');
      message.classList.add('d-none');
    });
}

var func = (typeMsg, message)=>{
  var divMessage = document.querySelector("#message");
  var type = document.querySelector("#type-message");
  var content = document.querySelector("#content-message");
  var button = document.querySelector("#close-message");

  if (typeMsg == true){
    type.textContent = 'Sucesso';
    divMessage.classList.remove('alert-danger');
    divMessage.classList.add('alert-success');
    button.classList.remove('btn-danger');
    button.classList.add('btn-success');
  }
  else{
    type.textContent = 'Erro';
    divMessage.classList.remove('alert-success');
    divMessage.classList.add('alert-danger');
    button.classList.remove('btn-success');
    button.classList.add('btn-danger');
  }

  content.textContent = message;

  divMessage.classList.remove('d-none');
  divMessage.classList.add('d-flex');
}

function generateColors(length) {
  const startColor = "#d2b300";
  const endColor = "#0f1015";

  // Converte as cores para o formato RGBA
  const startRGB = hexToRgb(startColor);
  const endRGB = hexToRgb(endColor);

  // Gera uma sequência linear de cores no espaço RGB
  const colorsRGB = interpolateColors(startRGB, endRGB, length);

  // Converte as cores de volta para o formato hexadecimal
  const colorsHex = colorsRGB.map(rgbToHex);

  return colorsHex;
}

function hexToRgb(hex) {
  const bigint = parseInt(hex.slice(1), 16);
  const r = (bigint >> 16) & 255;
  const g = (bigint >> 8) & 255;
  const b = bigint & 255;
  return [r, g, b];
}

function rgbToHex(rgb) {
  return `#${((1 << 24) + (rgb[0] << 16) + (rgb[1] << 8) + rgb[2]).toString(16).slice(1)}`;
}

function interpolateColors(start, end, steps) {
  const stepFactor = 1 / (steps - 1);
  const interpolatedColors = [];

  for (let i = 0; i < steps; i++) {
    const r = Math.round(start[0] + i * stepFactor * (end[0] - start[0]));
    const g = Math.round(start[1] + i * stepFactor * (end[1] - start[1]));
    const b = Math.round(start[2] + i * stepFactor * (end[2] - start[2]));
    interpolatedColors.push([r, g, b]);
  }

  return interpolatedColors;
}

