# -*- coding: utf-8 -*-
import requests
import base64
import re
import sys
import argparse
import xml.etree.ElementTree as ET
import traceback
from XmlParser import XmlParser

from wbxml import wbxml_parser
from as_code_pages import as_code_pages
from wapxml import wapxmltree, wapxmlnode
from Search import Search
from MSASHTTP import ASHTTPConnector
from ItemOperations import ItemOperations

wapxml_parser = wbxml_parser(*as_code_pages.build_as_code_pages())

def get_unc_listing(ip, username, password, unc_path):
    try:

        cmd = 'Search'
        search_xmldoc_req = Search.build(unc_path, username=username, password=password)
        
        as_conn = ASHTTPConnector(ip)
        as_conn.set_credential(username, password)
        #res = as_conn.post("Search", wapxml_parser.encode(search_xmldoc_req))
        content = as_conn.post("Search", wapxml_parser.encode(search_xmldoc_req))

        wapxml_res = wapxml_parser.decode(content)

        xml = str(wapxml_res)
        #print xml
        parser_xml = XmlParser(xml)
        linkid_values = parser_xml.get_linkid_values()
        get_total = parser_xml.get_total()
        status = parser_xml.get_status()

        if status == 5:
            print("[!] No access permission to access the %s ..." % (unc_path))
            return
        if get_total < 2:
            print("[!] Not Found %s Shares..." % (unc_path) )
            return
        else:
            print("[+] UNC %s list:" % (unc_path))
            for index, value in enumerate(linkid_values):
                if index == 0:
                    continue
                print("\t"+value)

        #filename = "get_unc_listing.txt"
        #print('[+] Save response file to %s'%(filename))
        #with open(filename, 'w+') as file_object:
        #    file_object.write(str(wapxml_res))

    except Exception as e:
            print('[!]Error:%s'%e)
            traceback.print_exc()


def get_unc_file(ip, username, password, unc_path):
    try:
        as_conn = ASHTTPConnector(ip)
        as_conn.set_credential(username, password)

        operation = {'Name': 'Fetch', 'Store': 'DocumentLibrary', 'LinkId': unc_path}
        operation['UserName'] = username
        operation['Password'] = password
        operations = [operation]

        xmldoc_req = ItemOperations.build(operations)
        res = as_conn.post("ItemOperations", wapxml_parser.encode(xmldoc_req))
        print res
        xmldoc_res = wapxml_parser.decode(res)
        responses = ItemOperations.parse(xmldoc_res)

        op, _, path, info, _ = responses[0]
        data = info['Data'].decode('base64')
        print data

    except Exception as e:
            print('[!]Error:%s'%e)
        
if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog="easBrowseShareFile.py",description='Use to browse the share file by eas(Exchange Server ActiveSync)',usage='%(prog)s 192.168.1.1 test@attck.com password1 listfile \\\\dc1\\SYSVOL\t\t\n%(prog)s 192.168.1.1 test@attck.com password1 readfile \\\\dc1\\SYSVOL\\test.com\\Policies\\{{6AC1786C-016F-11D2-945F-00C04fB984F9}}\\GPT.INI')
    parser.add_argument('host', help='Host name or IP address')
    parser.add_argument('user', help='User name for authentication')
    parser.add_argument('password', help='Password for authentication')
    parser.add_argument('mode', choices=['listfile', 'readfile'], help='Mode of operation')
    parser.add_argument('path', help='Path to file or directory')
    args = parser.parse_args()
    if args.mode == 'listfile':
        get_unc_listing(args.host, args.user, args.password, args.path)
    elif args.mode == 'readfile':
        get_unc_file(args.host, args.user, args.password, args.path)



    
