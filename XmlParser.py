import re
class XmlParser(object):
    def __init__(self, xml_data):
        self.xml_data = xml_data

    def get_linkid_values(self):
        pattern_linkid = r'<documentlibrary:LinkId>(.*?)<\/documentlibrary:LinkId>'
        linkid_values = re.findall(pattern_linkid, self.xml_data)
        return linkid_values

    def get_total(self):
        pattern_total = r'<Total>(.*?)<\/Total>'
        total_value = re.search(pattern_total, self.xml_data)
        return int(total_value.group(1)) if total_value else None

    def get_status(self):
        pattern_status = r'<Response>.*?<Store>.*?<Status>(.*?)<\/Status>'
        status_value = re.search(pattern_status, self.xml_data, re.DOTALL)
        return int(status_value.group(1)) if status_value else None