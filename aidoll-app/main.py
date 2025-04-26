from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from android.permissions import request_permissions, Permission
from jnius import autoclass
import threading

class BluetoothApp(App):
    def build(self):
        self.bt_socket = None
        self.recording = False # recording
        
        # Ask for Bluetooth permissions on Android 12+
        request_permissions([
            Permission.BLUETOOTH,
            Permission.BLUETOOTH_CONNECT,
            Permission.BLUETOOTH_SCAN,
        ])

        # Connect to pi button
        layout = BoxLayout(orientation='vertical')
        
        self.connect_btn = Button(text="Connect to Pi")
        self.connect_btn.bind(on_press=self.connect_pi)
        layout.add_widget(self.connect_btn)
        
        # Cue Me Button
        self.cue_me_btn = Button(text="Cue Me!", disabled=True)
        self.cue_me_btn.bind(on_press=self.send_cue_me)
        layout.add_widget(self.cue_me_btn)
        
        # Notification Button
        self.ntf_btn = Button(text="Notification!", disabled=True)
        self.ntf_btn.bind(on_press=self.send_notification)
        layout.add_widget(self.ntf_btn)
        
        # Cue Me Button
        self.mute_btn = Button(text="Mute", disabled=True)
        self.mute_btn.bind(on_press=self.send_mute)
        layout.add_widget(self.mute_btn)

        return layout

    def connect_pi(self, instance):
        # pass
        if(self.bt_socket == None):
            # threading.Thread(target=self._send_data_to_pi).start()
            threading.Thread(target=self._connect_to_pi).start()
        else:
            threading.Thread(target=self._disconnect_to_pi).start()
            
    def send_cue_me(self, instance):
        if(self.recording == False):
            self.__send_to_device__("Cue me.")
            self.cue_me_btn.text = "Cue ok."
            self.recording = True
        else:
            self.__send_to_device__("Cue ok.")
            self.cue_me_btn.text = "Cue me."
            self.recording = False
        
    def send_interact(self, instance):
        if(self.recording == False):
            threading.Thread(target=self._start_recording).start()
        else:
            threading.Thread(target=self._end_recording).start()
            
    def send_notification(self, instance):
        self.__send_to_device__("Notification.")
        
    def take_a_picture(self, instance):
        self._take_a_picture()
        
    def invoke_response(self, instance):
        self._invoke_response()
    
    def send_mute(self, instance):
        self.__send_to_device__("Mute")
    
    def send_wifi(self, instance):
        pass
    
    def _connect_to_pi(self):
        # Android Bluetooth classes
        BluetoothAdapter = autoclass('android.bluetooth.BluetoothAdapter')
        BluetoothDevice = autoclass('android.bluetooth.BluetoothDevice')
        UUID = autoclass('java.util.UUID')

        adapter = BluetoothAdapter.getDefaultAdapter()
        # Replace with your Pi's Bluetooth MAC address
        address = "DC:A6:32:8D:9B:A6"

        device = adapter.getRemoteDevice(address)

        # ⚠️ Here's the key change: Use insecure connection on port 1 (no SDP)
        self.bt_socket = device.createRfcommSocket(1)  # ← Android hidden API, may fail

        # Cancel discovery if needed
        if adapter.isDiscovering():
            adapter.cancelDiscovery()
            
        try:
            self.bt_socket.connect()
        except:
            return
        
        # Update UI
        self.connect_btn.text        = "Disconnect from Pi"
        self.cue_me_btn.text           = "Cue me."
        self.cue_me_btn.disabled       = False
        self.ntf_btn.disabled          = False
        self.mute_btn.disabled         = False
        # self.interact_btn.disabled   = False
        # self.take_a_pic_btn.disabled = False
        # self.invoke_res_btn.disabled = False
        # self.wifi_btn.disabled       = False
        
        print("Bluetooth connected!")
        
    def _disconnect_to_pi(self):
        self.bt_socket.close()
        self.bt_socket = None
       
        # Update UI
        self.connect_btn.text        = "Connect to Pi"
        self.cue_me_btn.text           = "Cue me."
        self.cue_me_btn.disabled       = True
        self.ntf_btn.disabled          = True
        self.mute_btn.disabled         = True
        # self.interact_btn.disabled   = True
        # self.take_a_pic_btn.disabled = True
        # self.invoke_res_btn.disabled = True
        # self.wifi_btn.disabled       = True
        
        self.recording = False
        
        
    def _start_recording(self):
        self.__send_to_device__("Start recording.")
        
        # Update state
        self.recording = True
        
        # Update UI
        # self.interact_btn.text = "Stop recording"
        self.cue_me_btn.text = "Cue ok!"
        
    def _end_recording(self):
        self.__send_to_device__("Stop recording.")
        
        # Update state
        self.recording = False
        
        # Update UI
        # self.interact_btn.text = "Start recording"
        self.cue_me_btn.text = "Cue Me!"
        
        
        
        
    def _take_a_picture(self):
        self.__send_to_device__("Take a picture.")
        
    def _invoke_response(self):
        self.__send_to_device__("Invoke response.")
        
    def __send_to_device__(self, msg):
        try:
            output = self.bt_socket.getOutputStream()
            message = msg
            output.write(bytes(message, "UTF-8"))
            output.flush()
        except:
            return
    # def _send_data_to_pi(self):
    #     try:
    #         # Android Bluetooth classes
    #         BluetoothAdapter = autoclass('android.bluetooth.BluetoothAdapter')
    #         BluetoothDevice = autoclass('android.bluetooth.BluetoothDevice')
    #         UUID = autoclass('java.util.UUID')

    #         adapter = BluetoothAdapter.getDefaultAdapter()

    #         # Replace with your Pi's Bluetooth MAC address
    #         address = "DC:A6:32:8D:9B:A6"

    #         device = adapter.getRemoteDevice(address)

    #         # ⚠️ Here's the key change: Use insecure connection on port 1 (no SDP)
    #         socket = device.createRfcommSocket(1)  # ← Android hidden API, may fail

    #         # Cancel discovery if needed
    #         if adapter.isDiscovering():
    #             adapter.cancelDiscovery()

    #         socket.connect()

    #         # output = socket.getOutputStream()
    #         # message = "Hello Pi!"
    #         # output.write(bytes(message, "UTF-8"))
    #         # output.flush()
            
    #         # ---------- SEND --------------------------------------------------
    #         out_stream = socket.getOutputStream()
    #         msg        = b"Hello Pi!\n"
    #         out_stream.write(jarray('b', msg))
    #         out_stream.flush()
    #         print("> sent:", msg.decode().strip())

    #         # ---------- RECEIVE (blocking) ------------------------------------
    #         in_stream  = socket.getInputStream()
    #         buf        = jarray('b', 256)        # Java byte[] buffer
    #         received   = bytearray()

    #         while True:
    #             n = in_stream.read(buf)          # returns -1 on EOF
    #             if n == -1:
    #                 raise IOError("Pi closed the connection")

    #             received.extend(buf[:n])

    #             # stop when we see a newline
    #             if received.endswith(b"\n"):
    #                 break
                
    #         answer = received.decode("utf-8", "replace").strip()
    #         print("< recv:", answer)

    #         # socket.close()
    #         print("Message sent!")

    #     except Exception as e:
    #         print(f"[Bluetooth Error] {e}")

BluetoothApp().run()
