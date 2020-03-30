const add = document.getElementById('add')
const remove = document.getElementById('remove')
const quant = document.getElementById('quantity')

add.addEventListener('click', function () {
    quant.value = parseInt(quant.value) +1
})

remove.addEventListener('click', function () {
    value = parseInt(quant.value)
    if (value != 1){
        value = value -1
    }
    quant.value = value


})