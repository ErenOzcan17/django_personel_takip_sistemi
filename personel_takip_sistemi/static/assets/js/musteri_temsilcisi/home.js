document.getElementById('button1').addEventListener('click', function() {
    window.location.href = '/personel/musteri_temsilcisi/cagri_listesi_menu/'
});

document.getElementById('button2').addEventListener('click', function() {
    window.location.href = '/personel/musteri_temsilcisi/aylik_prim_listesi_menu/'
});

document.getElementById('button3').addEventListener('click', function() {
    window.location.href = '/personel/musteri_temsilcisi/yapilan_itirazlar/'
});

function showMessage(message) {
    document.getElementById('message').textContent = message;
}
