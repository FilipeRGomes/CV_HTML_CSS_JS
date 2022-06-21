function verificar(params) {
    var data = new Date()
    var ano = data.getFullYear()
    var fano = document.getElementById('txtano')
    var res = document.querySelector('div#res')
        //var res = document.querySelector('div#res')

    //window.alert(fano)
    if (fano.value.length == 0 || fano.value > ano) {
        window.alert('Verifique os dados informados')
    } else {
        var fsex = document.getElementsByName('radsex')
        var idade = ano - Number(fano.value)
        var img = document.createElement('img')
        img.setAttribute('id', 'foto')
            //window.alert(`Idade Calculada ${idade}`)
        var genero = ''
        if (fsex[0].checked) {
            genero = 'Homem'
            img.setAttribute('src', 'imagens/manha.png')
        } else if (fsex[1].checked) {
            genero = 'Mulher'

            img.setAttribute('src', 'imagens/noite.png')
        }

        res.innerHTML = `Idade Calculada ${idade}, genero ${genero}`
        res.appendChild(img)
    }

}