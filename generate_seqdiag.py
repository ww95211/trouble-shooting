__author__ = 'weifshen'

# Install seqdiag
# easy_install seqdiag
# brew install zlib #install zlib if need

import sys
import os
import re

import cmr_events

def find_event(events, key) :
	for e in cmr_events._events:
		if key in cmr_events._events[e]:
			return cmr_events._events[e][key]
	return None

def collect_events(fn, conf_id) :
	ret = []
	cmd = ''
	first = True
	for e in cmr_events._events:
		for e1 in cmr_events._events[e]:
			if not first:
				cmd = cmd + '|' + e1
			else:
				cmd =  e1
				first = False
	cmd = cmd.replace('[','\[')
	cmd = cmd.replace(']','\]')
	cmd = cmd.replace('(','\(')
	cmd = cmd.replace(')','\)')

	regs=r'^\[(\d+[/]\d+[/]\d+ \d+[:]\d+[:]\d+[.]\d+).*'+conf_id+'.*('+cmd+')(.*)$'
	f=open(fn)
	for line in f:
		m=re.match(regs,line)
		if (m is not None):
			obj = find_event(cmr_events._events,m.group(2))
			msg = obj['call'] + ' [label="' +  obj['label'] + '(' + m.group(1)
			for i in range(2, len(m.groups())) :
				if len(m.group(i + 1)) > 0:
					msg = msg + ',' + m.group(i + 1)
			msg = msg + ')"]'
			if 'ext-call' in obj:
				msg = msg + '{' + obj['ext-call'] + ' [label="' +  obj['label'] + '(' + m.group(1) + ')"];}'
			msg = msg + ';'
			ret.append(msg)
	f.close()
	return ret


def generate_seqdiag(fn , conf_id) :

	f = open ( 'callflow-'+conf_id+'.diag', 'w' )
	if f is not None :
		f.write('{')
		f.write('edge_length = 300;')
		f.write('span_height = 80;')
		f.write('default_fontsize = 16;')
		f.write('activation = none;')
		f.write('autonumber = True;')
		f.write('default_note_color = lightblue;')
		print 'generate the events ....'
		ret = collect_events(fn, conf_id)
		print 'generate the events done!'
		for i in range(0, len(ret)):
			f.write ( ret[i])
		f.write('}')
		f.close()
		
		print 'generate the sequence diagram ...'
		cmd = 'seqdiag -f ./ciscoreg.ttf callflow-'+conf_id+'.diag'
		os.system(cmd)
		print 'generate the sequence diagram done!'


if len(sys.argv) < 3:
        print "Usage: python ", sys.argv[0], " log_file confid"
        quit()


generate_seqdiag(sys.argv[1], sys.argv[2])


