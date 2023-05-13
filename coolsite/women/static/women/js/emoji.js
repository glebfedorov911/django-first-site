var dep = document.querySelector('.dep-button');
var emoji = ['❤', '🤣', '🤔', '😍', '😢', '🤬'];
var lst = [];
var textar = document.querySelector('#id_text');
var div_emoji = document.querySelector('.emoji');

emoji.forEach(e => {
    lst.push(document.createElement('div'));
    lst[lst.length-1].innerHTML = e;
    div_emoji.appendChild(lst[lst.length-1]);
    lst[lst.length-1].style.display = 'none';
    lst[lst.length-1].style.webkitUserSelect = 'none';
})

function emoji_list(e) {
    for(let i of lst) {
        i.style.display = (i.style.display=='none') ? 'inline' : 'none';
    }
}

dep.addEventListener('click', emoji_list);

function func(e) {
    textar.value += this.innerHTML
}

lst.forEach(l => l.addEventListener('click', func));