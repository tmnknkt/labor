function fillFilmList() {
    fetch('/lab7/rest-api/films/')
        .then(function (data) {
            return data.json();
        })
    .then(function (films) {
        let tbody = document.getElementById('film-list');
        tbody.innerHTML = ''; 
        
        for(let i = 0; i < films.length; i++) {
            let tr = document.createElement('tr'); 


            let tdTitleRus = document.createElement('td');
            let tdTitle = document.createElement('td');
            let tdYear = document.createElement('td');
            let tdActions = document.createElement('td'); 

            tdTitleRus.innerText = films[i].title_ru;
            
            if (films[i].title && films[i].title !== films[i].title_ru) {
                let originalTitleSpan = document.createElement('span');
                originalTitleSpan.className = 'original-title';
                originalTitleSpan.innerText = `(${films[i].title})`;
                tdTitle.appendChild(originalTitleSpan);
            } else {
                tdTitle.innerText = '-';
            }
            
            tdYear.innerText = films[i].year;

            let editButton = document.createElement('button');
            editButton.className = 'btn-edit';
            editButton.innerText = '✏️ Редактировать';

            editButton.onclick = function() {
                editFilm(i);        
            };

            let delButton = document.createElement('button');
            delButton.className = 'btn-delete';
            delButton.innerText = '🗑️ Удалить';

            delButton.onclick = function() {
                deleteFilm(i, films[i].title_ru);
            };

            tdActions.append(editButton);
            tdActions.append(delButton);

            tr.append(tdTitleRus);  
            tr.append(tdTitle);     
            tr.append(tdYear);
            tr.append(tdActions);

            tbody.append(tr);
        }
    })
    .catch(function (error) {
        console.error('Ошибка при загрузке фильмов:', error);
    });
}

function deleteFilm(id, title) { 
    if (!confirm(`Вы точно хотите удалить фильм "${title}"?`)) 
        return;

    fetch(`/lab7/rest-api/films/${id}`, {method: 'DELETE'})
        .then(function () {
            fillFilmList();
        })
        .catch(function(error) {
            console.error('Ошибка при удалении фильма:', error);
        });
}

function showModal() {
    document.getElementById('title-ru-error').innerText = '';
    document.getElementById('description-error').innerText = '';
    document.querySelector('div.modal').style.display = 'block';
    document.querySelector('.modal-overlay').style.display = 'block';
}

function hideModal() {
    document.querySelector('div.modal').style.display = 'none';
    document.querySelector('.modal-overlay').style.display = 'none';
}

function cancel() {
    hideModal();
}

function addFilm() {
    document.getElementById('title-ru-error').innerText = '';
    document.getElementById('description-error').innerText = '';
    
    document.getElementById('id').value = '';
    document.getElementById('title').value = '';
    document.getElementById('title-ru').value = '';
    document.getElementById('year').value = '';
    document.getElementById('description').value = '';
    
    document.getElementById('modal-title').textContent = 'Добавить фильм';
    
    showModal();
}

function sendFilm() {
    const id = document.getElementById('id').value;
    const titleRu = document.getElementById('title-ru').value;
    const titleOriginal = document.getElementById('title').value;
    const year = document.getElementById('year').value;
    const description = document.getElementById('description').value;
    
    const film = {
        title_ru: titleRu,
        title: titleOriginal,
        year: year,
        description: description
    };
    
    if (!film.title || film.title.trim() === '') {
        film.title = '';
    }

    const url = `/lab7/rest-api/films/${id}`;
    const method = id === '' ? 'POST' : 'PUT';

    document.getElementById('title-ru-error').innerText = '';
    document.getElementById('description-error').innerText = '';

    fetch(url, {
        method: method,
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(film)
    })
    .then(function(resp) {
        if(resp.ok) {
            fillFilmList();
            hideModal();
            return {};
        }
        return resp.json();
    })
    .then(function(errors) {
        if (errors) {
            if (errors.title_ru) {
                document.getElementById('title-ru-error').innerText = errors.title_ru;
            }
            if (errors.description) {
                document.getElementById('description-error').innerText = errors.description;
            }
        }
    })
    .catch(function(error) {
        console.error('Ошибка при отправке фильма:', error);
    });
}

function editFilm(id) {
    document.getElementById('title-ru-error').innerText = '';
    document.getElementById('description-error').innerText = '';
    
    fetch(`/lab7/rest-api/films/${id}`)
        .then(function(data) {
            return data.json();
        })
        .then(function(film) {
            document.getElementById('id').value = id;
            document.getElementById('title-ru').value = film.title_ru;
            
            if (film.title === film.title_ru) {
                document.getElementById('title').value = '';
            } else {
                document.getElementById('title').value = film.title;
            }
            
            document.getElementById('year').value = film.year;
            document.getElementById('description').value = film.description;
            
            document.getElementById('modal-title').textContent = 'Редактировать фильм';
            
            showModal();
        })
        .catch(function(error) {
            console.error('Ошибка при загрузке фильма для редактирования:', error);
        });
}

document.addEventListener('DOMContentLoaded', function() {
    const titleRuInput = document.getElementById('title-ru');
    const titleOriginalInput = document.getElementById('title');
    
    if (titleRuInput && titleOriginalInput) {
        titleRuInput.addEventListener('input', function() {
            if (!titleOriginalInput.value || titleOriginalInput.value === this.value) {
                titleOriginalInput.value = this.value;
            }
        });
        
        titleOriginalInput.addEventListener('input', function() {
            if (this.value !== titleRuInput.value) {
            }
        });
    }
});