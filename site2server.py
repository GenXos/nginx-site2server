#! /usr/bin/python

# script: getmapping.py
# author: Todd Fields
# date: 2015-08-21
# version: 0.1
#
# this script creates a Site to Server mapping based on the configs
# found in /etc/nginx/conf.d which are parsed to get server and port
# the site names are based on the file name. The generated page is
# created in /usr/share/nginx/html and is called site2server.html
#

from os import listdir
from os.path import isfile, join
from datetime import date

# variables
pathToConfigs = "/etc/nginx/conf.d/"
configFiles = [ f for f in listdir(pathToConfigs) if isfile(join(pathToConfigs,f)) ]

# add files to skipFiles if you do not wish for them to be parsed
skipFiles = ["default.conf", "vhost.template"]
today = date.today()

try:
# open an html file for writing out the page
  list_writer = open('/usr/share/nginx/html/site2server.html','w')
  list_writer.write("<html>\n")
  list_writer.write("<head><title>Site To Server Mapping</title>\n")
  # the table uses tablesorter from http://tablesorter.com to sort the table columns
  list_writer.write('<script type="text/javascript" src="tablesorter/jquery-latest.js"></script>\n') 
  list_writer.write('<script type="text/javascript" src="tablesorter/jquery.tablesorter.js"></script>\n')
  
  # dont know why but the webpage didnt/wouldnt recognize the external css page
  # probably something I did, but no time now to fix 
  list_writer.write("""<style>

    h1 {
        font-family:arial;
        font-size: 40px;
    }

    h3 {
        font-family:arial;
        font-size: 12px;
    }

    /* tables */
    table.tablesorter {
	font-family:arial;
	background-color: #CDCDCD;
	margin:10px 0pt 15px;
	font-size: 12pt;
	width: 100%;
	text-align: left;
    }
    table.tablesorter thead tr th, table.tablesorter tfoot tr th {
	background-color: #e6EEEE;
	border: 1px solid #FFF;
	font-size: 12pt;
	padding: 4px;
    }
    table.tablesorter thead tr .header {
	background-image: url(bg.gif);
	background-repeat: no-repeat;
	background-position: center right;
	cursor: pointer;
    }
    table.tablesorter tbody td {
	color: #3D3D3D;
	padding: 4px;
	background-color: #FFF;
	vertical-align: top;
    }
    table.tablesorter tbody tr.odd td {
	background-color:#F0F0F6;
    }
    table.tablesorter thead tr .headerSortUp {
	background-image: url(asc.gif);
    }
    table.tablesorter thead tr .headerSortDown {
	background-image: url(desc.gif);
    }
    table.tablesorter thead tr .headerSortDown, table.tablesorter thead tr .headerSortUp {
        background-color: #8dbdd8;
    }
  </style>\n""")

  list_writer.write('</head>\n')
  list_writer.write("<body>\n")
  list_writer.write('<h1 align="center">Site to Server Mapping</h1>\n')
  list_writer.write('<h3 align="center">Updated: ' + str(today) + '</h3>\n') 
  list_writer.write("""<script>
    $(document).ready(function() 
    { 
        $("#myTable").tablesorter( {sortList: [[0,0], [1,0]]} ); 
    } 
    );
  </script>\n""")
  list_writer.write('<table align="center" id="myTable" class="tablesorter">\n')
  list_writer.write('<thead><tr><th width="30%" align="center">Site</th><th width="30%" align="center">Server</th><th width="30%" align="center">Port</th></tr></thead>\n')
  list_writer.write('<tbody>\n')
  # Get a list of the config files
  #mapping = {}
  for file in configFiles:
    if file not in skipFiles:
      in_file = open(pathToConfigs + file, "r")
      text = in_file.readlines()
      in_site = file.split('.')
      # got the site name based on our naming convention of config files
      site = in_site[0]
      in_file.close()

      # find the server and ports from the proxy pass line and strip it out
      for line in text:
        line.strip()
        if "proxy_pass" in line:
          server_port = line.split('//')
          server_port = server_port[1]
          server_port = server_port.translate(None, ";")
          server = server_port.split('_')
          port = server[1].rstrip('\n')
          server = server[0]

      row = '<tr><td>' + site + '</td><td>' + server + '</td><td>' + port + '</td></tr>\n'

      list_writer.write(row)

      mapping = {
          site: [server, port]
      }

      print(mapping)
  list_writer.write("<h3>Number of Sites: " + len(mapping) + "</h3>\n")
  list_writer.write("</tbody>")
  list_writer.write("</body>\n")
  list_writer.write("</html>\n")
  list_writer.close()
except Exception as exception:
  pass
