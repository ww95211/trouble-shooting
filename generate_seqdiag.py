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

	regs=r'^\[(\d+[/]\d+[/]\d+ \d+[:]\d+[:]\d+[.]\d+).*('+cmd+').*$'
	print regs
	f=open(fn)
	for line in f:
		m=re.match(regs,line)
		if (m is not None):
			obj = find_event(cmr_events._events,m.group(2))
			msg = obj['call'] + ' [label="' +  obj['label'] + '(' + m.group(1)
			for i in range(2, len(m.groups())) :
				msg = msg + ',' + m.group(i + 1)
			msg = msg + ')"];'
			ret.append(msg)
	f.close()
	return ret


def generate_seqdiag(fontfile, fn , conf_id) :

	f = open ( 'output.diag', 'w' )
	if f is not None :
		f.write('{')
		f.write('edge_length = 300;')
		f.write('span_height = 80;')
		f.write('default_fontsize = 16;')
		f.write('activation = none;')
		f.write('autonumber = True;')
		f.write('default_note_color = lightblue;')
		ret = collect_events(fn, conf_id)
		for i in range(0, len(ret)):
			f.write ( ret[i])
		f.write('}')
		f.close()

		cmd = 'seqdiag -f '+fontfile+' output.diag'
		os.system(cmd)


generate_seqdiag('/Users/weifshen/andrew/ciscoreg.ttf','/Users/weifshen/andrew/wbxtpgw-1_info_09272016_3.14503.log', '2526716586')


