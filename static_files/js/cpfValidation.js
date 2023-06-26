function validateCPF(input_cpf) {
    input_cpf.classList.add('red-border')
    strTemp = input_cpf.value;
    var strCPF = strTemp.replaceAll(".","").replaceAll("-","").replaceAll("_","");
    var Soma;
    var Resto;
    Soma = 0;
    if (strCPF == "00000000000")
        return false;
    for (i = 1; i <= 9; i++)
        Soma = Soma + parseInt(strCPF.substring(i - 1, i)) * (11 - i);
    Resto = (Soma * 10) % 11;
    if ((Resto == 10) || (Resto == 11))
        Resto = 0;
    if (Resto != parseInt(strCPF.substring(9, 10)))
        return false;
    Soma = 0;
    for (i = 1; i <= 10; i++)
        Soma = Soma + parseInt(strCPF.substring(i - 1, i)) * (12 - i);
    Resto = (Soma * 10) % 11;
    if ((Resto == 10) || (Resto == 11))
        Resto = 0;
    if (Resto != parseInt(strCPF.substring(10, 11)))
        return false;

    input_cpf.classList.remove('red-border');
    input_cpf.classList.add('green-border');
    return document.getElementById('btn-save-collaborator').disabled = false;
}






