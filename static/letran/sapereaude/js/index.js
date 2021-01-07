"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
function getHeaders(name = 'csrftoken') {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        document.cookie.split(';').forEach(cookie => {
            if (cookie.trim().substring(0, name.length + 1) === `${name}=`) {
                cookieValue = decodeURIComponent(cookie.trim().substring(name.length + 1));
            }
        });
        if (cookieValue && cookieValue !== '') {
            return {
                'Accept': 'application/json, text/plain, */*',
                'Content-Type': 'application/json',
                'X-CSRFToken': cookieValue
            };
        }
        else {
            return false;
        }
    }
    else {
        return false;
    }
}
function getFormatDate(fecha) {
    const monthsList = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Sep', 'Oct', 'Nov', 'Dic'];
    const datepub = String(fecha).split('-');
    const months = monthsList[Number(datepub[1]) - 1];
    const date = datepub[2];
    const year = datepub[0];
    return [year, months, date];
}
class EditionManager {
    constructor(slug, name, datepub, dateupdate) {
        this.slug = slug;
        this.name = name;
        this.datepub = datepub;
        this.dateupdate = dateupdate;
    }
}
class EditionsManager {
    constructor(urlall) {
        this.editions = new Array();
        this.urlall = urlall;
    }
    chargeAllData(element) {
        fetch(this.urlall)
            .then(response => {
            response.json()
                .then(data => {
                data.forEach(el => {
                    this.editions.push(new EditionManager(el.slug, el.name, el.datepub, el.dateupdate));
                    this.addToHTML(element, this.editions[this.editions.length - 1]);
                });
            });
        });
    }
    addToHTML(element, edition) {
        let html = document.querySelector(`#${element}`);
        let li = document.createElement('li');
        let a = document.createElement('a');
        a.href = `${edition.slug}`;
        a.innerHTML = `${edition.name}`;
        li.appendChild(a);
        html.appendChild(li);
    }
}
class SectionManager {
    constructor(slug, name) {
        this.name = name;
        this.slug = slug;
    }
}
class SectionsManager {
    constructor(urlall) {
        this.sections = new Array();
    }
    chargeAllData(element) {
        fetch(urls.section.all)
            .then((response) => {
            response.json().then((data) => {
                data.forEach((el) => {
                    this.sections.push(new SectionManager(el.slug, el.name));
                });
                this.addToHTML(element);
            });
        });
    }
    addToHTML(element) {
        let html = document.querySelector(`#${element}`);
        while (html.firstChild) {
            html.firstChild.remove();
        }
        this.sections.forEach(section => {
            let a = document.createElement('a');
            a.classList.add('p-2');
            a.classList.add('link-secondary');
            a.href = `${section.slug}`;
            a.innerHTML = `${section.name}`;
            html.appendChild(a);
        });
    }
}
class Author {
    constructor(slug, name, lastname, filial) {
        this.name = name;
        this.lastname = lastname;
        this.filial = filial;
        this.slug = slug;
    }
}
class ArticleManager {
    constructor(slug, title, subtitle, abstract, datepub, dateupdate, image, authors, section) {
        this.slug = slug;
        this.title = title;
        this.subtitle = subtitle;
        this.abstract = abstract;
        this.datepub = datepub;
        this.dateupdate = dateupdate;
        this.image = image;
        this.authors = new Array();
        this.getAuthors(authors);
        this.getSection(section);
    }
    getAuthors(filterauthors) {
        const data = JSON.stringify({
            authors: filterauthors
        });
        const headerCSRFToken = getHeaders();
        if (headerCSRFToken) {
            fetch(urls.author.all, {
                method: 'POST',
                body: data,
                headers: headerCSRFToken
            }).then(response => {
                response.json().then(data => {
                    data.forEach(el => {
                        this.authors.push(new Author(el.slug, el.name, el.lastname, el.filial));
                    });
                });
            });
        }
        else {
            throw new Error("403. CSRF caducado");
        }
    }
    getSection(filtersection) {
        const data = JSON.stringify({
            section: filtersection
        });
        const headerCSRFToken = getHeaders();
        if (headerCSRFToken) {
            fetch(urls.section.all, {
                method: 'POST',
                body: data,
                headers: headerCSRFToken
            }).then(response => {
                response.json().then(data => {
                    data.forEach(el => {
                        this.section = new SectionManager(el.slug, el.name);
                        try {
                            this.sectionHTMLElement.innerHTML = el.name;
                        }
                        catch (e) {
                        }
                    });
                });
            });
        }
    }
}
class ArticlesManager {
    constructor() {
        this.articles = new Array();
    }
    chargeAllData(element = '', elements = '') {
        fetch(urls.article.all).then(response => {
            response.json().then(data => {
                data.forEach(el => {
                    this.articles.push(new ArticleManager(el.slug, el.title, el.subtitle, el.abstract, el.datepub, el.dateupdate, el.image, el.authors, el.section));
                });
                if (element !== '') {
                    this.addToHighNews(element);
                }
                if (elements !== '') {
                    this.addToHighNews2(elements);
                }
            });
        });
    }
    addToHighNews(element) {
        let container = document.querySelector(`.${element}`);
        let title = container.querySelector('h1');
        let subtitle = container.querySelector('h6');
        let abstract = container.querySelector('p');
        this.randomnum = Math.floor(Math.random() * this.articles.length);
        const article = this.articles[this.randomnum];
        const fecha = getFormatDate(article.datepub);
        title.innerHTML = article.title;
        subtitle.innerHTML = `${article.subtitle} · ${fecha[2]}${fecha[1]}${fecha[0]}`;
        abstract.innerHTML = article.abstract.substring(0, (article.abstract.length > 150 ? 147 : article.abstract.length)) + '...';
    }
    addToHighNews2(element) {
        let i = 0;
        for (let k = 0; k <= this.articles.length; k++) {
            let container = document.querySelector(`.${element}-${i}`);
            let title = container.querySelector('h3');
            let section = container.querySelector('strong');
            let date = container.querySelector('div');
            let abstract = container.querySelector('p');
            let img = document.querySelector(`.${element}-${i}-img`);
            if (k !== this.randomnum) {
                const article = this.articles[k];
                const fecha = getFormatDate(article.datepub);
                title.innerHTML = article.title;
                this.articles[k].sectionHTMLElement = section;
                date.innerHTML = `${fecha[2]}${fecha[1]}`;
                abstract.innerHTML = article.abstract.substring(0, (article.abstract.length > 100 ? 97 : article.abstract.length)) + '...';
                img.src = article.image;
                i++;
            }
            if (i > 1) {
                break;
            }
        }
    }
}
class App {
    constructor() {
        this.editions = new EditionsManager(urls.edition.all);
        this.editions.chargeAllData('editions');
        this.sections = new SectionsManager(urls.section.all);
        this.sections.chargeAllData('nav');
        this.articles = new ArticlesManager();
        this.articles.chargeAllData('high-news', 'high-news');
        let editiontitle = document.querySelector('.edition-name');
        const data = JSON.stringify({
            edition: editiontitle.getAttribute('data-slug')
        });
        const headerCSRFToken = getHeaders();
        if (headerCSRFToken) {
            fetch(urls.edition.filter, {
                method: 'POST',
                body: data,
                headers: headerCSRFToken
            })
                .then(response => {
                response.json()
                    .then(data => {
                    console.log(data);
                    data.forEach(el => {
                        this.edition = new EditionManager(el.slug, el.name, el.datepub, el.dateupdate);
                        editiontitle.innerHTML = this.edition.name;
                    });
                });
            });
        }
    }
}
exports.App = App;
new App();
//# sourceMappingURL=index.js.map