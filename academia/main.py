from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.metrics import dp
from kivymd.app import MDApp
from kivymd.uix.progressbar import MDProgressBar

class ContadorApp(MDApp):
    def build(self):
        self.numero_repeticoes = 3
        self.numero_maximo = 12
        self.contagem_atual = 1
        self.intervalo_entre_numeros = 5  # Intervalo entre cada número na contagem em segundos

        # Configurar o tema para se adaptar às cores do sistema (Light ou Dark)
        self.theme_cls.theme_style = "Dark"  # Você pode ajustar para "Dark" se preferir

        layout = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10))

        self.label = Label(text="", font_size=dp(25))
        layout.add_widget(self.label)

        self.circular_bar = MDProgressBar()
        layout.add_widget(self.circular_bar)

        self.botao_iniciar = Button(text="Iniciar Contagem", on_press=self.iniciar_contagem,
                                    font_size=dp(14), background_color=self.theme_cls.primary_color,
                                    size_hint_x=None, width=dp(450))  # Ajuste a largura aqui
        layout.add_widget(self.botao_iniciar)

        self.botao_parar = Button(text="Parar Contagem", on_press=self.parar_contagem, state='normal',
                                  font_size=dp(14), background_color=self.theme_cls.accent_color,
                                  size_hint_x=None, width=dp(450))  # Ajuste a largura aqui
        layout.add_widget(self.botao_parar)

        return layout

    def iniciar_contagem(self, instance):
        self.botao_iniciar.disabled = True
        self.botao_parar.disabled = False
        self.circular_bar.max = self.numero_maximo
        self.contagem(1)

    def contagem(self, numero):
        if self.contagem_atual <= self.numero_repeticoes:
            if numero <= self.numero_maximo:
                self.label.text = str(numero)
                self.circular_bar.value = numero
                Clock.schedule_once(lambda dt: self.contagem(numero + 1), self.intervalo_entre_numeros)
            else:
                self.label.text = "Contagem Concluída - Repetição {}".format(self.contagem_atual)
                self.contagem_atual += 1
                Clock.schedule_once(self.iniciar_proxima_repeticao, 2)
        else:
            self.label.text = "Contagem Finalizada"
            self.botao_iniciar.disabled = False
            self.botao_parar.disabled = True

    def iniciar_proxima_repeticao(self, dt):
        self.label.text = "Intervalo: 30s"
        self.circular_bar.value = 0
        Clock.schedule_once(self.resetar_contagem, 30)

    def resetar_contagem(self, dt):
        self.label.text = ""
        self.contagem(1)

    def parar_contagem(self, instance):
        self.label.text = "Contagem Interrompida"
        self.botao_iniciar.disabled = False
        self.botao_parar.disabled = True


if __name__ == "__main__":
    ContadorApp().run()
