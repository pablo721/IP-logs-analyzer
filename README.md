# IP-logs-analyzer
Simple desktop GUI tool designed to analyze login histories in online games, websites or any other services. Can 
Analyzer can be used to assist in account recoveries, spot suspicious activities and check IP addresses using online fraud risk services (VPN, proxy, search robot, server and Tor exit node detection + general ISP risk score).

App takes .csv files with login history (you need to specify names or indexes of columns containing IP and location) and displays them in 2 tables, first groupped by IP address, second by location. Tables show numbers of logins from each IP and location and corresponding percentage share of all logins.
Last column of the table can be used to do octet by octet IP address comparison (i.e. whether 0, 1, 2, 3 or 4 octets of given IP matches with those in history).

