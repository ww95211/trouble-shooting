__author__ = 'weifshen'

_format_data = {
	#'sources-filter' : ['TPGW','CB','Hecate','Linus','WebEx-client'],
	'sources-filter' : ['MCS','MCC','Tahoe','Linus','VUser','AUser','nonWUser','WUser'],
	'start-with-pattern' : '\[(\d+[/]\d+[/]\d+ \d+[:]\d+[:]\d+[.]\d+) ',
	'log-levels-pattern': {
		'info'    : ' Info:',
		'warning' : ' Warning:',
		'error'   : ' Error:',
		'debug'   : ' Detail:',
	},
	'source-pattern': 'source:([^,]*)',
	'target-pattern': 'target:([^,]*)',
	'confId-locusId-map': {'pattern':'.*meeting_id=(.*)_.*locus\/api\/v(1|2|3)\/loci\/(.*).*$', 'confId-Idx':1, 'locusId-Idx':3},
}

_events_data = {
	'conference-events' : {
		'CMediaServer::OnSessionStartRequest,':{'source':'MCC','target':'MCS','label':'creating conference request'},
		'CMediaServer::OnStartConf,':{'source':'MCS','target':'MCC','label':'creating conference respone'},
		'CMediaConference::NewVideoSession':{'source':'MCS','target':'MCC','label':'creating video session'},
		'CMediaConference::NewVoIPSession':{'source':'MCS','target':'MCC','label':'creating audio session'},
		'CMediaConference::RemoveSession':{'source':'MCS','target':'MCC','label':'remove session'},
		'CMediaServer::OnStopConf,':{'source':'MCS','target':'MCC','label':'close conference'}
	},
	'session-events' : {
		'MmServerVideoSession::OnVideoSessionOpen,' : {'source':'MCS','target':'MCC','label':'session created', 'separator-line':'before'},
		'MmServerVideoSession::CallTahoe' : {'source':'MCS','target':'Tahoe','label':'Sip Call'},
		'MmServerVideoSession::StopSession' : {'source':'MCS','target':'VUser','label':'session close'},
		'CMmAudioSession::StopSession' : {'source':'AUser','target':'MCS','label':'session close'},
		'MMPRtpSession::Start,' : {'source':'MCS','target':'Linus','label':'create RTP session'},
		#'CVideoSipConnection::StartMmRtpSession' : {'source':'MCS','target':'Linus','label':'Video RTP session'},
		'MMPRtpSession::on_data_indication' : {'source':'Linus','target':'MCS','label':'reveice first data pkg'},
		'MMPRtpSession::Destroy' : {'source':'Linus','target':'MCS','label':'destory RTP session'},
		'MmServerVideoSession::OnVideoSessionClose' : {'source':'MCS','target':'MCC','label':'session closed', 'separator-line':'after'}
	},
	'user-events':{
		'MmServerVideoSession::UserJoinSession;' : {'source':'VUser','target':'MCS','label':'user join'},
		'CMmAsnMgr::OnUserLeave,' : {'source':'VUser','target':'MCS','label':'user leave session'},
		'CMmAudioSession::UserJoinSession;' : {'source':'AUser','target':'MCS','label':'session created'},
		'CMmAudioSession::CallAppServer,' : {'source':'MCS','target':'Tahoe','label':'Sip Call'},
		'CMmAudioSession::NotifyCallAppSvrResult,' : {'source':'Tahoe','target':'MCS','label':'Sip Call Suss'},	
		'MmServerVideoSession::CreateTandberg' : {'source':'linus','target':'MCS','label':'frist tp video user join'},
		'CMmVideoSession4Spark::OnDummyTPUserJoin' : {'source':'MCS','target':'linus','label':'ccp video user join'},
		'CMmSessionServerDummyTpEndPointManager::BroadcastStatus' : {'source':'MCS','target':'VUser','label':'ccp video user join'},
		'CMmSessionServerSessionEx::OnDummyTPLeave_u,' : {'source':'MCS','target':'linus','label':'ccp video user join'},
		'CMmSession4SparkImpl::OnUserLeave' : {'source':'MCS','target':'VUser','label':'ccp video user join'}
	},
	'exception-events':{
		'CMediaServer::OnUserJoinSession':{'source':'MCS','target':'VUser','label':'user join'}	
	}
	
	
}
