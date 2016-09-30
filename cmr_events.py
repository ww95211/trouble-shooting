__author__ = 'weifshen'


_events = {
	'conference-events' : {
		'CreateMeeting,' : {'call':'TPGW -> CB','label':'creating conference'},
		'OnCreateJoinMeetingConfirm [PETA],uRoomId=' : {'call':'CB -> TPGW','label':'conf created'},
		'callbackURL=https' : {'call':'Hecate -> TPGW','label':'join conf'},
		'OnMeetingClosedIndication [PETA],uRoomId' : {'call':'CB -> TPGW','label':'conf closed'},
		'LeaveMeeting,m_iStatus=3' : {'call':'TPGW -> CB','label':'leave conference'},
		#'OnUserEjected [PETA],roomId=' : {'call':'CB -> TPGW','label':'eject user','ext-call':'TPGW -> Hecate'},
		'OnAddEndpointRequest,userid=' : {'call':'Hecate -> TPGW','label':'user join','ext-call':'TPGW -> CB'},
		'OnCreateJoinMeetingConfirm [PETA],err=' : {'call':'CB -> TPGW','label':'user joined'},
		'OnRemoveEndpointRequest [PETA],userId=' : {'call':'Hecate -> TPGW','label':'user leave'},
		'LeaveMeeting,m_iStatus=8' : {'call':'TPGW -> CB','label':'user leave'},
		#'OnSetMuteStatusRequest [PETA],userId=' : {'call':'Hecate -> TPGW','label':'mute user','ext-call':'TPGW -> CB'},
		'OnHostChangedIndication,uNewHostId=' : {'call':'CB -> TPGW','label':'Host changed'},
		'1:: OnPresenterChangedIndication' : {'call':'CB -> TPGW','label':'Presenter changed'},
	},
	'session-events' : {
		'OnSessionCreatedIndication:4,' : {'call':'CB -> TPGW','label':'session created'},
		'OnSessionClosedIndication,AS' : {'call':'CB -> TPGW','label':'session closed'},
	},
	'media-events' : {
		'HandleDataFromSpark, receive key frame' : {'call':'Linus -> TPGW','label':'key frame','ext-call':'TPGW -> WebEx-client'},
		'InputReceivedRtpDataFromWebEx,this is a key frame' : {'call':'WebEx-client -> TPGW','label':'key frame','ext-call':'TPGW -> Linus'},
		'OnMCUFullIntraRequest' : {'call':'Linus -> TPGW','label':'key frame request[SIP]'},
		'RequestIdrFrameFromAS' : {'call':'TPGW -> WebEx-client','label':'key frame request'},
		'OnPictureLossIndication' : {'call':'Linus -> TPGW','label':'key frame request[RTCP]'},
		'OnIDRRequest,uUsrId' : {'call':'WebEx-client -> TPGW','label':'key frame request'},
		'WBXFullIntraRequest ' : {'call':'TPGW -> Linus','label':'key frame request[SIP]'},
		'CMultiStreamRtpSession::RequestIDR' : {'call':'TPGW -> Linus','label':'key frame request[RTCP]'},
		'HandleSCR:' : {'call':'Linus -> TPGW','label':'SCR'},
		'OnSubScribe()' : {'call':'TPGW -> TPGW','label':'OnSubScribe'},
		'Announce(), availabe' : {'call':'TPGW -> TPGW','label':'Announce'},
		'SendSCA:' : {'call':'TPGW -> Linus','label':'SCA'},
	},
	'BFCP-events' : {
		'OnMCUPresenterGrabedNotify,floor status' : {'call':'Linus -> TPGW','label':'Grab floor'},
		'OnWBXGrabPresenterConfirm,result:' : {'call':'Linus -> TPGW','label':'Grab floor confirm'},
		'OnWBXPresenterRevokedNotify' : {'call':'Linus -> TPGW','label':'Floor revoked'},
		'OnWBXReleasePresenterConfirm' : {'call':'Linus -> TPGW','label':'Floor released confirm'},
		'OnBFCPConnected,floor status:' : {'call':'TPGW -> TPGW','label':'BFCP connected'},
		'GrabFloor,floor status' : {'call':'TPGW -> Linus','label':'Grab floor'},
		'ReleaseFloor,floor status:' : {'call':'TPGW -> Linus','label':'Release floor'},
	}
}
