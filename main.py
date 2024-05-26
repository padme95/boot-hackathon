import speech_recognition as sr
import unidecode
import bootTerms

r = sr.Recognizer()

with sr.Microphone() as s:
    r.adjust_for_ambient_noise(s)

    while True:
        print("ouvindo...! Por favor, leia os termos em voz alta")
        audio = r.listen(s)

        try:
            # Reconhece a fala usando o Google Web Speech API
            fala = r.recognize_google(audio, language='pt')

            # Obtendo o texto dos termos
            textoTermos = bootTerms.textTerms

            #Função para formatar o texto
            def formatterText(texto):
                texto_sem_acentos = unidecode.unidecode(texto)
                texto_minusculo = texto_sem_acentos.lower()
                texto_form = texto_minusculo.replace('.', '').replace(',', '').replace('-', '').replace(':', '')
                return texto_form

            # Formatando o texto dos termos
            termos_formatado = formatterText(textoTermos)
            fala_formatada = formatterText(fala)

            print('Você disse: ', fala_formatada)
            print('Termos formatados do doc: ', termos_formatado)

            if fala_formatada and termos_formatado and fala_formatada == termos_formatado and len(
                fala_formatada) == len(termos_formatado):
                print("--- Bem vindo novamente, por favor, respeite as regras do regulamento na próxima partida.")
            else:
                print(
                    "Não foi possível reconhecer a fala, por favor, leia atentamente o regulamento e tente novamente.")

        except sr.UnknownValueError:
            print("Não consegui entender o que você disse.")
        except sr.RequestError as e:
            print(f"Erro na requisição ao serviço de reconhecimento de fala: {e}")
        except Exception as e:
            print(f"Ocorreu um erro: {e}")
# import re
# import unicodedata
# import azure.cognitiveservices.speech as speechsdk
# import bootTerms
#
# # Configurações do serviço
# speech_key, service_region = "3f51a3f0d6334975a728fa4ac642e997", "brazilsouth"
# speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
#
# # Configuração do serviço de fala
# speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config)
#
# print("Say something...")
# # result = speech_recognizer.recognize_once()
# # print(f'{result.text}')
#
#
# # Cria um cliente de perfil de voz
# def create_voice_profile():
#     voice_profile_client = speechsdk.VoiceProfileClient(speech_config)
#     return voice_profile_client
#
# # Função para registrar amostras de voz para o perfil do usuário
# def enroll_voice_samples(profile, audio_files):
#     for audio_file in audio_files:
#         enrollment_response = profile.enrollments.add(speechsdk.AudioData(path=audio_file))
#         if enrollment_response.reason == speechsdk.ResultReason.EnrolledVoiceProfile:
#             print(f"Sample enrolled successfully: {audio_file}")
#         else:
#             print(f"Enrollment failed for sample {audio_file}: {enrollment_response.reason}")
#
#
# # Função para verificar a identidade do usuário
# def verify_user_identity(profile, audio_file):
#     result = profile.recognize(speechsdk.AudioData(path=audio_file))
#     if result.reason == speechsdk.ResultReason.EnrolledVoiceProfile:
#         print("User identity verified.")
#     else:
#         print("User identity verification failed.")
#
#
# # Função para gravar a voz do usuário lendo o texto do termo de consentimento
# def record_voice_from_text():
#     speech_recognizer = speechsdk.SpeechRecognizer(speech_config)
#     print("Por favor, leia o seguinte termo de consentimento em voz alta:")
#     print(bootTerms.textTerms)
#     print("Gravando... Aguarde até terminar de ler o texto.")
#     result = speech_recognizer.recognize_once()
#     if result.reason == speechsdk.ResultReason.RecognizedSpeech and result.text.strip():  # Verifica se o texto não está vazio
#         audio_filename = "voice_sample.wav"
#         audio_output = speechsdk.AudioOutputConfig(filename=audio_filename)
#         audio_config = speechsdk.AudioConfig(output_format=speechsdk.AudioOutputFormat.Wav16Khz16BitMono,
#                                              audio_output=audio_output)
#         speech_recognizer.start_continuous_recognition()
#         print("Gravação concluída.")
#         return audio_filename, result.text.strip()  # Retorna também o texto reconhecido
#     else:
#         print("Não foi possível reconhecer a fala ou o texto é vazio. Por favor, leia novamente.")
#         return record_voice_from_text()  # Chama novamente a função para que o usuário leia o texto novamente
#
#
# # Função para normalizar o texto
# def normalize_text(text):
#     # Remove letras maiúsculas, hífens e acentos
#     text = text.lower()
#     text = re.sub(r'[^a-z0-9\s]', '', text)
#     text = ''.join((c for c in unicodedata.normalize('NFD', text) if unicodedata.category(c) != 'Mn'))
#     return text
#
#
# # Criar perfil de voz para o usuário
# user_profile = create_voice_profile()
#
# # Gravar a voz do usuário lendo o texto do termo de consentimento
# voice_sample_file, recognized_text = record_voice_from_text()
#
# # Normalizar o texto reconhecido
# normalized_recognized_text = normalize_text(recognized_text)
#
# # Normalizar o texto do termo de consentimento
# normalized_text_terms = normalize_text(bootTerms.textTerms)
#
# # Comparar os textos normalizados
# if normalized_recognized_text == normalized_text_terms:
#     print("Texto reconhecido e texto do termo de consentimento são iguais.")
# else:
#     print("Texto reconhecido e texto do termo de consentimento são diferentes.")
#
# # Registrar as amostras de voz
# voice_samples = [voice_sample_file]
# enroll_voice_samples(user_profile, voice_samples)
#
# # Verificar a identidade do usuário
# verify_user_identity(user_profile, voice_sample_file)




# ------->>>>
# import azure.cognitiveservices.speech as speechsdk
# import bootTerms
# import re
# import unicodedata
#
# # Substitua pelos valores reais obtidos na sua conta do Azure
# speech_key = "3f51a3f0d6334975a728fa4ac642e997"
# service_region = "brazilsouth"
#
# # Configuração do serviço
# speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
#
# # Cria um cliente de perfil de voz
# def create_voice_profile():
#     voice_profile_client = speechsdk.VoiceProfileClient(speech_config)
#     return voice_profile_client
#
# # Função para registrar amostras de voz para o perfil do usuário
# def enroll_voice_samples(profile, audio_files):
#     for audio_file in audio_files:
#         enrollment_response = profile.enrollments.add(speechsdk.AudioData(filename=audio_file))
#         if enrollment_response.reason == speechsdk.ResultReason.EnrolledVoiceProfile:
#             print(f"Amostra registrada com sucesso: {audio_file}")
#         else:
#             print(f"Falha no registro da amostra {audio_file}: {enrollment_response.reason}")
#
# # Função para verificar a identidade do usuário
# def verify_user_identity(profile, audio_file):
#     result = profile.recognize_once(speechsdk.AudioData(filename=audio_file))
#     if result.reason == speechsdk.ResultReason.EnrolledVoiceProfile:
#         print("Identidade do usuário verificada.")
#     else:
#         print("Falha na verificação da identidade do usuário.")
#
# # Função para gravar a voz do usuário lendo o texto do termo de consentimento
# def record_voice_from_text():
#     speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config)
#     print("Por favor, leia o seguinte termo de consentimento em voz alta:")
#     print(bootTerms.textTerms)
#     print("Gravando... Aguarde até terminar de ler o texto.")
#     result = speech_recognizer.recognize_once()
#     if result.reason == speechsdk.ResultReason.RecognizedSpeech and result.text.strip():  # Verifica se o texto não está vazio
#         audio_filename = "voice_sample.wav"
#         audio_config = speechsdk.audio.AudioOutputConfig(filename=audio_filename)
#         speech_recognizer.start_continuous_recognition()
#         print("Gravação concluída.")
#         return audio_filename, result.text.strip()  # Retorna também o texto reconhecido
#     else:
#         print("Não foi possível reconhecer a fala ou o texto é vazio. Por favor, leia novamente.")
#         return record_voice_from_text()  # Chama novamente a função para que o usuário leia o texto novamente
#
# # Função para normalizar o texto
# def normalize_text(text):
#     # Remove letras maiúsculas, hífens e acentos
#     text = text.lower()
#     text = re.sub(r'[^a-z0-9\s]', '', text)
#     text = ''.join((c for c in unicodedata.normalize('NFD', text) if unicodedata.category(c) != 'Mn'))
#     return text
#
# # Criar perfil de voz para o usuário
# user_profile = create_voice_profile()
#
# # Gravar a voz do usuário lendo o texto do termo de consentimento
# voice_sample_file, recognized_text = record_voice_from_text()
#
# # Normalizar o texto reconhecido
# normalized_recognized_text = normalize_text(recognized_text)
#
# # Normalizar o texto do termo de consentimento
# normalized_text_terms = normalize_text(bootTerms.textTerms)
#
# # Comparar os textos normalizados
# if normalized_recognized_text == normalized_text_terms:
#     print("Texto reconhecido e texto do termo de consentimento são iguais.")
# else:
#     print("Texto reconhecido e texto do termo de consentimento são diferentes.")
#
# # Registrar as amostras de voz
# voice_samples = [voice_sample_file]
# enroll_voice_samples(user_profile, voice_samples)
#
# # Verificar a identidade do usuário
# verify_user_identity(user_profile, voice_sample_file)
