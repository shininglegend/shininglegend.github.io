// Coming soon! Maybe? (Beyond scope of project to be handed in)

// Hide the navbar on admin pages
$(document).ready(function() {
    var path = window.location.pathname;
    if (path.startsWith("/admin")) {
        $("#mainNavBar").removeClass("navbar-expand-xl");
    } else {
        $("#mainNavBar").addClass("navbar-expand-xl");
    }
});

// Written by ChatGPT-4
document.addEventListener('DOMContentLoaded', function() {
    var currentPage = window.location.pathname;
    var textarea;
    var previousContent = "";

    // Make rows clickable on specific pages
    if (currentPage === "/" || currentPage === "/admin/client-journals") {
        var rows = document.getElementsByClassName("clickable-row");
        for (var i = 0; i < rows.length; i++) {
            rows[i].addEventListener("click", function() {
                window.location = this.dataset.href;
            });
        }
    }

    // Check if current URL matches pattern "/journals/##" or "/admin/respond/##"
    // and select the appropriate textarea
    if (/^\/journals\/\d{1,10}$/.test(currentPage)) {
        textarea = document.querySelector('#journal');
    } else if (/^\/admin\/respond\/\d{1,10}$/.test(currentPage)) {
        textarea = document.querySelector('#response');
    }

    // Load draft from local storage if it exists and textarea is present
    var savedDraft = localStorage.getItem(currentPage + '-draft');
    if (savedDraft && textarea) {
        textarea.value = savedDraft;
    }

    if (textarea) {
        // Check if textarea content has changed every 5 seconds
        setInterval(function() {
            if (textarea.value !== previousContent) {
                previousContent = textarea.value;
                localStorage.setItem(currentPage + '-draft', textarea.value); // Save to localStorage
                saveDraft();
            }
        }, 2500);
    }

    // Function to save draft
    function saveDraft() {
        fetch(`${currentPage}/autosave`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            credentials: 'same-origin', // include, same-origin, *omit
            body: `content=${encodeURIComponent(textarea.value)}`
        }).then(function() { // Removed 'data' from the function parameters as it wasn't being used
            localStorage.removeItem(currentPage + '-draft'); // Clear from localStorage using the correct key after successful server save
            // Update the save indicator
            var saveIndicator = document.querySelector("#save-indicator");
            saveIndicator.innerText = "Draft saved at " + new Date().toLocaleTimeString();
        });
    }
});