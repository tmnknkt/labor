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
                    originalTitleSpan.innerText = films[i].title;
                    tdTitle.appendChild(originalTitleSpan);
                } else {
                    tdTitle.innerText = '-';
                }
                
                tdYear.innerText = films[i].year;
                
                let editButton = document.createElement('button');
                editButton.className = 'btn-edit';
                editButton.innerText = '✏️ Редактировать';
                
                editButton.onclick = function() {
                    editFilm(films[i].id);
                };
                
                let delButton = document.createElement('button');
                delButton.className = 'btn-delete';
                delButton.innerText = '🗑️ Удалить';
                
                delButton.onclick = function() {
                    deleteFilm(films[i].id, films[i].title_ru);
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
        .then(function (response) {
            if (response.status === 204) {
                fillFilmList();
            } else {
                return response.json();
            }
        })
        .then(function(errorData) {
            if (errorData && errorData.error) {
                alert('Ошибка при удалении: ' + errorData.message);
            }
        })
        .catch(function(error) {
            console.error('Ошибка при удалении фильма:', error);
            alert('Произошла ошибка при удалении фильма');
        });
}

function showModal() {
    document.getElementById('title-ru-error').innerText = '';
    document.getElementById('title-error').innerText = '';
    document.getElementById('year-error').innerText = '';
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
    document.getElementById('title-error').innerText = '';
    document.getElementById('year-error').innerText = '';
    document.getElementById('description-error').innerText = '';
    
    document.getElementById('id').value = '';
    document.getElementById('title').value = '';
    document.getElementById('title-ru').value = '';
    document.getElementById('year').value = '';
    document.getElementById('description').value = '';
    
    const charsCounter = document.getElementById('chars-counter');
    if (charsCounter) {
        charsCounter.textContent = '2000';
        charsCounter.style.color = '#7f8c8d';
    }
    
    document.getElementById('modal-title').textContent = 'Добавить фильм';
    
    showModal();
}

function validateForm() {
    const titleRu = document.getElementById('title-ru').value.trim();
    const titleOriginal = document.getElementById('title').value.trim();
    const year = document.getElementById('year').value.trim();
    const description = document.getElementById('description').value.trim();
    const currentYear = new Date().getFullYear();
    
    document.getElementById('title-ru-error').innerText = '';
    document.getElementById('title-error').innerText = '';
    document.getElementById('year-error').innerText = '';
    document.getElementById('description-error').innerText = '';
    
    let isValid = true;
    
    if (!titleRu) {
        document.getElementById('title-ru-error').innerText = 'Заполните русское название';
        isValid = false;
    } else if (titleRu.length > 255) {
        document.getElementById('title-ru-error').innerText = 'Русское название не должно превышать 255 символов';
        isValid = false;
    }
    
    if (!titleOriginal) {
        document.getElementById('title-error').innerText = 'Заполните оригинальное название';
        isValid = false;
    } else if (titleOriginal.length > 255) {
        document.getElementById('title-error').innerText = 'Оригинальное название не должно превышать 255 символов';
        isValid = false;
    }
    
    if (!year) {
        document.getElementById('year-error').innerText = 'Укажите год выпуска';
        isValid = false;
    } else {
        const yearNum = parseInt(year);
        if (isNaN(yearNum)) {
            document.getElementById('year-error').innerText = 'Год должен быть числом';
            isValid = false;
        } else if (yearNum < 1895 || yearNum > currentYear) {
            document.getElementById('year-error').innerText = `Год должен быть в диапазоне от 1895 до ${currentYear}`;
            isValid = false;
        }
    }
    
    if (!description) {
        document.getElementById('description-error').innerText = 'Заполните описание';
        isValid = false;
    } else if (description.length > 2000) {
        document.getElementById('description-error').innerText = 'Описание не должно превышать 2000 символов';
        isValid = false;
    }
    
    return isValid;
}

function sendFilm() {
    if (!validateForm()) {
        return;
    }
    
    const id = document.getElementById('id').value;
    const titleRu = document.getElementById('title-ru').value.trim();
    const titleOriginal = document.getElementById('title').value.trim();
    const year = document.getElementById('year').value.trim();
    const description = document.getElementById('description').value.trim();
    
    const film = {
        title_ru: titleRu,
        title: titleOriginal,
        year: parseInt(year),
        description: description
    };
    
    const url = `/lab7/rest-api/films/${id}`;
    const method = id === '' ? 'POST' : 'PUT';
    
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
            if (errors.title) {
                document.getElementById('title-error').innerText = errors.title;
            }
            if (errors.year) {
                document.getElementById('year-error').innerText = errors.year;
            }
            if (errors.description) {
                document.getElementById('description-error').innerText = errors.description;
            }
        }
    })
    .catch(function(error) {
        console.error('Ошибка при отправке фильма:', error);
        alert('Произошла ошибка при сохранении фильма');
    });
}

function editFilm(id) {
    document.getElementById('title-ru-error').innerText = '';
    document.getElementById('title-error').innerText = '';
    document.getElementById('year-error').innerText = '';
    document.getElementById('description-error').innerText = '';
    
    fetch(`/lab7/rest-api/films/${id}`)
        .then(function(data) {
            return data.json();
        })
        .then(function(film) {
            document.getElementById('id').value = film.id;
            document.getElementById('title-ru').value = film.title_ru;
            document.getElementById('title').value = film.title;
            document.getElementById('year').value = film.year;
            document.getElementById('description').value = film.description;
            
            const charsCounter = document.getElementById('chars-counter');
            if (charsCounter) {
                const remaining = 2000 - film.description.length;
                charsCounter.textContent = remaining;
                
                if (remaining < 0) {
                    charsCounter.style.color = '#e74c3c';
                } else if (remaining < 100) {
                    charsCounter.style.color = '#f39c12';
                } else {
                    charsCounter.style.color = '#7f8c8d';
                }
            }
            
            document.getElementById('modal-title').textContent = 'Редактировать фильм';
            
            showModal();
        })
        .catch(function(error) {
            console.error('Ошибка при загрузке фильма для редактирования:', error);
            alert('Произошла ошибка при загрузке фильма');
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
    }
    
    const descriptionInput = document.getElementById('description');
    const charsCounter = document.getElementById('chars-counter');
    
    if (descriptionInput && charsCounter) {
        descriptionInput.addEventListener('input', function() {
            const remaining = 2000 - this.value.length;
            charsCounter.textContent = remaining;
            
            if (remaining < 0) {
                charsCounter.style.color = '#e74c3c';
            } else if (remaining < 100) {
                charsCounter.style.color = '#f39c12';
            } else {
                charsCounter.style.color = '#7f8c8d';
            }
        });
    }
});
