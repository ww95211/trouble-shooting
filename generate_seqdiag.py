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

	def __init__(self):
		print 'WbxCallflow::__init__'

	def get_id_from_map(self, fn, value1, idx1_key, idx2_key,fmt) :
		if 'confId-locusId-map' not in fmt:
			return None
		mapping = fmt['confId-locusId-map']
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
		#else :
			#print 'Not found'
		return value2

	def filter_one_log_file(self, fn ,fmt, events):
		if self.m_confId is None:
			return
		if 'start-with-pattern' not in fmt :
			return
		fil = '('+self.m_confId
		if self.m_locusId is None:
			fil = fil + ')'
		else :
			fil = fil + '|' + self.m_locusId + ')'
		regs = r'^' + fmt['start-with-pattern'] + '.*$'
		f=open(fn)
		line_t = ''
		for line in f:
			m=re.match(regs,line)
			if (m is not None):
				r2=r'.*'+fil+'.*$'
				m2 = re.match(r2,line_t)
				if (m2 is not None):
					self.collect_events(line, fmt, events)
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
				msg = ''
				if 'separator-line' in obj:
					if obj['separator-line'] == 'before':
						msg = msg + '=== Separator line ===\n'
				source = self.get_keyvalue(line, 'source-pattern',obj, 'source', fmt)
				target = self.get_keyvalue(line, 'target-pattern',obj, 'target', fmt)

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
		if self.m_confId is None:
			print 'Error: confId cannot be None!'
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
		fn_diag = 'callflow_' + self.m_confId+'-'+self.m_locusId+ '.diag'
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


	def generate_seqdiag_for_all_via_locusId(self,locusId):
		CURDIR = os.path.dirname(os.path.realpath(__file__))
		self.m_locusId = locusId
		if self.m_confId is None :
			for i in os.listdir(CURDIR) :
				if self.m_confId is None:
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
								self.m_confId = self.get_id_from_map(i,locusId, 'locusId-Idx' ,'confId-Idx',mod._format_data )
								if self.m_confId is not None :
									break
		self.generate_seqdiag()

	def generate_seqdiag_for_all_via_confId(self,confId):
		CURDIR = os.path.dirname(os.path.realpath(__file__))
		self.m_confId = confId
		if self.m_locusId is None :
			for i in os.listdir(CURDIR):
				if self.m_locusId is not None:
					break
				if os.path.isfile(os.path.join(CURDIR,i)):
					if i.rfind('.log') == len(i) - 4:
						for importer, modname, ispkg in pkgutil.iter_modules([CURDIR + '/events']):
							if ispkg:
								continue
							if modname.find('events') >= 0 :
								fpath = os.path.join(CURDIR + '/events', modname) + '.py'
								mod = imp.load_source(modname, fpath)
								self.m_locusId = self.get_id_from_map(i,confId, 'confId-Idx' ,'locusId-Idx',mod._format_data )
								if self.m_locusId is not None :
									break
		self.generate_seqdiag()


if len(sys.argv) < 2:
        print "Usage: python ", sys.argv[0], " confid"
        print "copy all the logs into current folder"
        quit()

callflow = WbxCallflow()
callflow.generate_seqdiag_for_all_via_confId(sys.argv[1])


