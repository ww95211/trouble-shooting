__author__ = 'weifshen'

# Install seqdiag
# easy_install seqdiag
# brew install zlib #install zlib if need

import sys
import os
import re
import pkgutil
import imp


class WbxCallflow:
	m_callflow_events = []
	m_confId = None
	m_locusId = None
	m_trackingId = None

	def __init__(self):
		print 'WbxCallflow::__init__'

	def get_id_from_map(self, fn, mapKey, value1, idx1_key, idx2_key,fmt) :
		if mapKey not in fmt:
			return None
		mapping = fmt[mapKey]
		if 'pattern' not in mapping:
			return None
		pattern = mapping['pattern']
		idx1 = 1
		idx2 = 2
		if idx1_key in mapping:
			idx1 = int(mapping[idx1_key])
		if idx2_key in mapping :
			idx2 = int(mapping[idx2_key])
		value2 = None
		regs = r'' + pattern
		f=open(fn)
		for line in f:
			m=re.match(regs,line)
			if (m is not None):
				if m.group(idx1) == value1:
					value2 = m.group(idx2)
					break
		f.close()
		if value2 is not None:
			print idx1_key+':'+value1 + ','+idx2_key +':' + value2 + ',from:'+fn
		else :
			print 'Not found'
		return value2

	def filter_one_log_file(self, fn ,fmt, events):
		if self.m_confId is None and self.m_trackingId is None:
			return
		if 'start-with-pattern' not in fmt :
			return
		fil = ''
		if self.m_confId is not None:
			fil = '('+self.m_confId
			if self.m_locusId is not None :
				fil = fil + '|' + self.m_locusId
			fil = fil + ')'
		else :
			fil = '('+self.m_trackingId+')'

		regs = r'^' + fmt['start-with-pattern'] + '.*$'
		f=open(fn)
		line_t = ''
		for line in f:
			m=re.match(regs,line)
			if (m is not None):
				r2=r'.*'+fil+'.*$'
				m2 = re.match(r2,line_t)
				if (m2 is not None):
					self.collect_events(line_t, fmt, events)
				line_t = line
			else :
				line_t = line_t + line.replace('\n','\\n').replace('\r','\\r').replace('   ','')
		f.close()

	def find_event(self, events, key) :
		for e in events:
			if key in events[e]:
				return events[e][key]
		return None

	def excape_reserve_keyword(self, str):
		return str.replace('[','\[').replace(']','\]').replace('(','\(').\
			replace(')','\)').replace('{','\{').replace('}','\}').replace('\\"','\"').replace('\"','\\"')


	def get_color_from_log_level(self, line, fmt) :
		if 'log-levels-pattern' not in fmt :
			return 'black'
		levels = {'info':'black','warning':'orange', 'error':'red', 'debug':'blue'}
		for level in fmt['log-levels-pattern'] :
			regs=r'^.*'+fmt['log-levels-pattern'][level]+'.*$'
			m=re.match(regs,line)
			if (m is not None):
				return levels[level]
		return 'black'

	def get_keyvalue(self, line, pattern,obj, key, fmt):
		if pattern in fmt :
			regs = '.*' + fmt[pattern] + '.*$'
			m = re.match(regs, line)
			if m is not None:
				return m.group(1)
		if key in obj :
			return obj[key]
		return None

	def is_unidirectional_only(self, fmt):
		if fmt is None or 'unidirectional-only' not in fmt:
			return False
		return fmt['unidirectional-only']

	def get_module_name(self,fmt):
		if fmt is None or 'module-name' not in fmt:
			return None
		return fmt['module-name']

	def collect_events(self, line, fmt, events) :
		if 'start-with-pattern' not in fmt :
			return
		cmd = ''
		first = True
		for e in events:
			for e1 in events[e]:
				if not first:
					cmd = cmd + '|' + e1
				else:
					cmd =  e1
					first = False
		cmd = self.excape_reserve_keyword(cmd)
		regs=r'^' + fmt['start-with-pattern']+'.*('+cmd+')(.*)$'
		m=re.match(regs,line)
		if (m is not None):
			obj = self.find_event(events,m.group(2))
			if obj is not None :
				source = self.get_keyvalue(line, 'source-pattern',obj, 'source', fmt)
				target = self.get_keyvalue(line, 'target-pattern',obj, 'target', fmt)
				if self.is_unidirectional_only(fmt) and self.get_module_name(fmt) != source :
					return
				msg = ''
				if 'separator-line' in obj:
					if obj['separator-line'] == 'before':
						msg = msg + '=== Separator line ===\n'
				msg = msg + source + ' -> ' + target + ' [label="' +  obj['label'] + '(' + m.group(1)
				for i in range(2, len(m.groups())) :
					if len(m.group(i + 1)) > 0:
						msg = msg + ',' + self.excape_reserve_keyword(m.group(i + 1))
				clr = 'color="'+ self.get_color_from_log_level(line, fmt)+'"'
				msg = msg + ')",'+clr+']'
				if 'farward' in obj or 'return' in obj:
					msg = msg + '{'
					if 'return' in obj and obj['return'] == True:
						msg = msg + target + ' -> ' + source + ' [label="RET:' +  obj['label'] + '(' + m.group(1) + ')",'+clr+'];'
					if 'farward' in obj:
						msg = msg + target + ' -> ' + obj['farward'] +' [label="FWD:' + obj['label'] + '(' + m.group(1) + ')",'+clr+'];'
					msg = msg + '}'
				msg = msg + ';\n'
				if 'separator-line' in obj:
					if obj['separator-line'] == 'after':
						msg = msg + '=== Separator line ===\n'
				self.m_callflow_events.append({m.group(1):msg})

	def generate_seqdiag(self) :
		if self.m_confId is None and self.m_trackingId is None:
			print 'Error: confId or trackingId cannot be None!'
			return
		print 'generate the events ....'
		CURDIR = os.path.dirname(os.path.realpath(__file__))
		for i in os.listdir(CURDIR):
			if os.path.isfile(os.path.join(CURDIR,i)):
				if i.rfind('.log') == len(i) - 4:
					print i
					for importer, modname, ispkg in pkgutil.iter_modules([CURDIR + '/events']):
						if ispkg:
							continue
						if modname.find('events') >= 0 :
							fpath = os.path.join(CURDIR + '/events', modname) + '.py'
							mod = imp.load_source(modname, fpath)
							print 'modname:'+modname+'.py'
							self.filter_one_log_file(i,mod._format_data,mod._events_data)
		fn_diag = ''
		if self.m_confId is not None:
			fn_diag = 'callflow_' + self.m_confId + '.diag'
		else :
			fn_diag = 'callflow_' + self.m_trackingId + '.diag'
		f_diag = open(fn_diag , 'w')
		f_diag.write('{\n')
		f_diag.write('edge_length = 300;\n')
		f_diag.write('span_height = 80;\n')
		f_diag.write('default_fontsize = 16;\n')
		f_diag.write('activation = none;\n')
		f_diag.write('autonumber = True;\n')
		f_diag.write('default_note_color = lightblue;\n')
		self.m_callflow_events.sort()
		for item in self.m_callflow_events:
			print item
			for k in item:
				f_diag.write(item[k])

		f_diag.write('}\n')
		f_diag.close()
		print 'generate the events done!'

		print 'generate the sequence diagram ...'
		cmd = 'seqdiag -f ./ciscoreg.ttf ' + fn_diag
		os.system(cmd)
		print 'generate the sequence diagram done!'

	def find_id(self, mapKey, v1, v1Idx,v2Idx):
		CURDIR = os.path.dirname(os.path.realpath(__file__))
		v2 = None
		for i in os.listdir(CURDIR) :
			if v2 is not None:
				break
			if os.path.isfile(os.path.join(CURDIR,i)):
				if i.rfind('.log') == len(i) - 4:
					print i
					for importer, modname, ispkg in pkgutil.iter_modules([CURDIR + '/events']):
						if ispkg:
							continue
						if modname.find('events') >= 0 :
							fpath = os.path.join(CURDIR + '/events', modname) + '.py'
							mod = imp.load_source(modname, fpath)
							v2 = self.get_id_from_map(i,mapKey,v1, v1Idx ,v2Idx,mod._format_data )
							if v2 is not None :
								break
		return v2

	def generate_seqdiag_for_all_via_trackingId(self,trackingId):
		self.m_trackingId = trackingId
		self.m_locusId = None
		self.m_confId = None
		self.generate_seqdiag()

	def generate_seqdiag_for_all_via_locusId(self,locusId):
		CURDIR = os.path.dirname(os.path.realpath(__file__))
		self.m_trackingId = None
		self.m_locusId = locusId
		self.m_confId = self.find_id('confId-locusId-map',locusId,'locusId-Idx' ,'confId-Idx')
		self.generate_seqdiag()

	def generate_seqdiag_for_all_via_confId(self,confId):
		CURDIR = os.path.dirname(os.path.realpath(__file__))
		self.m_trackingId = None
		self.m_confId = confId
		self.m_locusId = self.find_id('confId-locusId-map',confId,'confId-Idx','locusId-Idx')
		self.generate_seqdiag()


if len(sys.argv) < 3:
        print "Usage: python ", sys.argv[0], " -cid/-lid/tid confId/locudId/trackingId"
        print "copy all the logs into current folder"
        quit()

callflow = WbxCallflow()
if sys.argv[1] == '-cid' :
	callflow.generate_seqdiag_for_all_via_confId(sys.argv[2])
elif sys.argv[1] == '-lid' :
	callflow.generate_seqdiag_for_all_via_locusId(sys.argv[2])
elif sys.argv[1] == '-tid' :
	callflow.generate_seqdiag_for_all_via_trackingId(sys.argv[2])
else :
	print 'wrong parameters'


