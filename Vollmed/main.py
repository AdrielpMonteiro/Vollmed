
from sklearn.feature_extraction.text import CountVectorizer
import pandas as pd 
from sklearn.naive_bayes import MultinomialNB 
from sklearn.pipeline import Pipeline 
import numpy as np 
import google.generativeai as genai 
import json 


genai.configure(api_key="AIzaSyCT1eEjgr6hzZPIdKxvi6MDeWWEuhoVP_c")

def chat_google_ai(mensagem):
    try:
        model = genai.GenerativeModel("gemini-2.0-flash-lite")  
        response = model.generate_content(mensagem)
        return response.text
    except Exception as e:
        return f"Erro: {e}"
    

#while True: 
    #texto = input("Você->  ")
    #if texto.lower() == "sair":
   ##     break
   ##     resposta = chat_google_ai(texto)
        print(f"Gemini: {resposta}")
        print("-" * 40)

##print(chat_google_ai("Olá, bom dia!"))


Frases =  [
    ##Saudações
    "Boa Dia   ",
    "Boa tarde ",
    "Boa noite  ",
    "Oi ",
    "Tudo bem? ",


    ##Ajuda
    "Preciso de ajuda",
    "Preciso de auxilio",
    "Gostaria ",
    
    ##informações
    "Qual horário de funcionamento",
    "Que horas vocês abrem", 
    "Telefone da clinica",

    ##cancelamento  
    "Quero cancelar meu plano",
    "cancelamento",
    "não quero mais continuar com plano ",

    ##Exaemes
    "Exame",
    "quero saber valores dos meus exames",
    "Resultado Exaemes",
    "Exames",

]


categorias = [
    "SAUDAÇÃO","SAUDAÇÃO","SAUDAÇÃO","SAUDAÇÃO","SAUDAÇÃO",
    "AJUDA","AJUDA","AJUDA",
    "INFORMAÇÕES","INFORMAÇÕES","INFORMAÇÕES",
    "CANCELAMENTO","CANCELAMENTO","CANCELAMENTO",
    "EXAMES","EXAMES","EXAMES","EXAMES"
]


modelo = Pipeline([
    ('vetorizacao', CountVectorizer()),
    ('classificador', MultinomialNB())
])


respostas = {
    "SAUDACAÇÃO: Olá Bem vindo , a Clinica VollMed ! "

    "AJUDA: Olá Bem vindo ,  Como posso ajudá-ló hoje? "

    "INFORMAÇÕES: 📋 **Informações da Clínica:**\n• Horário: Segunda a Sexta, 7h às 19h\n• Telefone: (11) 3333-4444\n• Endereço: Rua Medical, 123 - Centro\n• WhatsApp: (11) 98888-7777"

    "CANCELAMENTO: Poxa que pena , vou te transferir para um representante ! Espero que muda de opnião e continue conosco! "

    "EXAMES: Olá \n Exames Disponivéis  \n*  Agendamento de Exames \n "

}



modelo.fit(Frases, categorias) 

def chat_google_ai(mensagem):
    try:
        model = genai.GenerativeModel("gemini-2.0-flash-lite")  
        response = model.generate_content(mensagem)
        return response.text
    except Exception as e:
        return f"Erro: {e}"


# Nessa Função, o chatbot responde com respostas fixas
def verificar_mensagem(mensagem: str) -> str:
    categoria = modelo.predict([mensagem.lower()])[0]

    if categoria in respostas: 
        return respostas[categoria]
    else: 
        return chat_google_ai(mensagem)
    
usuario = input ("digite seu nome: ")

def salvar_hist(usuario,mensagem,resposta): 
    historico = carregar_hist(usuario)
    historico.append({"mensagem": mensagem , "resposta" : resposta })
    with open(f'{usuario}_historico.json','w') as file:
        json.dump(historico,file,indent=4)

def carregar_hist(usuario):
    try:
        with open(f'{usuario}_historico.json','r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []

historico = carregar_hist(usuario)


#Teste de Confiança:
def confiança (mensagem: str, liminar: float = 0.4):

    #Prever a probabilidade
    probabilidades = modelo.predict_proba([mensagem.lower()])[0]

    #Encontra a categoria que tem a maior probabilidade
    indice_max = probabilidades.argmax()
    probabilidade_max = probabilidades[indice_max]
    categoria_prevista = modelo.classes_[indice_max]

    #Maio ou menor?
    if probabilidade_max >= liminar and categoria_prevista in respostas:
        return respostas[categoria_prevista] #Aqui retorna a resposta fixa se a confiança for maior que a liminar
    
    else:
        return chat_google_ai(mensagem) #Aqui consulta o Gemini se a confiança for menor que a liminar


while True: 
    texto = input(f"{usuario} -- ").lower().strip()
    if texto.lower() == "sair":
        print("chat encerrado")
        break

    #Vai ser a reposta fixa ou a do Gemini?
    if texto in respostas:
        resposta = respostas [texto]
    else:
        resposta = confiança (texto)
        
    print(f"Gemini: {resposta}")
    print("-" * 40)
    salvar_hist(usuario, texto, resposta)






##print(chat_google_ai("Olá, bom dia!"))

#entrada = input("Digite uma frase para o chatbot: ")
saida = modelo.predict([texto])[0]
##print(f"Categoria prevista: {saida[0]}")

