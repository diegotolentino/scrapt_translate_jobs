# coding: utf-8
from pyquery import PyQuery as pq
from feedformatter import Feed
import time

class translatorscafe():
    url_base = "http://www.translatorscafe.com"

    def get(self, url):
        print "Getting jobs from: %s" % url

        html = pq(url=url)

        itens = []

        for job in html("div#JobsPreview div.job"):
            # Create an item
            item = {}

            item["guid"] =   pq(job).find('div.hdr b').eq(1).html()

            item["pubDate"] = time.gmtime()
            #date = pq(job).find('div.hdr b').eq(1).html()

            item["description"] = item["title"] = pq(job).find('div.cnt table td a b').eq(0).html()

            url = pq(job).find('div.cnt table td a').eq(0).attr('href')

            #Se a url não for publica ignora o job
            if not url:
                print "Ignorando ";
                print item["title"]
                continue

            item["link"] = self.url_base + url

            item["description"] += "<br> Language: " +  pq(job).find('div.cnt table td.lng').eq(0).html()

            # Add item to feed
            itens.append(item)

        return itens

    def find(self, query):
        # Create the feed
        feed = Feed()

        # Set the feed/channel level properties
        feed.feed["title"] = "Translate jobs search: %s" % query
        feed.feed["link"] = "http://www.diegotolentino.com"
        feed.feed["author"] = "Diego Tolentino"
        feed.feed["description"] = u'Extrator de trabalhos de tradução'

        # @todo Aparentemente o "pq(url=url)" da função get() sempre guarda o cache da primeira url lido, não lendo os demais, por isso sempre será lido somente a primeira pagina

        for i in [1]:
            # get itens of the page
            for item in self.get( "%s/cafe/SearchJobs.asp?Page=%s" % (self.url_base, i)):
                # If query match in item
                if query.lower() in item["description"].lower():
                    # Retrieving the complete description for item
                    html = pq(url=item["link"])
                    item["description"] = html('table.jobTbl td.thinborder').eq(2).html()

                    # Add item to feed
                    feed.items.append(item)

        # Return the feed in rss2 format
        return feed.format_rss2_string()