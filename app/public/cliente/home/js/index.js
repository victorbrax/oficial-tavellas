const cepInput = document.querySelector("#cepCliente");
const estadoInput = document.querySelector("#estadoCliente");
const cidadeInput = document.querySelector("#cidadeCliente");
const bairroInput = document.querySelector("#bairroCliente");
const logradouroInput = document.querySelector("#logradouroCliente");
const complementoInput = document.querySelector("#complementoCliente");
const message = document.querySelector("#messageForms");

const onlyNumbersRegex = /^[0-9]+$/;
const cepValidRegex = /^[0-9]{8}$/;

function validarCEP(cep) {
    if (!onlyNumbersRegex.test(cep) || !cepValidRegex.test(cep)) {
        throw new Error("CEP inválido.");
    }
}

async function buscarCEP(cep) {
    const response = await fetch(`https://viacep.com.br/ws/${cep}/json/`);
    if (!response.ok) {
        throw new Error(`Erro ao buscar o CEP: ${response.statusText}`);
    }
    return await response.json();
}

function exibirMensagemErro(mensagem) {
    message.textContent = mensagem;
    setTimeout(() => {
        message.textContent = "";
    }, 5000);
}

cepInput.addEventListener('focusout', async () => {
    try {
        validarCEP(cepInput.value);
        const responseCep = await buscarCEP(cepInput.value);

        estadoInput.value = responseCep.uf;
        cidadeInput.value = responseCep.localidade;
        bairroInput.value = responseCep.bairro;
        logradouroInput.value = responseCep.logradouro;
        complementoInput.value = responseCep.complemento;

    } catch (error) {
        exibirMensagemErro(error.message);
    }
});
