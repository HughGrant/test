$(function() {
	setup_keywords_ui()
})

chrome.runtime.onMessage.addListener(function(request, sender, sendResponse) {

	if (request.action == 'set_keywords') {
		set_keywords(request.data)
	}

})