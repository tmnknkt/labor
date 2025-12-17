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

            // Создаем ячейки для данных
            let tdTitle = document.createElement('td');
            let tdTitleRus = document.createElement('td');
            let tdYear = document.createElement('td');
            let tdActions = document.createElement('td'); 

            // Заполняем данные
            tdTitle.innerText = films[i].title == films[i].title_ru ? '' : films[i].title;
            tdTitleRus.innerText = films[i].title_ru;
            tdYear.innerText = films[i].year;

            // Создаем кнопки действий
            let editButton = document.createElement('button');
            editButton.innerText = 'редактировать';
            
            let delButton = document.createElement('button');
            delButton.innerText = 'удалить';

            // Добавляем кнопки в ячейку действий
            tdActions.append(editButton);
            tdActions.append(delButton);

            // Добавляем ячейки в строку
            tr.append(tdTitle);
            tr.append(tdTitleRus);
            tr.append(tdYear);
            tr.append(tdActions);

            // Добавляем строку в таблицу
            tbody.append(tr);
        }
    })
    .catch(function (error) {
        console.error('Ошибка при загрузке фильмов:', error);
    });
}