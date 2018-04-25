var me = {};
me.avatar = "https://lh6.googleusercontent.com/-lr2nyjhhjXw/AAAAAAAAAAI/AAAAAAAARmE/MdtfUmC0M4s/photo.jpg?sz=48";

var you = {};
you.avatar = "https://a11.t26.net/taringa/avatares/9/1/2/F/7/8/Demon_King1/48x48_5C5.jpg";
var botspeak = false;
var bingClientTTS = new BingSpeech.TTSClient("018cfaf12bd9423cb2f3c7751ef0f436", BingSpeech.SupportedLocales.enUS_Female);
var bingClientSR = new BingSpeech.RecognitionClient("018cfaf12bd9423cb2f3c7751ef0f436");
var recordstate = false;

function formatAMPM(date) {
    var hours = date.getHours();
    var minutes = date.getMinutes();
    var ampm = hours >= 12 ? 'PM' : 'AM';
    hours = hours % 12;
    hours = hours ? hours : 12; // the hour '0' should be '12'
    minutes = minutes < 10 ? '0'+minutes : minutes;
    var strTime = hours + ':' + minutes + ' ' + ampm;
    return strTime;
}            

//-- No use time. It is a javaScript effect.
function insertChat(who, text, time){
    if (time === undefined){
        time = 0;
    }
    var control = "";
    var date = formatAMPM(new Date());
    
    if (who == "me"){
        control = '<li style="width:100%">' +
                        '<div class="msj macro">' +
                            '<div class="text text-l">' +
                                '<p>'+ text +'</p>' +
                                '<p><small>'+date+'</small></p>' +
                            '</div>' +
                        '</div>' +
                    '</li>';                    
    }else{
        control = '<li style="width:100%;">' +
                        '<div class="msj-rta macro">' +
                            '<div class="text text-r">' +
                                '<p>'+text+'</p>' +
                                '<p><small>'+date+'</small></p>' +
                            '</div>'  +                                
                  '</li>';
    }
    setTimeout(
        function(){                        
            $("#msglog").append(control).scrollTop($("#msglog").prop('scrollHeight'));
        }, time);
    
}

function resetChat(){
    $("ul").empty();
}

function setluismsg(text) {
    var params = {
            // These are optional request parameters. They are set to their default values.
            "q" : text,
            "timezoneOffset": "0",
            "verbose": "false",
            "spellCheck": "false",
            "staging": "false",
        };
        $.ajax({
            url: "https://westus.api.cognitive.microsoft.com/luis/v2.0/apps/f595017d-1f62-4b0e-bf07-c8af20b56239?" + $.param(params),
            beforeSend: function(xhrObj){
                // Request headers
                xhrObj.setRequestHeader("Ocp-Apim-Subscription-Key","7ff0db3a38c64081ab77c753bfb00ef3");
            },
            type: "GET",
            // The request body may be empty for a GET request
            data: "",
        })
        .done(function(data) {
            // Display a popup containing the top intent
            if(data.topScoringIntent.intent === "Hello") {
            	insertChat("me",$("meta[name='defaultmsg']").attr("content"));
            	if(botspeak) {
            		bingClientTTS.synthesize("Hi! Have anything to ask about the document? I can brief you about the document, list the dated events, and point the important words in it.");
            	}
            }
            if(data.topScoringIntent.intent === "Type") {
                insertChat("me","The case is of type : " + $("meta[name='category']").attr("content"));
                if(botspeak) {
                    bingClientTTS.synthesize("The case is of type " + $("meta[name='category']").attr("content"));
                }
            }
            if(data.topScoringIntent.intent === "Persons") {
                insertChat("me","The individuals involved are : " + $("meta[name='persons']").attr("content"));
                if(botspeak) {
                    bingClientTTS.synthesize("The individuals involved are : " + $("meta[name='persons']").attr("content"));
                }
            }
            if(data.topScoringIntent.intent === "Orgs") {
                insertChat("me","The organisations involved are : " + $("meta[name='orgs']").attr("content"));
                if(botspeak) {
                    bingClientTTS.synthesize("The organisations involved are : " + $("meta[name='orgs']").attr("content"));
                }
            }
            if(data.topScoringIntent.intent === "Locs") {
                insertChat("me","The locations involved are : " + $("meta[name='locs']").attr("content"));
                if(botspeak) {
                    bingClientTTS.synthesize("The locations involved are : " + $("meta[name='locs']").attr("content"));
                }
            }
            if(data.topScoringIntent.intent === "Date") {
                insertChat("me","Here are the dated events<br>" + $("meta[name='chatdates']").attr("content"));
                if(botspeak) {
                    bingClientTTS.synthesize("Here are the dated events");
                    var rawtext = $("meta[name='rawchatdates']").attr("content");
                    var lines = rawtext.split('.');
                    for(var i = 0;i < lines.length;i++) {
                        if(lines[i].length < 1000) {
                            bingClientTTS.synthesize(lines[i]);
                        }
                        else {
                            var lines2 = lines[i].split(',');
                            for(var j = 0;j < lines2.length;j++) {
                                bingClientTTS.synthesize(lines2[j]);
                            }
                        }
                    }
                }
            }
            if(data.topScoringIntent.intent === "Shortsummary") {
                insertChat("me","Here's a quick rundown<br>" + $("meta[name='chatshortsummary']").attr("content"));
                if(botspeak) {
                    bingClientTTS.synthesize("Here's a quick rundown");
                    var rawtext = $("meta[name='rawchatshortsummary']").attr("content");
                    var lines = rawtext.split('.');
                    for(var i = 0;i < lines.length;i++) {
                        if(lines[i].length < 1000) {
                            bingClientTTS.synthesize(lines[i]);
                        }
                        else {
                            var lines2 = lines[i].split(',');
                            for(var j = 0;j < lines2.length;j++) {
                                bingClientTTS.synthesize(lines2[j]);
                            }
                        }
                    }
                }
            }
            if(data.topScoringIntent.intent === "Keypoints") {
                insertChat("me","Watch out for these points when reading the whole thing<br>" + $("meta[name='chatkeywords']").attr("content"));
                if(botspeak) {
                    bingClientTTS.synthesize("Watch out for these key points when reading the whole thing");
                    var rawtext = $("meta[name='rawchatkeywords']").attr("content");
                    var lines = rawtext.split(',');
                    for(var i = 0;i < lines.length;i++) {
                        //
                        var temp = lines[i].split(' ');
                        if(temp.length > 2) {
                            bingClientTTS.synthesize(lines[i]);
                        }
                    }
                }

            }
            if(data.topScoringIntent.intent === "None") {
                insertChat("me","Sorry I didn't understand, please ask again");
                if(botspeak) {
                    bingClientTTS.synthesize("Sorry, I didn't understand, please ask again");
                }
            }
        })
        .fail(function() {
            insertChat("me","Sorry I didn't understand, please ask again");
            bingClientTTS.synthesize("Sorry, I didn't understand, please ask again");
        });
}

$(".mytext").on("keydown", function(e){
    if (e.which == 13){
        var text = $(this).val();
        if (text !== ""){
            insertChat("you", text); 
            //if(text === "send") {
            //	insertChat("you","metadata<br>" + $("meta[name='fulltext']").attr("content"));
            //}
            setluismsg(text);
            $(this).val('');
        }
    }
});

$('#sendbutton').click(function(){
    $(".mytext").trigger({type: 'keydown', which: 13, keyCode: 13});
});

$('#enablevoice').click(function() {
    var buttontext = $('#enablevoice').text();
    if(buttontext === "Enable Voice") {
        botspeak = true;
        $('#enablevoice').text('Disable Voice');
    }
    else {
        botspeak = false;
        $('#enablevoice').text('Enable Voice');
    }
});
//-- Clear Chat
resetChat();
insertChat("me",$("meta[name='defaultmsg']").attr("content"));
//-- Print Messages
bingClientSR.onFinalResponseReceived = function(response) {
    insertChat("you",response);
    setluismsg(response);
}

bingClientSR.onError = function(code,requestID) {
    insertChat("me","Sorry, there seems to be an error. Please try again or try using text");
    if(botspeak) {
        bingClientTTS.synthesize("Sorry, there seems to be an error. Please try again or try using text");
    }
}
$('#startrecord').click(function() {
    bingClientSR.startMicAndContinuousRecognition();
});
$('#endrecord').click(function() {
    bingClientSR.endMicAndContinuousRecognition();
});

$('#recordbutton').click(function() {
    if(recordstate) {
        $('#recordbutton').css("color","black");
        bingClientSR.endMicAndContinuousRecognition();
        recordstate = false;
    }
    else {
        $('#recordbutton').css("color","red");
        bingClientSR.startMicAndContinuousRecognition();
        recordstate = true;
    }
});

//insertChat("me","Persons : " + $("meta[name='persons']").attr("content"));
//insertChat("me","Organisations : " + $("meta[name='orgs']").attr("content"));
//insertChat("me","Locations : " + $("meta[name='locs']").attr("content"));

