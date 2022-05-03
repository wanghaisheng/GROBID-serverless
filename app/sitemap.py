try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET
from xml.dom import minidom
from datetime import datetime


class SiteMapXML(object):

    def __init__(self, website_content, prefix, domain):
        self.website_content = website_content
        self.prefix = prefix
        self.domain = domain
        self.root_metadata = {
            'name': 'urlset',
            'attrs': {
                'xmlns': 'http://www.sitemaps.org/schemas/sitemap/0.9'
            }
        }
        self.url_metadata = {
            'name': 'url',
            'attrs': {},
        }

    def build_url(self, prefix, domain, path):
        return '%s://%s%s' % (prefix, domain, path)

    def generate(self):

        # generate root element
        root_elem = ET.Element(self.root_metadata['name'])
        for attr_name, attr_value in self.root_metadata['attrs'].items():
            root_elem.set(attr_name, attr_value)

        comment = ET.Comment('SiteMap generated for DeliveryHero challenge')
        root_elem.append(comment)

        # generate children
        for path, obj in self.website_content.items():
            # url (element)
            url = self.build_url(self.prefix, self.domain, path)
            url_elem = ET.SubElement(root_elem, self.url_metadata['name'])

            # loc (url)
            url_child_elem = ET.SubElement(url_elem, 'loc')
            url_child_elem.text = url

            # lastmod (datetime)
            url_child_elem = ET.SubElement(url_elem, 'lastmod')
            url_child_elem.text = obj.get('lastmod')

        # output it as well
        output = self.prettify(root_elem)
        print('\n' + output + '\n')

        filename = 'sitemap.xml'
        print("# Generating %s file..." % filename)
        output_file = open(filename, 'w')
        output_file.write('<?xml version="1.0" encoding="UTF-8"?>')
        output_file.write(output)
        output_file.close()
        print("# Done!")

    def prettify(self, elem):
        """
        Return a pretty-printed XML string for the Element.
        <?xml version="1.0" encoding="UTF-8"?>
        <urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
           <url>
              <loc>http://www.example.com/</loc>
              <lastmod>2005-01-01 12:00:00</lastmod>
           </url>
        </urlset>
        """
        rough_string = ET.tostring(elem, 'utf-8')
        reparsed = minidom.parseString(rough_string)
        return reparsed.toprettyxml(indent="  ")
