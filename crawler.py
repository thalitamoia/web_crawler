import scrapy

class CrawlerSpider(scrapy.Spider):
    name = "crawler"
    start_urls = ["https://itclinical.com/it.php"]

    # extração dos links e nomes
    def parse(self, response):
        SELETOR = ".portfolio-item"  # Seletor CSS para itens de portfólio
        for categoria in response.css(SELETOR):
            # link relativo com o link completo
            link_relativo = categoria.css("a::attr(href)").get()
            link_completo = response.urljoin(link_relativo)

            # Extraindo o nome do item
            nome = categoria.css("h5::text").get()

            # dicionário com as informações básicas
            lista = {
                'nome': nome,
                'link': link_completo
            }

            
            yield response.follow(link_completo, callback=self.parse_item, meta={'lista': lista})

     # Adicionando o método parse_item para coletar mais informações de cada item
    def parse_item(self, response):
        lista = response.meta['lista']  

        # Extraindo o texto da classe body
        body_text = ' '.join(response.css('.body *::text').getall()).strip()

        if body_text:
            lista['body_text'] = body_text

        # Retorna o dicionário atualizado
        yield lista