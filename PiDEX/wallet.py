from kivy.app import App  # Import Kivy framework
from kivy.uix.boxlayout import BoxLayout  # Import layout for UI
from kivy.uix.button import Button  # Import button widget
from kivy.uix.label import Label  # Import label widget
import requests  # Import requests to communicate with Flask API

class WalletApp(App):
    """ Kivy Wallet App """

    def build(self):
        """ Build UI Layout """
        self.layout = BoxLayout(orientation='vertical')  # Create vertical layout

        self.balance_label = Label(text="Balance: Loading...")  # Label to display balance
        self.refresh_button = Button(text="Refresh Balance", on_press=self.get_balance)  # Button to refresh balance

        self.layout.add_widget(self.balance_label)  # Add label to UI
        self.layout.add_widget(self.refresh_button)  # Add button to UI

        return self.layout  # Return UI layout

    def get_balance(self, instance):
        """ Fetch balance from Flask API """
        response = requests.get("http://127.0.0.1:5000/balance/user1")  # Request user1's balance
        balance = response.json().get("balance", "Error")  # Get balance or error message
        self.balance_label.text = f"Balance: {balance} Pi"  # Update label with balance

if __name__ == '__main__':
    WalletApp().run()  # Run Kivy app
class WalletApp(App):
    def get_balance(self, instance):
        response = requests.get("https://your-pi-wallet.vercel.app/balance/user1")
        balance = response.json().get("balance", "Error")
        self.balance_label.text = f"Balance: {balance} Pi"
