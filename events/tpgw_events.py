__author__ = 'weifshen'

_format_data = {
	'start-with-pattern' : '\[(\d+[/]\d+[/]\d+ \d+[:]\d+[:]\d+[.]\d+) ',
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

_events_data = {
	'conference-events' : {
		'CreateMeeting,' : {'source':'TPGW','target':'CB','label':'creating conference'},
		'OnCreateJoinMeetingConfirm [PETA],uRoomId=' : {'source':'CB','target':'TPGW','label':'conf created'},
		'sourcebackURL=' : {'source':'Hecate','target':'TPGW','label':'join conf'},
		'OnMeetingClosedIndication [PETA],uRoomId' : {'source':'CB','target':'TPGW','label':'conf closed'},
		'LeaveMeeting,m_iStatus=3' : {'source':'TPGW','target':'CB','label':'leave conference'},
		#'OnUserEjected [PETA],roomId=' : {'source':'CB','target':'TPGW','label':'eject user','forward':'Hecate'},
		'OnAddEndpointRequest,userid=' : {'source':'Hecate','target':'TPGW','label':'endpoint join','forward':'CB'},
		'OnCreateJoinMeetingConfirm [PETA],err=' : {'source':'CB','target':'TPGW','label':'endpoint/dummy user joined'},
		'OnRemoveEndpointRequest [PETA],userId=' : {'source':'Hecate','target':'TPGW','label':'endpoint leave'},
		'LeaveMeeting,m_iStatus=8' : {'source':'TPGW','target':'CB','label':'endpoint leave'},
		#'OnSetMuteStatusRequest [PETA],userId=' : {'source':'Hecate','target':'TPGW','label':'mute user','forward':'CB'},
		'OnHostChangedIndication,uNewHostId=' : {'source':'CB','target':'TPGW','label':'Host changed'},
		'1:: OnPresenterChangedIndication' : {'source':'CB','target':'TPGW','label':'Presenter changed'},
		'NotifyWebexUserJoin, WEBEX_TRACKINGID=' : {'source':'CB','target':'TPGW','label':'WebEx user join','forward':'Hecate'},
		'NotifyWebexUserLeave, WEBEX_TRACKINGID=' : {'source':'CB','target':'TPGW','label':'WebEx user leave','forward':'Hecate'},
	},
	'session-events' : {
		'OnSessionCreatedIndication:4,' : {'source':'CB','target':'TPGW','label':'session created', 'separator-line':'before'},
		'OnSessionClosedIndication,AS' : {'source':'CB','target':'TPGW','label':'session closed', 'separator-line':'after'},
	},
	'media-events' : {
		'HandleDataFromSpark, receive key frame' : {'source':'Linus','target':'TPGW','label':'key frame','forward':'WebEx-client'},
		'InputReceivedRtpDataFromWebEx,this is a key frame' : {'source':'WebEx-client','target':'TPGW','label':'key frame','forward':'Linus'},
		'OnMCUFullIntraRequest' : {'source':'Linus','target':'TPGW','label':'key frame request[SIP]'},
		'RequestIdrFrameFromAS' : {'source':'TPGW','target':'WebEx-client','label':'key frame request'},
		'OnPictureLossIndication' : {'source':'Linus','target':'TPGW','label':'key frame request[RTCP]'},
		'OnIDRRequest,uUsrId' : {'source':'WebEx-client','target':'TPGW','label':'key frame request'},
		'WBXFullIntraRequest ' : {'source':'TPGW','target':'Linus','label':'key frame request[SIP]'},
		'CMultiStreamRtpSession::RequestIDR' : {'source':'TPGW','target':'Linus','label':'key frame request[RTCP]'},
		'HandleSCR:' : {'source':'Linus','target':'TPGW','label':'SCR'},
		'OnSubScribe()' : {'source':'TPGW','target':'TPGW','label':'OnSubScribe'},
		'Announce(), availabe' : {'source':'TPGW','target':'TPGW','label':'Announce'},
		'SendSCA:' : {'source':'TPGW','target':'Linus','label':'SCA'},
	},
	'BFCP-events' : {
		'OnMCUPresenterGrabedNotify,floor status' : {'source':'Linus','target':'TPGW','label':'Grab floor'},
		'OnWBXGrabPresenterConfirm,result:' : {'source':'Linus','target':'TPGW','label':'Grab floor confirm'},
		'OnWBXPresenterRevokedNotify' : {'source':'Linus','target':'TPGW','label':'Floor revoked'},
		'OnWBXReleasePresenterConfirm' : {'source':'Linus','target':'TPGW','label':'Floor released confirm'},
		'OnBFCPConnected,floor status:' : {'source':'TPGW','target':'TPGW','label':'BFCP connected'},
		'GrabFloor,floor status' : {'source':'TPGW','target':'Linus','label':'Grab floor'},
		'ReleaseFloor,floor status:' : {'source':'TPGW','target':'Linus','label':'Release floor'},
	},
	'CI-events' : {
		'validate req_id' : {'source':'TPGW', 'target':'CI', 'label' : 'validate token'},
		'getBearerToken req_id' : {'source':'TPGW', 'target':'CI', 'label' : 'get bear token'},
		'GetResponseTrackingId' : {'source':'CI', 'target':'TPGW', 'label' : 'CI response'},
	}
}
