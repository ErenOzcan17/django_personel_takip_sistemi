document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('gorusmeForm').addEventListener('submit', function(event) {
        event.preventDefault();

        var form = event.target;
        var formData = new FormData(form);

        fetch(form.action, {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': '{{ csrf_token }}'
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                // Hata durumunda kullanıcıya bildirim gösterilebilir
                console.error(data.result);
            } else {
                // Başarılı durumda kullanıcıya bildirim gösterilebilir
                console.log(data.result);
                // Örneğin, başarılı kayıt sonrası formu temizlemek için:
                form.reset();
            }
        })
        .catch(error => {
            console.error('Bir hata oluştu:', error);
        });
    });
});
