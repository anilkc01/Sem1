function searchTable() {
    var input, filter, table, tr, td, i, txtValue;
    input = document.getElementById("searchInput");
    filter = input.value.toUpperCase();
    table = document.getElementById("stockTable");
    tr = table.getElementsByTagName("tr");

    // Loop through all table rows, and hide those who don't match the search query
    for (i = 1; i < tr.length; i++) {
        td = tr[i].getElementsByTagName("td")[0]; // Check only the first column (symbol)
        if (td) {
            txtValue = td.textContent || td.innerText;
            if (txtValue.toUpperCase().indexOf(filter) > -1) {
                tr[i].style.display = "";
            } else {
                tr[i].style.display = "none";
            }
        }
    }
}

setTimeout(function() {
    const flashMessage = document.querySelector('.flash-message');
    if (flashMessage) {
        flashMessage.style.opacity = 0;
        setTimeout(function() {
            flashMessage.style.display = 'none';
        }, 500);  // Matches the fade-out duration
    }
}, 3000);

function openPopup(action) {
    fetch(`/${action}`) // Dynamically fetch buy.html or sell.html
        .then(response => response.text())
        .then(html => {
            document.getElementById("popup-container").innerHTML = html;
            document.getElementById("popup-container").style.display = "block";
        });
}

function closePopup() {
    document.getElementById("popup-container").style.display = "none";
}

window.openPopup = openPopup;
window.closePopup = closePopup;


function showReceipt() {
    
    var inp_symbol = document.getElementById("symbol");
    var inp_quantity = document.getElementById("quantity");
    var selectedOption = document.querySelector(`option[value="${inp_symbol.value}"]`);

    if (!inp_symbol) {
        alert("Please select a valid stock symbol!");
        return;
    }

    var ltp = parseFloat(selectedOption.dataset.ltp) || 0;
    var quantity = inp_quantity.value;
    var total = (ltp * quantity).toFixed(2);

    if (!quantity || quantity <= 0) {
        alert("Enter a valid quantity!");
        return;
    }


    document.getElementById("r_symbol").innerText = inp_symbol.value;
    document.getElementById("r_price").innerText = ltp;
    document.getElementById("r_quantity").innerText = quantity;
    document.getElementById("r_total").innerText = total;

   
    document.getElementById("h_symbol").value = inp_symbol.value;
    document.getElementById("h_price").value = ltp;
    document.getElementById("h_quantity").value = quantity;
    document.getElementById("h_total").value = total;

    document.getElementById("receipt").style.display = "block";
}