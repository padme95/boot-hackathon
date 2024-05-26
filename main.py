# import speech_recognition as sr
# import unidecode
# import bootTerms
#
# r = sr.Recognizer()
#
# with sr.Microphone() as s:
#     r.adjust_for_ambient_noise(s)
#
#     while True:
#         print("Estou ouvindo... Diga algo!")
#         audio = r.listen(s)
#
#         try:
#             # Reconhece a fala usando o Google Web Speech API
#             fala = r.recognize_google(audio, language='pt')
#             print('Você disse: ', fala)
#
#             # Obtendo o texto dos termos
#             textoTermos = bootTerms.textTerms
#
#             # Função para formatar o texto
#             def formatterText(texto):
#                 texto_sem_acentos = unidecode.unidecode(texto)
#                 texto_minusculo = texto_sem_acentos.lower()
#                 texto_formatado = texto_minusculo.replace('.', '').replace(',', '')
#                 return texto_formatado
#
#             # Formatando o texto dos termos
#             texto_formatado = formatterText(textoTermos)
#             print('Termos formatados: ', texto_formatado)
#
#         except sr.UnknownValueError:
#             print("Não consegui entender o que você disse.")
#         except sr.RequestError as e:
#             print(f"Erro na requisição ao serviço de reconhecimento de fala: {e}")
#         except Exception as e:
#             print(f"Ocorreu um erro: {e}")

import re
import unicodedata
import azure.cognitiveservices.speech as speechsdk
import bootTerms

# Configurações do serviço
subscription_key = "3f51a3f0d6334975a728fa4ac642e997"
region = "brazilsouth"

# Configuração do serviço de fala
speech_config = speechsdk.SpeechConfig(subscription=subscription_key, region=region)


# Função para criar um perfil de voz
def create_voice_profile():
    recognizer = speechsdk.SpeechRecognizer(speech_config)
    profile = recognizer.create_profile(speechsdk.VoiceProfileType.TextDependentVerification, "pt")
    print(f"Profile ID: {profile.profile_id}")
    return profile.profile_id


# Função para registrar amostras de voz para o perfil do usuário
def enroll_voice_samples(profile_id, audio_files):
    recognizer = speechsdk.SpeakerRecognizer(speech_config)
    profile = speechsdk.VoiceProfile(profile_id, speechsdk.VoiceProfileType.TextDependentVerification)

    for audio_file in audio_files:
        audio_config = speechsdk.AudioConfig(filename=audio_file)
        result = recognizer.enroll_profile(profile, audio_config)
        if result.reason == speechsdk.ResultReason.EnrolledVoiceProfile:
            print(f"Sample enrolled successfully: {audio_file}")
        else:
            print(f"Enrollment failed for sample {audio_file}: {result.reason}")


# Função para verificar a identidade do usuário
def verify_user_identity(profile_id, audio_file):
    recognizer = speechsdk.SpeakerRecognizer(speech_config)
    audio_config = speechsdk.AudioConfig(filename=audio_file)
    model = speechsdk.SpeakerVerificationModel(profile_id)
    result = recognizer.recognize_once(audio_config, model)

    if result.reason == speechsdk.ResultReason.RecognizedSpeaker:
        print("User identity verified.")
    else:
        print("User identity verification failed.")

# Função para gravar a voz do usuário lendo o texto do termo de consentimento
def record_voice_from_text():
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config)
    print("Por favor, leia o seguinte termo de consentimento em voz alta:")
    print(bootTerms.textTerms)
    print("Gravando... Aguarde até terminar de ler o texto.")
    result = speech_recognizer.recognize_once()
    if result.reason == speechsdk.ResultReason.RecognizedSpeech and result.text.strip():  # Verifica se o texto não está vazio
        # audio_filename = "voice_sample.wav"
        audio_output = speechsdk.AudioOutputConfig(filename=audio_filename)
        audio_config = speechsdk.AudioConfig(output_format=speechsdk.AudioOutputFormat.Wav16Khz16BitMono,
                                             audio_output=audio_output)
        speech_recognizer.start_continuous_recognition()
        print("Gravação concluída.")
        return audio_filename, result.text.strip()  # Retorna também o texto reconhecido
    else:
        print("Não foi possível reconhecer a fala ou o texto é vazio. Por favor, leia novamente.")
        return record_voice_from_text()  # Chama novamente a função para que o usuário leia o texto novamente


# Função para normalizar o texto
def normalize_text(text):
    # Remove letras maiúsculas, hífens e acentos
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s]', '', text)
    text = ''.join((c for c in unicodedata.normalize('NFD', text) if unicodedata.category(c) != 'Mn'))
    return text


# Criar perfil de voz para o usuário
user_profile_id = create_voice_profile()

# Gravar a voz do usuário lendo o texto do termo de consentimento
voice_sample_file, recognized_text = record_voice_from_text()

# Normalizar o texto reconhecido
normalized_recognized_text = normalize_text(recognized_text)

# Normalizar o texto do termo de consentimento
normalized_text_terms = normalize_text(bootTerms.textTerms)

# Comparar os textos normalizados
if normalized_recognized_text == normalized_text_terms:
    print("Texto reconhecido e texto do termo de consentimento são iguais.")
else:
    print("Texto reconhecido e texto do termo de consentimento são diferentes.")

# Registrar as amostras de voz
voice_samples = [voice_sample_file]
enroll_voice_samples(user_profile_id, voice_samples)

# Verificar a identidade do usuário
verify_user_identity(user_profile_id, voice_sample_file)