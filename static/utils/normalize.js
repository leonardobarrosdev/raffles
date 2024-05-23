const formCpf = document.getElementById('register_form');

formCpf.addEventListener('submit', (e) => {
  e.preventDefault();
  const inputCpf = document.getElementById('valid-cpf').value;
  const cpf = inputCpf.replace(/[^\d]+/g, '');
  const phoneNumber = document.getElementById('cellfone').value.trim();

  if(validateCPF(cpf)) {
    // Need return a error to class
    return true
  }
  if(validatePhoneNumber(phoneNumber)) {
    // Need return a error to class
    return true
  }

  document.getElementsByClassName('msg-error').innerHTML = '\
    <div class="alert alert-danger" role="alert">\
      A simple danger alert with <a href="#" class="alert-link">an example link</a>. Give it a click if you like.\
    </div>';
})

function validateCPF(cpf) {
  if(cpf.length != 11 || cpf == '') return false;
  // Eliminate known invalid CPF
  if (cpf == "00000000000" ||
      cpf == "11111111111" ||
      cpf == "22222222222" ||
      cpf == "33333333333" ||
      cpf == "44444444444" ||
      cpf == "55555555555" ||
      cpf == "66666666666" ||
      cpf == "77777777777" ||
      cpf == "88888888888" ||
      cpf == "99999999999")
    return false;
  // Verify if exist
  return true;
}

function validatePhoneNumber(phoneNumber) {
  const pattern = /^\d{10}$/;
  const isValid = pattern.test(phoneNumber);
  return isValid;
}
