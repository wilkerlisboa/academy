from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.metrics import dp


class ContadorApp(App):
    def build(self):
        self.numero_repeticoes = 3
        self.numero_maximo = 12
        self.contagem_atual = 1

        layout = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10))

        self.label = Label(text="", font_size=dp(36))
        layout.add_widget(self.label)

        self.botao_iniciar = Button(text="Iniciar Contagem", on_press=self.iniciar_contagem,
                                    font_size=dp(14), background_color=(0.2, 0.7, 0.3, 1),
                                    size_hint_x=None, width=dp(200))  # Ajuste a largura aqui
        layout.add_widget(self.botao_iniciar)

        self.botao_parar = Button(text="Parar Contagem", on_press=self.parar_contagem, state='normal',
                                  font_size=dp(14), background_color=(0.8, 0.2, 0.2, 1),
                                  size_hint_x=None, width=dp(200))  # Ajuste a largura aqui
        layout.add_widget(self.botao_parar)

        return layout

    def iniciar_contagem(self, instance):
        self.botao_iniciar.disabled = True
        self.botao_parar.disabled = False
        self.contagem(1)

    def contagem(self, numero):
        if self.contagem_atual <= self.numero_repeticoes:
            if numero <= self.numero_maximo:
                self.label.text = str(numero)
                Clock.schedule_once(lambda dt: self.contagem(numero + 1), 6)  # Intervalo de 6 segundos
            else:
                self.label.text = "Contagem Concluída - Repetição {}".format(self.contagem_atual)
                self.contagem_atual += 1
                Clock.schedule_once(self.iniciar_proxima_repeticao, 54)
        else:
            self.label.text = "Contagem Finalizada"
            self.botao_iniciar.disabled = False
            self.botao_parar.disabled = True

    def iniciar_proxima_repeticao(self, dt):
        self.label.text = "Intervalo: 54s"
        Clock.schedule_once(self.resetar_contagem, 54)

    def resetar_contagem(self, dt):
        self.label.text = ""
        self.contagem(1)

    def parar_contagem(self, instance):
        self.label.text = "Contagem Interrompida"
        self.botao_iniciar.disabled = False
        self.botao_parar.disabled = True


if __name__ == "__main__":
    ContadorApp().run()
