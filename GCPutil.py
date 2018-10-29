# Imports the Google Cloud client library
from google.cloud import translate
from google.cloud import texttospeech


class GTranslator:

    trans_client = None
    trans_en = None
    trans_ko = None

    def __init__(self):
        # Instantiates a client
        self.trans_client = translate.Client()

    def gcp_translate(self, text, source, target):
        self.trans_ko = self.trans_client.translate(text, source_language=source, target_language=target)
        print('Translate [' + target + '] :', text, '->', self.trans_ko['translatedText'])
        return self.trans_ko['translatedText']

    # def trans_to_eng(self, text):
    #     self.trans_en = self.trans_client.translate(text, source_language=Constant.language['French'],
    #                                                 target_language=Constant.language['English'])
    #     print('Translate [EN] :', text, '->', self.trans_en['translatedText'])
    #     return self.trans_en['translatedText']
    #
    # def trans_to_kor(self, text):
    #     self.trans_ko = self.trans_client.translate(text, source_language=Constant.language['French'],
    #                                                 target_language=Constant.language['Korean'])
    #     print('Translate [KO] :', text, '->', self.trans_ko['translatedText'])
    #     return self.trans_ko['translatedText']


class GTextToSpeech:

    client = None
    voice = None

    def __init__(self, language='fr'):
        # Instantiates a client
        self.client = texttospeech.TextToSpeechClient()
        self.voice = texttospeech.types.VoiceSelectionParams(
            language_code=language,
            ssml_gender=texttospeech.enums.SsmlVoiceGender.NEUTRAL)

    def tts_to_mp3(self, text, speed=1.0):
        synthesis_input = texttospeech.types.SynthesisInput(text=text)
        audio_config = texttospeech.types.AudioConfig(
            speaking_rate=speed,
            audio_encoding=texttospeech.enums.AudioEncoding.MP3)
        response = self.client.synthesize_speech(synthesis_input, self.voice, audio_config)

        out_file = text + '_' + str(int(speed*100)) + '.mp3'
        with open(out_file, 'wb') as out:
            out.write(response.audio_content)
            out.close()
            print('Audio content written to file :', out_file)

        return out_file


class Constant:
    language = {'English': 'en', 'French': 'fr', 'Korean': 'ko'}
