# IP-logs-analyzer
Simple desktop GUI tool designed to analyze login histories in online games, websites or any other services. 
Analyzer can be used to assist in account recoveries, spot suspicious activities and identify potential risks (VPN, proxy, search robot, server and Tor exit node detection). It was used to help myself and my ex-teammates when dealing with more complicated cases.

App takes .csv files with login history (you need to specify names or indexes of columns containing IP and location) and displays them in 2 tables, first groupped by IP address, second by location. Tables show numbers of logins from each IP and location and corresponding percentage share of all logins.
Text field can be used to compare given IP address to those in login history by matching octets, (i.e. whether 0, 1, 2, 3 or 4 first octets of given IP matches with those in history).

