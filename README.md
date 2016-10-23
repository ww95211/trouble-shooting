# tpgw-debug-tools

Install seqdiag
------------------
Install seqdiag with pip:

$ pip install seqdiag

Or with easy_install:

$ easy_install seqdiag

# Defines
------------------
```
1. Events python file name :  ‘component-name’ + ‘_events.py’ , # tpgw_events.py, put this file under events folder
2. Log format data object:
	_format_data = {
		‘multi-lines’ : false, # If this is true, we will use ‘start-with-pattern’ as separator 
		‘filter-base’: ‘trackingId|confId’, # trackingId or confId , using confId by default
		‘start-with-pattern’: ‘\[(\d+[/]\d+[/]\d+ \d+[:]\d+[:]\d+[.]\d+) ’, # or None for default pattern
		‘log-levels-pattern’: {
			‘info’ : ‘\[INFO\]’,
			‘warning’ : ‘\[WARN\]’,
			‘error’ : ‘\[ERROR\]’,
			‘debug’ : ‘\[DEBUG\]’
		},
		‘source-pattern’: ‘SOURCE:(.*),’, # or None if there is no such keywords
		‘target-pattern’:’TARGET:(.*),’, # or None if there is no such keywords
		‘confId-trackingId-map’: {‘pattern’:’confId:(.*),trackingId:(.*),’, ‘confId-Idx’:1, ‘trackingId-Idx’:2} 
	}

2. Events data object

	_events_data = {
		‘events-set-1’ : { # any name is allowed, system does not care.
			‘event-keyword1’ : { # the keyword in log files to match this event.
				‘source’ : ‘TPGW’, # source component, if there is source in log file, ignore this value.
				‘target’ : ‘CB’ , # target component, if there is source in log file, ignore this value.
				‘label’ : ‘create meeting’, # the label will be showed in the call flow 
				‘return’ : false, # return call flow line if it is true, by default , it is false
				’separator-line’ : ‘before’, # add a separator line before this call for ‘before’, or separator line after this call for ‘after’
			}
			‘event-keyword2’ : {}
		}
		‘events-set-2’ : {
			…
		}

	}
```
