# Passo a Passo:
# Passo 1 - Botão de iniciar chat
# Passo 2 - popup para entratr no chat
# Passo 3 - quando entrar no chat: (aprece para todo mundo)
    # a mensagem que você entrou no chat
    # o compo e o borao de enviar mensagem
# Passo 4 - a cada mensagem que você envia (aprece para todo mundo)
    # Nome: Texo da mensagem

import flet as ft

def main(page):
    texto = ft.Text("WhatsApp 2");

    chat = ft.Column();

    userName = ft.TextField(label ="Escreva seu nome aqui:");

    def sendMsgTunnel(message):
        type = message["type"]
        if type == "message":
            msgText = message["text"];
            msgUser = message["user"];
            # adicionar a mensagem no chat
            chat.controls.append(ft.Text(f"{msgUser}: {msgText}"));
        else:
            msgUser = message["user"];
            chat.controls.append(ft.Text(f"{msgUser} entrou no chat",
                                        size=12, italic=True, color=ft.colors.CYAN_ACCENT_100));
        page.update();
    
    # PUBSUB
    page.pubsub.subscribe(sendMsgTunnel)

    def sendMsg(evento):
        page.pubsub.send_all({"text":messageField.value, "user":userName.value,
                                "type":"mensagem"});
        # limpar o campo de mensagem
        messageField.value = "";
        page.update();

    messageField = ft.TextField(label="Digite uma mensagem");
    sendBtn = ft.ElevatedButton("Enviar", on_click=sendMsg);

    def enterPopup(evento):
        page.pubsub.send_all({"user":userName.value, "type":"entrada"})
        # adicionar o chat
        page.add(chat);
        # fechar o popup
        popup.open = False;
        # remover o botão iniciar chat
        page.remove(startBtn);
        # criar o campo de mensagem de usuario
        page.add(ft.Row(
                [messageField,sendBtn])
            );
        # criar o botão de enviar mensagem do usuario
        page.remove(texto);
        page.update();

    popup = ft.AlertDialog(
        open = False,
        modal = True,
        title = ft.Text("Bem vindo ao whatsapp 2"),
        content= userName,
        actions=[ft.ElevatedButton("Entrar", on_click= enterPopup),ft.ElevatedButton("Sair")],
    );

    def enterChat(evento):
        page.dialog = popup;
        popup.open = True;
        page.update();


    startBtn = ft.ElevatedButton("Iniciar chat",on_click=enterChat)

    page.add(texto);
    page.add(startBtn)

ft.app(target=main, view=ft.WEB_BROWSER, port=8000, assets_dir="assets");