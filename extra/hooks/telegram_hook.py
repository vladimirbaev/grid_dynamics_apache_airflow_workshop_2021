from airflow.hooks.base_hook import BaseHook
from telebot import TeleBot


class TelegramHook(BaseHook):

    def __init__(self, conn_id):
        self.conn_id = conn_id
        self.chat_id = None

    def get_conn(self) -> TeleBot:
        conn = self.get_connection(self.conn_id)
        self.chat_id = conn.login
        token = conn.get_password()
        return TeleBot(token)

    def run(self, message):
        conn = self.get_conn()
        print(self.chat_id, message)
        return conn.send_message(self.chat_id, message)
