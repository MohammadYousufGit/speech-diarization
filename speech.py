import torchaudio
from speechbrain.pretrained import EncoderDecoderASR, VAD, EncoderClassifier
from speechbrain.pretrained.interfaces import foreign_class
import pyaudioconvert as pac

class Speech:
    
    def transcribe(audio): 
        asr_model = EncoderDecoderASR.from_hparams(
        source="speechbrain/asr-transformer-transformerlm-librispeech",
        savedir="pretrained_models/asr-transformer-transformerlm-librispeech",
        # run_opts={"device": "cuda"}
        )
        return asr_model.transcribe_file(audio)

    
    def segments(audio):
        pac.convert_wav_to_16bit_mono('Process/' + audio, 'Converted/' + audio)
        vd = VAD.from_hparams(source="speechbrain/vad-crdnn-libriparty", savedir="pretrained_models/vad-crdnn-libriparty")
        prob_chunks = vd.get_speech_prob_file('Converted/' + audio)
        prob_th = vd.apply_threshold(prob_chunks, activation_th=0.5, deactivation_th=0.25).float()
        boundaries = vd.get_boundaries(prob_th)
        boundaries = vd.energy_VAD('Converted/' + audio,boundaries)
        boundaries = vd.merge_close_segments(boundaries, close_th=0.250)
        boundaries = vd.remove_short_segments(boundaries, len_th=0.250)
        vd.save_boundaries(boundaries, save_path='test.txt',print_boundaries=False)
        with open('test.txt') as f:
                contents = f.read()
        return contents

    def emotion(audio):
            from speechbrain.pretrained.interfaces import foreign_class
            classifier = foreign_class(source="speechbrain/emotion-recognition-wav2vec2-IEMOCAP", pymodule_file="custom_interface.py", classname="CustomEncoderWav2vec2Classifier")
            out_prob, score, index, text_lab = classifier.classify_file(audio)
            return text_lab

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

    def speakerId(audio):
            classifier = EncoderClassifier.from_hparams(source="speechbrain/spkrec-xvect-voxceleb")
            signal, fs =torchaudio.load(audio)
            classifier.encode_batch(signal)
            output_probs, score, index, text_lab = classifier.classify_batch(signal)
            return text_lab

    
