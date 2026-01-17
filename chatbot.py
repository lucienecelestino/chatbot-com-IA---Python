# titulo
# input do chat (campo de mensagem)
# a cada mensagem enviada:
    # mostrar a mensagem que o usuario enviou no chat
    # enviar essa mensagem para a IA responder
    # aparece na tela a resposta da IA

# streamlit - Apenas com o python é possivel criar o frontend e backend
# IA utilizada: Groq pois a API da OpenAI é paga 
#pip install groq streamlit
# para rodar o chatbot -> no terminal digite: streamlit run nome_do_seu_arquivo

#mantendo meu codigo de api seguro
import os
from dotenv import load_dotenv
load_dotenv()

import streamlit as st
from groq import Groq

#criando meu modelo de IA, da Groq, com a API
modelo_ia = Groq(api_key=os.getenv("GROQ_API_KEY")) #usando a api

st.write("# Chatbot com IA") # markdown -> se usa o "#"

# vai verificar se é a primeira vez que o usuário já interagiu, se sim, vai exibir a lista vazia, se não a vai exibir a lista de onde parou a "conversa"

if not "lista_mensagens" in st.session_state:  # session_state -> cookie no navegador do usuário, guarda o histórico da conversa
    
    # Mensagem inicial que define a PERSONALIDADE da IA (prompt do sistema)
    st.session_state["lista_mensagens"] = [
        {
            "role": "system",
            "content": "Você é uma assistente educada, paciente e didática. Explique as coisas de forma simples, clara e com exemplos quando possível. Responda sempre em português."
        }
    ]


texto_usuario = st.chat_input("Digite sua Mensagem")

#meu dicionario se chama "mensagem"
for mensagem in st.session_state["lista_mensagens"]: #para cada mensagem, quero colocar a mensagem na tela
    role = mensagem["role"]
    content = mensagem["content"]
    st.chat_message(role).write(content)


if texto_usuario:
    st.chat_message("user").write(texto_usuario)
    mensagem_usuario = {"role": "user", "content": texto_usuario} #criando uma mensagem, com a funcionalidade dicionario
    st.session_state["lista_mensagens"].append(mensagem_usuario)#adicionando a mensagem enviada na lista

    #IA respondeu:
    resposta_ia = modelo_ia.chat.completions.create(
        messages=st.session_state["lista_mensagens"],
        model="llama-3.1-8b-instant") 
    
    texto_resposta_ia = resposta_ia.choices[0].message.content # texto da resposta da IA

  
    st.chat_message("assistant").write(texto_resposta_ia)
    messagem_ia = {"role": "assistant", "content": texto_resposta_ia}
    st.session_state["lista_mensagens"].append(messagem_ia)#adicionando a resposta enviada na lista

   # print(st.session_state["lista_mensagens"]) -> testando no terminal se estava ocorrendo a comunicação entre o chatbot e a ia