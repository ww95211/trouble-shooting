# tpgw-debug-tools

Install seqdiag
------------------
Install seqdiag with pip:

$ pip install seqdiag

Or with easy_install:

$ easy_install seqdiag

# How to use
------------------
Copy all the logs into current folder and then running below command:
```
python generate_seqdiag.py -cid/-lid/-tid confId/locudId/trackingId
```

# Defines
------------------
```
1. Events python file name :  'component-name' + '_events.py' , # tpgw_events.py, put this file under events folder
2. Log format data object:
	_format_data = {
		'start-with-pattern': '\[(\d+[/]\d+[/]\d+ \d+[:]\d+[:]\d+[.]\d+) ',
        	'log-levels-pattern': {
                	'info'    : ' Info:',
                	'warning' : ' Warning:',
                	'error'   : ' Error:',
                	'debug'   : ' Detail:',
		},
		'source-pattern': 'source:([^,]*)',
		'target-pattern': 'target:([^,]*)',
		'confId-locusId-map': {'pattern':'.*meeting_id=(.*)_.*locus\/api\/v1\/loci\/(.*).*$', 'confId-Idx':1, 'locusId-Idx':2}
	}

2. Events data object

	_events_data = {
		'events-set-1' : { # any name is allowed, system does not care.
			'event-keyword1' : { # the keyword in log files to match this event.
				'source' : 'TPGW', # source component, if there is source in log file, ignore this value.
				'target' : 'CB' , # target component, if there is source in log file, ignore this value.
				'forward': 'WBX-Client', #
				'label'  : 'create meeting', # the label will be showed in the call flow 
				'return' : false, # return to source if it is true, by default , it is false
				'separator-line' : 'before', # add a separator line before this event for ‘before’, or separator line after this event for ‘after’
			}
			'event-keyword2' : {}
		}
		'events-set-2' : {
			…
		}

	}
```
