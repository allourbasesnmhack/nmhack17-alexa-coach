def prepare(message,speed="medium"):
    message="<speak><prosody rate='"+speed+"'>"+message+"</prosody></speak>"
    return message
