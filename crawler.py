import scrapy

class CrawlerSpider(scrapy.Spider):
    name = "crawler"
   
    start_urls = ["https://itclinical.com/it.php"]

    def parse(self, response):
        SELETOR = ".portfolio-item"  # Seletor dos itens
        for categoria in response.css(SELETOR):
            # Extraindo o link 
            link_relativo = categoria.css("a::attr(href)").get()

            # a URL base com o link
            link_completo = response.urljoin(link_relativo)

            # Extraindo o nome do item
            nome = categoria.css("h5::text").get()

            # dicionário com os dados portfólio
            lista = {
                'nome': nome,
                'link': link_completo 
            }

            yield response.follow(link_completo, callback=self.parse_item, meta={'lista': lista})

    def parse_item(self, response):
        lista = response.meta['lista']

        # todo o texto dentro da classe body
        body_text = ' '.join(response.css('.body *::text').getall()).strip()

        if body_text:
            lista['body_text'] = body_text

        # dados da classe `tabs-nav`
        tabs_nav = []  # Lista para armazenar as informações dos itens

        # Capturando todos os elementos <li> dentro da classe `tabs-nav`
        for item in response.css('.tabs-nav li'):
            titulo = item.css('a::text').get()  # Título do link
            link_item = item.css('a::attr(href)').get()  # Link do item
            if titulo and link_item:
                # Adicionando ao dicionário
                tabs_nav.append({
                    'titulo': titulo.strip(),  
                    'link': response.urljoin(link_item)  
                })

        # Adicionando a lista de tabs_nav ao dicionário de dados
        lista['tabs_nav'] = tabs_nav

        # Retorna os dados completos
        yield lista
