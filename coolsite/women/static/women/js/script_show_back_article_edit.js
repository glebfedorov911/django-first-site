var edit_button = document.querySelector('.edit');
var edit_article = document.querySelector('.edit_article');
var articlefull = document.querySelector('.articlefull');
var cancellation = document.querySelector('.cancellation');
var pages = document.querySelector('.list-pages');
var edit_form = document.querySelector('.edit_form');
var form_error = document.querySelector('.form_error');

function showing(e) {
    articlefull.style.display = 'none';
    edit_article.style.display = 'block';
    cancellation.style.display = 'block';
    edit_button.style.display = 'none';
    pages.style.display = 'none';
}

function back(e) {
    articlefull.style.display = 'block';
    edit_article.style.display = 'none';
    cancellation.style.display = 'none';
    edit_button.style.display = 'block';
    pages.style.display = 'block';
}

edit_button.addEventListener('click', showing);
cancellation.addEventListener('click', back);
edit_form.addEventListener('click', back);
