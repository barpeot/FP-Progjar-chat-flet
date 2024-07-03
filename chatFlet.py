from chatClient import *


import flet as ft


TARGET_IP = os.getenv("SERVER_IP") or "172.16.16.101"
TARGET_PORT = os.getenv("SERVER_PORT") or "8889"
ON_WEB = os.getenv("ONWEB") or "0"


def main(page: ft.Page):
    cc = ChatClient()
    page.title = "Chat Client App"

    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    username_input = ft.Ref[ft.TextField]()
    password_input = ft.Ref[ft.TextField]()
    name_input = ft.Ref[ft.TextField]()
    country_input = ft.Ref[ft.TextField]()
    groupname_input = ft.Ref[ft.TextField]()
    usernameto_input = ft.Ref[ft.TextField]()
    message_input = ft.Ref[ft.TextField]()
    filepath_input = ft.Ref[ft.TextField]()
    output = ft.Ref[ft.Text]()

    user_logged_in=""
    token=""

    def show_login(e=None):
        page.clean()
        page.add(
            ft.Column(
                [
                    ft.Text(value="Progjar Chat App", size=32),
                    ft.TextField(width=500, label="Username", ref=username_input),
                    ft.TextField(width=500, label="Password", ref=password_input, password=True, can_reveal_password=True),
                    ft.Row(
                        [
                            ft.ElevatedButton(text="Login", on_click=on_login),
                            ft.ElevatedButton(text="Register Page", on_click=show_register),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    ft.Text(value="", ref=output),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            )
        )
        page.update()

    def show_register(e=None):
        page.clean()
        page.add(
            ft.Column(
                [
                    ft.Text(value="Register Akun", size=32),
                    ft.TextField(width=500, label="Username", ref=username_input),
                    ft.TextField(width=500, label="Password", ref=password_input, password=True, can_reveal_password=True),
                    ft.TextField(width=500, label="Nama Lengkap", ref=name_input),
                    ft.TextField(width=500, label="Negara", ref=country_input),
                    ft.Row(
                        [
                            ft.ElevatedButton(text="Kembali", on_click=show_login),
                            ft.ElevatedButton(text="Register", on_click=on_register),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    ft.Text(value="", ref=output),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            )
        )
        page.update()

    def show_main(e=None):
        page.clean()
        page.add(
            ft.Column(
                [
                    ft.Text(value="Hai," + user_logged_in, size=32),
                    ft.Text(value="Token User: " + token),
                    ft.Text(value="", ref=output),
                    ft.Container(
                        content=ft.Row(
                            [
                                ft.Icon(name=ft.icons.PEOPLE),
                                ft.Text("Private Chat"),
                            ],
                            alignment=ft.MainAxisAlignment.START,
                        ),
                        alignment=ft.alignment.center,
                        bgcolor=ft.colors.GREEN_200,
                        width=page.width,
                        height=48,
                        border_radius=10,
                        ink=True,
                        on_click=show_chat_list,
                    ),
                    ft.Container(
                        content=ft.Row(
                            [
                                ft.Icon(name=ft.icons.GROUPS), 
                                ft.Text("View Group Chat"),
                            ],
                            alignment=ft.MainAxisAlignment.START,
                        ),
                        alignment=ft.alignment.center,
                        bgcolor=ft.colors.CYAN_200,
                        width=page.width,
                        height=48,
                        border_radius=10,
                        ink=True,
                        on_click=lambda e: print("Clickable with Ink clicked!"),
                    ),
                    ft.Container(
                        content=ft.Row(
                            [
                                ft.Icon(name=ft.icons.GROUPS), 
                                ft.Text("Add Group Chat"),
                            ],
                            alignment=ft.MainAxisAlignment.START,
                        ),
                        alignment=ft.alignment.center,
                        bgcolor=ft.colors.RED_200,
                        width=page.width,
                        height=48,
                        border_radius=10,
                        ink=True,
                        on_click=show_add_groups,
                    ),
                    ft.ElevatedButton(text="Logout", on_click=logout)
                ]
            )
        )
        page.update()

    def show_chat_list(e=None):
        users = cc.getusers()
        user_containers = []
        
        for user in users:
            if user['username'] != user_logged_in:
                user_containers.append(
                    ft.Container(
                        content=ft.Text(user['username']),
                        alignment=ft.Alignment(-0.95, 0.0),
                        bgcolor=ft.colors.CYAN_200,
                        width=page.width,
                        height=48,
                        border_radius=10,
                        ink=True,
                        on_click=lambda e: print("Clickable with Ink clicked!"),
                    ),
                )

        page.clean()
        page.add(
            ft.Column(
                controls=user_containers
            ),
            ft.ElevatedButton(text="Kembali", on_click=show_main)
        )
        page.update()

    def show_groups(e=None):
        return True

    def show_add_groups(e=None):
        page.clean()
        page.add(
            ft.Column(
                [
                    ft.Text(value="Add New Group", size=32),
                    ft.TextField(width=500, label="Nama Group", ref=groupname_input),
                    ft.Row(
                        [
                            ft.ElevatedButton(text="Kembali", on_click=show_main),
                            ft.ElevatedButton(text="Tambahkan", on_click=on_add_group),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    ft.Text(value="", ref=output),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            )
        )
        page.update()
        
    def show_chat(e=None):
        return True

    def on_login(e):
        nonlocal user_logged_in, token
        username=username_input.current.value
        password=password_input.current.value
        if username and password:
            result=cc.proses("auth {} {}".format(username, password))
            output.current.value=result
            output.current.update()
        else:
            output.current.value="Tolong isi field username dan password"
            output.current.update()
        if "OK" in result:
            message=result.split("|")
            user_logged_in=message[1]
            token=message[2]
            show_main()
        else:
            output.current.value=result
            output.current.update()

    def on_register(e):
        nonlocal user_logged_in, token
        username=username_input.current.value
        password=password_input.current.value
        nama=name_input.current.value
        negara=country_input.current.value
        if username and password and nama and negara:
            result=cc.proses("register {} {} {} {}".format(username, password, negara, nama))
            message = result.split(" ")
            user_logged_in=message[1]
            token=message[2]
            show_main()
        else:
            output.current.value="Tolong isi semua field registrasi"
            output.current.update()

    def on_add_group(e):
        group=groupname_input.current.value
        if group:
            result=cc.proses("addgroup {}".format(group))
            output.current.value=result
            output.current.update()
            if "successful" in result:
                show_main()
                output.current.value=result
                output.current.update()
        else:
            output.current.value="Tolong isi nama group"
            output.current.update() 
    
    def logout(e):
        nonlocal user_logged_in, token
        user_logged_in=""
        token=""
        show_login()

    show_login()

if __name__=='__main__':
    ft.app(target=main)
