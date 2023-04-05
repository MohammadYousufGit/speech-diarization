from s3 import S3
from db import Db
from speech import Speech
from datetime import timedelta
import time
from pydub import AudioSegment
import logging

def main(): 
    logging.basicConfig(filename="log.txt", level=logging.DEBUG)    
    logging.debug("Debug logging test...")
    aws = S3
    db = Db
    file_names = db.get_files()
    finalResult = []
    for name in file_names:
       d = aws.download_file(name[0])
       if d:
           diarization = Speech
           audio = name[0]
           speech = diarization.segments(audio)
           converted_segments = strToArray(speech)
           result = []
           for value in converted_segments:
                chunks = value.split()
                if(chunks[3] == 'SPEECH'):
                    timestamp = round(time.time() * 1000)
                    file_name = str(timestamp) + '.wav'
                    from_ms = float(chunks[1]) * 1000 
                    to_ms = float(chunks[2]) * 1000 
                    newAudio = AudioSegment.from_wav('Converted/' + audio)
                    newAudio = newAudio[from_ms:to_ms]
                    newAudio.export('chunks/' + file_name, format="wav")
                    text = diarization.transcribe('chunks/' + file_name)
                    mood = diarization.emotion('chunks/' + file_name)
                    speaker = diarization.speakerId('chunks/' + file_name)
                    data = {
                            "text" : text,
                            "emotions" : mood,
                            "speaker" : speaker,
                            "time" : chunks[1] + ':' + chunks[2],
                            
                    }
                    result.append(data)
        #    finalResult.append(result)
           sql = db.update(name[0], result)
           print('sql')
           print(sql)
#     query(name,result)
    print(finalResult)
#     result = []


def strToArray(str):
        out = []
        buff = []
        for c in str:
                if c == '\n':
                        out.append(''.join(buff))
                        buff = []
                else:
                        buff.append(c)
        else:
                if buff:
                        out.append(''.join(buff))

        return out

def query(file_name,data):
        db = Db 
        query  = db.update(file_name,data)
        if query > 1:
                return True
        else:
                return False

if __name__ == "__main__":
    main()      
