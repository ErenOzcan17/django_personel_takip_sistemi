document.addEventListener('DOMContentLoaded', function() {
    const modal = document.getElementById("itirazModal");
    const span = document.getElementsByClassName("close")[0];
    const submitButton = document.getElementById("submitItiraz");
    let currentPrimId = null;

    document.querySelectorAll('.itiraz-button').forEach(button => {
        button.onclick = function() {
            currentPrimId = this.getAttribute('data-id');
            modal.style.display = "block";
        }
    });

    span.onclick = function() {
        modal.style.display = "none";
    }

    window.onclick = function(event) {
        if (event.target == modal) {
            modal.style.display = "none";
        }
    }

    submitButton.onclick = function() {
        const itirazAciklama = document.getElementById("itirazAciklama").value;

        fetch('', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({
                id: currentPrimId,
                itiraz_aciklama: itirazAciklama
            })
        })
        .then(response => response.json())
        .then(data => {
            if (!data.error) {
                alert(data.result);
                location.reload();
            } else {
                alert(data.result);
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });

        modal.style.display = "none";
    }

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});
