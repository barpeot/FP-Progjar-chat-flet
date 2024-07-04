from chatClient import *


import flet as ft


TARGET_IP = os.getenv("SERVER_IP") or "172.16.16.101"
TARGET_PORT = os.getenv("SERVER_PORT") or "8889"
ON_WEB = os.getenv("ONWEB") or "0"

class Message():
    # nonlocal user_logged_in
    def __init__(self, user: str, text: str):
        self.user = user
        self.text = text

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
                                ft.Text("Group Chat"),
                            ],
                            alignment=ft.MainAxisAlignment.START,
                        ),
                        alignment=ft.alignment.center,
                        bgcolor=ft.colors.CYAN_200,
                        width=page.width,
                        height=48,
                        border_radius=10,
                        ink=True,
                        on_click=show_groups,
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
                    ft.Container(
                        content=ft.Row(
                            [
                                ft.Icon(name=ft.icons.GROUPS), 
                                ft.Text("Join Group Chat"),
                            ],
                            alignment=ft.MainAxisAlignment.START,
                        ),
                        alignment=ft.alignment.center,
                        bgcolor=ft.colors.CYAN_200,
                        width=page.width,
                        height=48,
                        border_radius=10,
                        ink=True,
                        on_click=show_join_groups,
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
            username = user['username']
            if user_logged_in.strip() != username:
                user_containers.append(
                    ft.Container(
                        content=ft.Row([
                            ft.Icon(name=ft.icons.PERSON),
                            ft.Text(user['username'])
                        ]),
                        alignment=ft.Alignment(-0.95, 0.0),
                        bgcolor=ft.colors.CYAN_200,
                        width=page.width,
                        height=48,
                        border_radius=10,
                        ink=True,
                        on_click=lambda e, username=username: show_chat(username),
                    )
                )

        page.clean()
        page.add(
            ft.Text(value="Pilih User", size=32),
            ft.Text(value="", ref=output),
            ft.Column(
                controls=user_containers
            ),
            ft.ElevatedButton(text="Kembali", on_click=show_main)
        )
        page.update()

    def show_groups(e=None):
        groups = cc.getgroups()
        grouplist = groups['groups']
        group_containers = []

        for group in grouplist:
            group_name = group['group']
            members = group['members']

            group_text = f"{group_name}\nAnggota Group: {', '.join(members)}"
            
            if user_logged_in.strip() in members:
                group_containers.append(
                    ft.Container(
                        content=ft.Row([
                            ft.Icon(name=ft.icons.GROUPS),
                            ft.Text(group_text),
                        ]),
                        alignment=ft.Alignment(-0.95, 0.0),
                        bgcolor=ft.colors.CYAN_200,
                        width=page.width,
                        height=64,
                        border_radius=10,
                        ink=True,
                        on_click=lambda e, group_name=group_name: show_chat_group(group_name),
                    ),
                )    
            

        page.clean()
        if group_containers:
            page.add(
                ft.Text(value="Pilih Group", size=32),
                ft.Text(value="", ref=output),
                ft.Column(controls=group_containers),
                ft.ElevatedButton(text="Kembali", on_click=show_main)
            )
        else:
            page.add(
                ft.Text(value="Pilih Group", size=32),
                ft.Text(value="", ref=output),
                ft.Text(value="Tidak ada group yang kamu join!"),
                ft.ElevatedButton(text="Kembali", on_click=show_main)
            )
        page.update()

    def show_join_groups(e=None):
        groups = cc.getgroups()
        grouplist = groups['groups']
        group_containers = []

        for group in grouplist:
            group_name = group['group']
            members = group['members']

            if user_logged_in.strip() not in members:
                group_text = f"{group_name}\nAnggota Group: {', '.join(members)}"
                
                group_containers.append(
                    ft.Container(
                        content=ft.Row([
                            ft.Icon(name=ft.icons.GROUPS),
                            ft.Text(group_text),
                        ]),
                        alignment=ft.Alignment(-0.95, 0.0),
                        bgcolor=ft.colors.CYAN_200,
                        width=page.width,
                        height=64,
                        border_radius=10,
                        ink=True,
                        on_click=lambda e, group_name=group_name: on_join_group(group_name),
                    ),
                )
    
        page.clean()
        if group_containers:
            page.add(
                ft.Text(value="Pilih Group", size=32),
                ft.Text(value="", ref=output),
                ft.Column(controls=group_containers),
                ft.ElevatedButton(text="Kembali", on_click=show_main)
            )
        else:
            page.add(
                ft.Text(value="Pilih Group", size=32),
                ft.Text(value="", ref=output),
                ft.Text(value="Tidak ada group yang dapat kamu join!"),
                ft.ElevatedButton(text="Kembali", on_click=show_main)
            )
        page.update()

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
        
    def show_chat(username):
        # Chat messages
        chat = ft.ListView(
            spacing=10,
            auto_scroll=True,
            height=page.height - 200,
        )
    
        # A new message entry form
        new_message = ft.TextField(
            hint_text="Write a message...",
            autofocus=True,
            shift_enter=True,
            min_lines=1,
            max_lines=5,
            filled=True,
            expand=True,
            #on_submit=send_message_click,
        )

        def popupFile(e=None): 
            dialog = ft.AlertDialog(
                open=True,
                modal=True,
                title=ft.Text("Input File Path"),
                content=ft.Column(
                    [ft.TextField(label="Filepath", ref=filepath_input)], 
                    tight=True
                ),
                actions=[
                    ft.ElevatedButton(text="Cancel", on_click=lambda e: close_dialog(dialog)),
                    ft.ElevatedButton(text="Send File", on_click=lambda e: send_file( username, filepath_input, dialog))
                ],
                actions_alignment="end",
            )
            page.overlay.append(dialog)
            page.update()
            
        def close_dialog(dialog):
            dialog.open = False
            page.update()

        def inbox(username):
            user=username
            rcvmsg = cc.proses("privateinbox {}" .format(user))
            data = json.loads(rcvmsg)

            # # Extract the messages
            
            # messages = []
            # files = []
            for key in data:
                for item in data[key]:
                    if 'msg' in item:
                        new_message_widget = ft.Text("{} : {}".format(item['msg_from'], item['msg']))
                        chat.controls.append(new_message_widget)
                    elif 'file_name' in item:
                        new_item_widget = ft.Text("{} : sent {}".format(item['msg_from'], item['file_name']))
                        chat.controls.append(new_item_widget)
                        try:
                            image_bytes = item['file_content']
                            image = ft.Image(
                                src=item['address'],
                                width=100,
                                height=100,
                                fit=ft.ImageFit.CONTAIN,
                            )
                            chat.controls.append(image)
                        except Exception as e:
                            print(f"Error decoding file content: {e}")
                        
                    
            
            # # Print the messages
            # for msg in messages:
            #     print(msg)
            #     new_message_widget = ft.Text("{} : {}".format(user, msg))
            #     chat.controls.append(new_message_widget)

            chat.update()
            page.update()
        
        # Function to handle send button click
        def send_click(e):
            nonlocal user_logged_in
            # Get the message text
            message_text = new_message.value
            if message_text:
                # Create a new Text widget for the message
                new_message_widget = ft.Text("{} : {}".format(user_logged_in, message_text))
                cc.proses("send {} {}".format(username, message_text))
                # Append the new message to the ListView
                chat.controls.append(new_message_widget)
                
                # Clear the text field
                new_message.value = ""
                
                # Update the ListView and page
                chat.update()
                page.update()

        def send_file(username, filepath, dialog):
            print(username)
            print(filepath.current.value)
            file=filepath.current.value
            rcvmsg = cc.proses("sendfile {} {}" .format(username, file))
            print(rcvmsg)
            close_dialog(dialog)
            new_message_widget = ft.Text("{} : sent {}".format(user_logged_in, file))
            chat.controls.append(new_message_widget)
            
            filepath = rcvmsg
            
            
            try:
                image = ft.Image(
                    src=filepath,
                    width=100,
                    height=100,
                    fit=ft.ImageFit.CONTAIN,
                )
                chat.controls.append(image)
            except Exception as e:
                print(f"Error decoding file content: {e}")
            
            chat.update()
            page.update()
    
        page.clean()
    
        # Add everything to the page
        page.add(
            ft.Column(
                [
                    ft.Row(
                        [
                            ft.IconButton(
                                icon=ft.icons.ARROW_BACK,
                                tooltip="Back",
                                on_click=show_chat_list,
                            ),
                            ft.Text(f"Chat with {username}", size=32),
                        ],
                    ),
                    ft.Container(
                        content=chat,
                        border=ft.border.all(1, ft.colors.OUTLINE),
                        border_radius=5,
                        padding=10,
                    ),
                    ft.Row(
                        [
                            new_message,
                            ft.IconButton(
                                icon=ft.icons.SEND_ROUNDED,
                                tooltip="Send message",
                                on_click=send_click,
                            ),
                            ft.IconButton(
                                icon=ft.icons.INBOX,
                                tooltip="Receive message",
                                on_click=lambda e, username=username: inbox(username.strip()),
                            ),
                            ft.IconButton(
                                icon=ft.icons.ATTACH_FILE_ROUNDED,
                                tooltip="Send file",
                                on_click=popupFile,
                            ),
                        ]
                    ),
                ]
            )
        )
    
        page.update()

    def show_chat_group(group_name):
        # Chat messages
        chat = ft.ListView(
            spacing=10,
            auto_scroll=True,
            height=page.height - 200,
        )
    
        # A new message entry form
        new_message = ft.TextField(
            hint_text="Write a message...",
            autofocus=True,
            shift_enter=True,
            min_lines=1,
            max_lines=5,
            filled=True,
            expand=True,
            #on_submit=send_message_click,
        )

        def popupFile(e=None): 
            dialog = ft.AlertDialog(
                open=True,
                modal=True,
                title=ft.Text("Input File Path"),
                content=ft.Column(
                    [ft.TextField(label="Filepath", ref=filepath_input)], 
                    tight=True
                ),
                actions=[
                    ft.ElevatedButton(text="Cancel", on_click=lambda e: close_dialog(dialog)),
                    ft.ElevatedButton(text="Send File", on_click=lambda e: send_file( group_name, filepath_input, dialog))
                ],
                actions_alignment="end",
            )
            page.overlay.append(dialog)
            page.update()
            
        def close_dialog(dialog):
            dialog.open = False
            page.update()

        def inbox(group_name):
            group=group_name
            rcvmsg = cc.proses("groupinbox {}" .format(group))
            data = json.loads(rcvmsg)

            # # Extract the messages
            
            # messages = []
            # files = []
            for key in data:
                for item in data[key]:
                    if 'msg' in item:
                        new_message_widget = ft.Text("{} : {}".format(item['msg_from'], item['msg']))
                        chat.controls.append(new_message_widget)
                    elif 'file_name' in item:
                        new_item_widget = ft.Text("{} : sent {}".format(item['msg_from'], item['file_name']))
                        chat.controls.append(new_item_widget)
                        try:
                            image_bytes = item['file_content']
                            image = ft.Image(
                                src=item['address'],
                                width=100,
                                height=100,
                                fit=ft.ImageFit.CONTAIN,
                            )
                            chat.controls.append(image)
                        except Exception as e:
                            print(f"Error decoding file content: {e}")
                        
                    
            
            # # Print the messages
            # for msg in messages:
            #     print(msg)
            #     new_message_widget = ft.Text("{} : {}".format(user, msg))
            #     chat.controls.append(new_message_widget)

            chat.update()
            page.update()
        
        # Function to handle send button click
        def send_click(e):
            nonlocal user_logged_in
            # Get the message text
            message_text = new_message.value
            if message_text:
                # Create a new Text widget for the message
                new_message_widget = ft.Text("{} : {}".format(user_logged_in, message_text))
                cc.proses("sendgroup {} {}".format(group_name, message_text))
                # Append the new message to the ListView
                
                # Clear the text field
                new_message.value = ""
                
                # Update the ListView and page
                chat.update()
                page.update()

        def send_file(group_name, filepath, dialog):
            print(group_name)
            print(filepath.current.value)
            file=filepath.current.value
            rcvmsg = cc.proses("sendgroupfile {} {}" .format(group_name, file))
            print(rcvmsg)
            close_dialog(dialog)
            new_message_widget = ft.Text("{} : sent {}".format(user_logged_in, file))
            chat.controls.append(new_message_widget)
            chat.update()
            page.update()
    
        page.clean()
    
        # Add everything to the page
        page.add(
            ft.Column(
                [
                    ft.Row(
                        [
                            ft.IconButton(
                                icon=ft.icons.ARROW_BACK,
                                tooltip="Back",
                                on_click=show_groups,
                            ),
                            ft.Text(f"Chat with {group_name}", size=32),
                        ],
                    ),
                    ft.Container(
                        content=chat,
                        border=ft.border.all(1, ft.colors.OUTLINE),
                        border_radius=5,
                        padding=10,
                    ),
                    ft.Row(
                        [
                            new_message,
                            ft.IconButton(
                                icon=ft.icons.SEND_ROUNDED,
                                tooltip="Send message",
                                on_click=send_click,
                            ),
                            ft.IconButton(
                                icon=ft.icons.INBOX,
                                tooltip="Receive message",
                                on_click=lambda e, group_name=group_name: inbox(group_name.strip()),
                            ),
                            ft.IconButton(
                                icon=ft.icons.ATTACH_FILE_ROUNDED,
                                tooltip="Send file",
                                on_click=popupFile,
                            ),
                        ]
                    ),
                ]
            )
        )
    
        page.update()
    
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
            
    def on_join_group(group_name):
        cc.proses("joingroup {}".format(group_name))
        show_main()
        output.current.value="Berhasil Join {}".format(group_name) 
        output.current.update()
    def on_show_private_chat(username):
        nonlocal user_logged_in
        if username.strip().lower() == user_logged_in.strip().lower():
            output.current.value="Tidak bisa chat dengan diri sendiri!"
            output.current.update()
        else:
            print(f"Clicked on user: {user_logged_in} {username}")
    
    def logout(e):
        nonlocal user_logged_in, token
        user_logged_in=""
        token=""
        show_login()

    show_login()

if __name__=='__main__':
    ft.app(target=main)