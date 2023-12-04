const list = document.getElementById('list');
const search = document.getElementById('search');

const listItems = [];

search.addEventListener('input', (e) => filterInput(e.target.value))

getDataFormPublicAPI();

async function getDataFormPublicAPI() {
    const responseAPI = await fetch('https://randomuser.me/api?results=50')
    console.log(responseAPI);
    const { results } =  await responseAPI.json();
    console.log('result :>>',results);
    list.innerHTML = 'Loading...';
    setTimeout(() =>{
        results.forEach(element => {
            const divItem = document.createElement('div');
            listItems.push(divItem);
            divItem.innerHTML = `
            <img src="${element.picture.thumbnail}" alt="${element.email}">
            <div class="detail">
            <h2>${element.name.title}. ${element.name.first} ${element.name.last} </h2>
            <p>${element.email}</p>
            `;
            list.appendChild(divItem);
        });
    },2000);
   
}
function filterInput(keySearch) {
    const searchItem = keySearch.toLowerCase();
    listItems.forEach((item) => {
        if(item.innerHTML.toLowerCase().includes(searchItem)) {
            item.classList.remove('hidden');
        }else {
            item.classList.add('hidden');
    }
})
}