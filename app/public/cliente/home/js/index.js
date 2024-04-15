async function buscarCEP(cep) {
    const response = await fetch(`https://viacep.com.br/ws/${cep}/json/`);
    if (!response.ok) {
        throw new Error(`Erro ao buscar o CEP: ${response.statusText}`);
    }
    return await response.json();
}


function setupInputs() {
    let nomeInput = document.querySelector("#nomeCliente");
    let celularInput = document.querySelector("#celularCliente");
    let telefoneInput = document.querySelector("#telefoneCliente");
    let cepInput = document.querySelector("#cepCliente");
    let estadoInput = document.querySelector("#estadoCliente");
    let cidadeInput = document.querySelector("#cidadeCliente");
    let bairroInput = document.querySelector("#bairroCliente");
    let logradouroInput = document.querySelector("#logradouroCliente");
    let numeroInput = document.querySelector("#numeroCliente");
    // let complementoInput = document.querySelector("#complementoCliente");

    var options =  {
        onComplete: function(val, e, f) {
            if (!f.hasClass('is-valid')) {
                f.removeClass('is-invalid');
                f.addClass('is-valid');
            }
        },
        onInvalid: function(val, e, f, invalid, options){
            if (!f.hasClass('is-invalid')) {
                f.addClass('is-invalid');
            }
            if (f.hasClass('is-valid')) {
                f.removeClass('is-valid');
            }
        }
    };

    $('#celularCliente').mask('(00) 00000-0000', options);
    $('#telefoneCliente').mask('(00) 0000-0000', options);
    $("#cepCliente").mask('00000-000', options);


    nomeInput.addEventListener('focusout', () => {
        const regex = /^[a-zA-ZÀ-ÿ\s'-]*$/;
        const inputValue = nomeInput.value.trim(); // Remover espaços em branco no início e no final

        if (regex.test(inputValue) && inputValue.length >= 1) {
            nomeInput.classList.remove('is-invalid');
            nomeInput.classList.add('is-valid');
        } else {
            nomeInput.classList.remove('is-valid');
            nomeInput.classList.add('is-invalid');
        }
    });


    function validarTelefone(input) {
        if (input.value.length > 9) {
            input.classList.remove('is-invalid');
            input.classList.add('is-valid');
        } else {
            input.classList.remove('is-valid');
            input.classList.add('is-invalid');
        }
    }

    celularInput.addEventListener('focusout', () => {
        validarTelefone(celularInput);
    });

    telefoneInput.addEventListener('focusout', () => {
        validarTelefone(telefoneInput);
    });

    cepInput.addEventListener('focusout', async () => {
        if (cepInput.value.length !== 9) {
            // Se o CEP não estiver completo, adiciona a classe is-invalid
            cepInput.classList.add('is-invalid');
            return;
        }

        try {
            const responseCep = await buscarCEP(cepInput.value);
            estadoInput.value = responseCep.uf;
            cidadeInput.value = responseCep.localidade;
            bairroInput.value = responseCep.bairro;
            logradouroInput.value = responseCep.logradouro;
            cepInput.classList.remove('is-invalid');
        } catch (error) {
            console.error(error);
            cepInput.classList.add('is-invalid');
        }
    });


}






setupInputs() // Chame setupInputs() quando abrir o modal pela primeira vez











// document.querySelector('#celularCliente').addEventListener('blur', validatePhone);

// const reSpaces = /^[0-9]*$/;

// function validatePhone(e) {
//     const phone = document.querySelector('#celularCliente');
//     if (reSpaces.test(phone.value)) {
//       phone.classList.remove('is-invalid');
//       phone.classList.add('is-valid');
//       return true;
//     } else {
//       phone.classList.remove('is-valid');
  
//       phone.classList.add('is-invalid');
//       return false;
//     }
//   }

  