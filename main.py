import speech_recognition as sr
import unidecode
import bootTerms

r = sr.Recognizer()

with sr.Microphone() as s:
    r.adjust_for_ambient_noise(s)

    while True:
        print("Estou ouvindo... Diga algo!")
        audio = r.listen(s)

        try:
            # Reconhece a fala usando o Google Web Speech API
            fala = r.recognize_google(audio, language='pt')
            print('Você disse: ', fala)

            # Obtendo o texto dos termos
            textoTermos = bootTerms.textTerms

            # Função para formatar o texto
            def formatterText(texto):
                texto_sem_acentos = unidecode.unidecode(texto)
                texto_minusculo = texto_sem_acentos.lower()
                texto_formatado = texto_minusculo.replace('.', '').replace(',', '')
                return texto_formatado

            # Formatando o texto dos termos
            texto_formatado = formatterText(textoTermos)
            print('Termos formatados: ', texto_formatado)

        except sr.UnknownValueError:
            print("Não consegui entender o que você disse.")
        except sr.RequestError as e:
            print(f"Erro na requisição ao serviço de reconhecimento de fala: {e}")
        except Exception as e:
            print(f"Ocorreu um erro: {e}")