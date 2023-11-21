document.addEventListener('DOMContentLoaded', () => {
    const rmBtn = document.getElementById('btn-df');
    const radioBtns = document.getElementsByTagName('input');
    rmBtn.addEventListener('click', () => {
            for (let i; i < radioBtns.length; i++)
                radioBtns[i].checked = false;})
})
