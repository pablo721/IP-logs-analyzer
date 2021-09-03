# IP-logs-analyzer
Simple desktop tool designed to analyze login histories in online games (or whatever other services). 
Analyzer can be used to assist in account recoveries, determine account ownership or spot suspicious activity. 
App takes .csv files with login history and displays them in 2 tables, groupped by IP address and location. 
Tables show numbers of logins from each IP and location and percentage share of each number.
Last column of the table can be used to do octet by octet IP address comparison (i.e. whether 0, 1, 2, 3 or 4 octets of given IP matches with those in history).
Additionally, each IP address can be checked by an online scam detection service (whether given IP address is a VPN, public proxy, web proxy, search robot, server or Tor exit node).
