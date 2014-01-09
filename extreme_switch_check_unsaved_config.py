#!/usr/bin/python

import re
import sys
import telnetlib
import getopt

state="OK: Config saved"
exit_state=0

def telnet_switch(hostname,username,password):
	try:
		tn = telnetlib.Telnet(hostname)

		tn.read_until("login: ")
		tn.write(username + "\n")
		tn.read_until("password: ")
		tn.write(password + "\n")

		tn.write("exit\n")
		tn.write("N\n")

		readout=tn.read_all()
		readout_list = [y for y in (x.strip() for x in readout.splitlines()) if y]
	except:
		return False
	return readout_list

def main(argv):
        helptext=(__file__)+' -s hostname -u username -p password'

        try:
		opts, args = getopt.getopt(argv,"hs:u:p:")
        except getopt.GetoptError:
                print "You are missing some options.\n"
                print helptext
                sys.exit(1)
        if not opts:
                print helptext
                sys.exit(1)
        for opt, arg in opts:
                if opt == '-h':
                        print helptext
                        sys.exit()
                elif opt in ('-s'):
			hostname=arg
                elif opt in ('-u'):
			username=arg
                elif opt in ('-p'):
			password=arg

        return hostname,username,password

if __name__ == "__main__":
        hostname,username,password=main(sys.argv[1:])

readout_list=telnet_switch(hostname,username,password)

if readout_list:
		for line in readout_list:
			if re.match("\*",line):
				state="WARNING: Config not saved"
				exit_state=1
else:
	print "Something went wrong"
	sys.exit(2)

print state
sys.exit(exit_state)
