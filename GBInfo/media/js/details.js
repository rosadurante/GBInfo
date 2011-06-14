
function display_details(isbn) {
    item = document.getElementById("" + isbn);
    if (item.getAttribute('style') == 'display:none;')
    {
        item.setAttribute('style', 'display:inherit;')
    }
    else
    {
        item.setAttribute('style', 'display:none;')
    }
}