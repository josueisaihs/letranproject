function getHeaders(name:string='csrftoken'){
    let cookieValue:string = null

    if (document.cookie && document.cookie !== ''){
        document.cookie.split(';').forEach(cookie=>{
            if (cookie.trim().substring(0, name.length + 1) === `${name}=`){
                cookieValue = decodeURIComponent(cookie.trim().substring(name.length + 1))
            }
        })

        if (cookieValue && cookieValue !== ''){
            return {
                'Accept': 'application/json, text/plain, */*', 
                'Content-Type': 'application/json', 
                'X-CSRFToken': cookieValue
            }
        }else{
            return false
        }        
    }else{
        return false
    }
}

function getFormatDate(fecha:Date){
    const monthsList:string[] = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Sep', 'Oct', 'Nov', 'Dic']
    const datepub = String(fecha).split('-')
    const months:string = monthsList[Number(datepub[1]) - 1]
    const date:string = datepub[2]
    const year:string = datepub[0]

    return [year, months, date]
}

class EditionManager {
    slug:string
    name:string
    datepub:Date
    dateupdate:Date

    constructor (slug:string, name:string, datepub:Date, dateupdate:Date){
        this.slug = slug
        this.name = name
        this.datepub = datepub
        this.dateupdate = dateupdate
    }
}

class EditionsManager {
    editions:Array<EditionManager>
    urlall:string

    constructor(urlall:string){
        this.editions = new Array()

        this.urlall = urlall
    }

    chargeAllData(element:string){
        fetch(this.urlall)
        .then(response => {
            response.json()
                .then(data=>{
                        data.forEach(el=>{
                                this.editions.push(
                                    new EditionManager(el.slug, el.name, el.datepub, el.dateupdate)
                                )
                                this.addToHTML(element, this.editions[this.editions.length - 1])
                            }                            
                        )                        
                    })
        })
    }

    addToHTML(element:string, edition:EditionManager){
        let html:HTMLElement = document.querySelector(`#${element}`) as HTMLElement

        let li = document.createElement('li')
        let a = document.createElement('a')
        a.href = `${edition.slug}`
        a.innerHTML = `${edition.name}`
        li.appendChild(a)
        
        html.appendChild(li)
    }
}

class SectionManager{
    slug:string
    name:string

    constructor(slug:string, name:string){
        this.name = name
        this.slug = slug
    }
}

class SectionsManager{
    sections:Array<SectionManager>

    constructor(urlall:string){
        this.sections = new Array()
    }

    chargeAllData(element:string){
        fetch(urls.section.all)
        .then((response) => {
            response.json().then((data)=>{
                        data.forEach(
                            (el)=>{
                                this.sections.push(
                                    new SectionManager(el.slug, el.name)
                                )
                            }                            
                        )
                        this.addToHTML(element)
                    })
        })
    }

    addToHTML(element:string){
        let html:HTMLElement = document.querySelector(`#${element}`) as HTMLElement
        while (html.firstChild){
            html.firstChild.remove()
        }

        this.sections.forEach(section => {
            let a = document.createElement('a')
            a.classList.add('p-2')
            a.classList.add('link-secondary')
            a.href = `${section.slug}`
            a.innerHTML = `${section.name}`
            
            html.appendChild(a)
        });
    }
}

class Author {
    slug:string
    name:string
    lastname:string
    filial:string

    constructor (slug:string, name:string, lastname:string, filial:name){
        this.name = name
        this.lastname = lastname
        this.filial = filial
        this.slug = slug
    }
}

class ArticleManager{
    slug:string
    title:string
    subtitle:string
    authors:Array<Author>
    abstract:string
    datepub:Date
    dateupdate:Date
    image:string
    section:SectionManager

    sectionHTMLElement:HTMLElement
    
    constructor(slug:string, title:string, subtitle:string, abstract:string, datepub:Date, dateupdate:Date,
        image:string, authors:Array<number>, section:number){
            this.slug = slug
            this.title = title
            this.subtitle = subtitle
            this.abstract = abstract
            this.datepub = datepub
            this.dateupdate = dateupdate
            this.image = image
            this.authors = new Array<Author>()

            this.getAuthors(authors)
            this.getSection(section)
    }

    getAuthors(filterauthors:Array<number>){
        const data = JSON.stringify({
            authors: filterauthors 
        })

        const headerCSRFToken:any = getHeaders()
        if (headerCSRFToken){
            fetch(urls.author.all, 
                {
                    method: 'POST', 
                    body: data, 
                    headers: headerCSRFToken
                }
            ).then(response=>{
                response.json().then(data=>{
                    data.forEach(el => {
                        this.authors.push(new Author(el.slug, el.name, el.lastname, el.filial))
                    });                    
                })
            })
        }else {
            throw new Error("403. CSRF caducado")            
        }
    }

    getSection(filtersection:number){
        const data = JSON.stringify({
            section: filtersection
        })
        const headerCSRFToken:any = getHeaders()
        if (headerCSRFToken){
            fetch(urls.section.all, 
                {
                    method: 'POST',
                    body: data,
                    headers: headerCSRFToken
                }
            ).then(response=>{
                response.json().then(data=>{
                    data.forEach(el => {
                        this.section = new SectionManager(el.slug, el.name)

                        try{
                            this.sectionHTMLElement.innerHTML = el.name
                        }catch (e){

                        }
                    });
                })
            }) 
        }
    }
}

class ArticlesManager {
    articles:Array<ArticleManager>
    randomnum:number

    constructor(){
        this.articles = new Array()
    }

    chargeAllData(element:string='', elements:string=''){
        fetch(urls.article.all).then(response=>{
            response.json().then(data=>{
                data.forEach(el => {
                    this.articles.push(
                        new ArticleManager(el.slug, el.title, el.subtitle, el.abstract, el.datepub, el.dateupdate, el.image, el.authors, el.section)
                    )
                }) 
                if (element !== ''){this.addToHighNews(element)}
                if (elements !== ''){this.addToHighNews2(elements)}
            })
        })
    }

    addToHighNews(element:string){
        let container:HTMLDivElement = document.querySelector(`.${element}`) as HTMLDivElement
        let title:HTMLElement = container.querySelector('h1') as HTMLElement
        let subtitle:HTMLElement = container.querySelector('h6') as HTMLElement
        let abstract:HTMLElement = container.querySelector('p') as HTMLElement
    
        this.randomnum = Math.floor(Math.random() * this.articles.length)      

        const article:ArticleManager = this.articles[this.randomnum]

        const fecha:string[] = getFormatDate(article.datepub)

        title.innerHTML = article.title
        subtitle.innerHTML = `${article.subtitle} · ${fecha[2]}${fecha[1]}${fecha[0]}`
        abstract.innerHTML = article.abstract.substring(0, (article.abstract.length > 150 ? 147 : article.abstract.length)) + '...'
    }

    addToHighNews2(element:string){
        let i = 0
        for (let k = 0; k <= this.articles.length; k++){
            let container:HTMLDivElement = document.querySelector(`.${element}-${i}`) as HTMLDivElement
            let title:HTMLElement = container.querySelector('h3') as HTMLElement
            let section:HTMLElement = container.querySelector('strong') as HTMLElement
            let date:HTMLElement = container.querySelector('div') as HTMLElement
            let abstract:HTMLElement = container.querySelector('p') as HTMLElement
            let img:HTMLImageElement = document.querySelector(`.${element}-${i}-img`) as HTMLImageElement

            if (k !== this.randomnum){
                const article:ArticleManager = this.articles[k]

                const fecha:string[] = getFormatDate(article.datepub)

                title.innerHTML = article.title
                this.articles[k].sectionHTMLElement = section
                date.innerHTML = `${fecha[2]}${fecha[1]}`
                abstract.innerHTML = article.abstract.substring(0, (article.abstract.length > 100 ? 97 : article.abstract.length)) + '...'
                img.src = article.image

                i++
            }

            if (i > 1){
                break
            }
        }
    }
}

export class App{
    edition:EditionManager
    editions:EditionsManager
    sections:SectionsManager
    articles:ArticlesManager

    constructor(){
        this.editions = new EditionsManager(urls.edition.all)
        this.editions.chargeAllData('editions')

        this.sections = new SectionsManager(urls.section.all)        
        this.sections.chargeAllData('nav')

        this.articles = new ArticlesManager()
        this.articles.chargeAllData('high-news', 'high-news')

        let editiontitle:HTMLElement = document.querySelector('.edition-name')
        const data = JSON.stringify({
            edition: editiontitle.getAttribute('data-slug')
        })
        const headerCSRFToken:any = getHeaders()
        if (headerCSRFToken){
            fetch(urls.edition.filter, {
                method: 'POST',
                body: data,
                headers: headerCSRFToken

            })
            .then(response => {
                response.json()
                    .then(data=>{
                            console.log(data)
                            data.forEach(el=>{
                                    this.edition = new EditionManager(el.slug, el.name, el.datepub, el.dateupdate)
                                    editiontitle.innerHTML = this.edition.name
                                }                            
                            )                        
                        })
            })
        }
    }
}

new App()
