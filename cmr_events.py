__author__ = 'weifshen'


_events = {
	"conf level events" : {
	    'CreateMeeting,' : {'call':'TPGW -> CB','label':'creating conference'},
	    'OnCreateJoinMeetingConfirm [PETA],uUsrId' : {'call':'CB -> TPGW','label':'conf created'},
	    'OnMeetingClosedIndication [PETA],uRoomId' : {'call':'CB -> TPGW','label':'conf closed'},
	    'LeaveMeeting,m_iStatus=3' : {'call':'TPGW -> CB','label':'leave conference'},
	},
	"session level events" : {
		'OnSessionCreatedIndication:4,' : {'call':'CB -> TPGW','label':'session created'},
		'OnSessionClosedIndication,AS' : {'call':'CB -> TPGW','label':'session closed'},
	},
	"key frame and request" : {
		'HandleDataFromSpark, receive key frame' : {'call':'Linus -> TPGW','label':'key frame'},
		'InputReceivedRtpDataFromWebEx,this is a key frame' : {'call':'WebEx-client -> TPGW','label':'key frame'},

		'OnMCUFullIntraRequest' : {'call':'Linus -> TPGW','label':'key frame request1'},
		'RequestIdrFrameFromAS' : {'call':'TPGW -> WebEx-client','label':'key frame request'},
		'OnPictureLossIndication' : {'call':'Linus -> TPGW','label':'key frame request2'},
		'OnIDRRequest,uUsrId' : {'call':'WebEx-client -> TPGW','label':'key frame request'},
		'CMultiStreamRtpSession::RequestIDR' : {'call':'TPGW -> Linus','label':'key frame request2'},
	},
	"SCR/SCA events" : {
		'HandleSCR:' : {'call':'Linus -> TPGW','label':'SCR'},
		'OnSubScribe()' : {'call':'TPGW -> TPGW','label':'OnSubScribe'},
		'Announce(), availabe' : {'call':'TPGW -> TPGW','label':'Announce'},
		'SendSCA:' : {'call':'TPGW -> Linus','label':'SCA'},
	}
}