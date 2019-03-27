var tonearr = [];
for (var i = 0; i < 3; i++){
    var r = "";
    var g = "";
    var b = "";
    switch(msg.payload[i].tone_id){
        case "anger":
            rgb = (255,000,000);
            break;
        case "disgust":
            rgb = (000,255,000);
            break;
        case "sadness":
            rgb = (000,000,255);
            break;
        case "fear":
            rgb = (255,000,255);
            break;
        case "joy":
            rgb = (255,255,000);
            break;
    }
    var toneObj = {
        "intensity": msg.payload[i].score,
        "tone_id": msg.payload[i].tone_id,
        "rgb": rgb
    };
    tonearr[i] = toneObj;
}

// Create MQTT message in JSON
msg = {
  payload: JSON.stringify(
    {
      d:{
        "tone1": tonearr[0],
        "tone2": tonearr[1],
        "tone3": tonearr[2],
      }
    }
  )
};
return msg;