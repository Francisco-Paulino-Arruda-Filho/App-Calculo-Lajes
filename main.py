from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.scrollview import ScrollView
from kivy.graphics import Color, Rectangle, RoundedRectangle, Line
from kivy.core.window import Window
from kivy.animation import Animation
from kivy.metrics import dp
from kivy.clock import Clock
import numpy as np

# ── Paleta ──────────────────────────────────────────────────────────────────
BG          = (0.06, 0.07, 0.10, 1)   # fundo principal
CARD        = (0.10, 0.12, 0.17, 1)   # card central
ACCENT      = (0.20, 0.55, 0.95, 1)   # azul elétrico
ACCENT2     = (0.10, 0.80, 0.65, 1)   # verde-água
TEXT        = (0.92, 0.94, 0.98, 1)   # branco suave
MUTED       = (0.45, 0.50, 0.60, 1)   # cinza médio
BORDER      = (0.18, 0.22, 0.30, 1)   # borda sutil
SUCCESS     = (0.20, 0.85, 0.60, 1)
INPUT_BG    = (0.13, 0.16, 0.22, 1)

Window.clearcolor = BG

# ── Helpers ──────────────────────────────────────────────────────────────────
def rgba255(r, g, b, a=1):
    return (r/255, g/255, b/255, a)

def hex_color(h, a=1):
    h = h.lstrip('#')
    r, g, b = tuple(int(h[i:i+2], 16)/255 for i in (0, 2, 4))
    return (r, g, b, a)


# ── Fundo animado (partículas) ────────────────────────────────────────────────
class AnimatedBackground(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._dots = []
        self._time = 0
        with self.canvas.before:
            Color(*BG)
            self._bg_rect = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self._update, size=self._update)
        Clock.schedule_interval(self._tick, 1/30)

    def _update(self, *_):
        self._bg_rect.pos  = self.pos
        self._bg_rect.size = self.size

    def _tick(self, dt):
        self._time += dt
        self.canvas.after.clear()
        with self.canvas.after:
            for i in range(8):
                import math
                x = self.width  * (0.1 + 0.12*i + 0.04*math.sin(self._time*0.4 + i))
                y = self.height * (0.15 + 0.10*i + 0.06*math.cos(self._time*0.3 + i*1.3))
                r = dp(2 + math.sin(self._time + i)*1.2)
                alpha = 0.06 + 0.04*math.sin(self._time*0.5 + i)
                Color(*ACCENT[:3], alpha)
                Rectangle(pos=(x-r, y-r), size=(r*2, r*2))


# ── Cartão com borda arredondada ──────────────────────────────────────────────
class Card(BoxLayout):
    def __init__(self, **kwargs):
        kwargs.setdefault('orientation', 'vertical')
        kwargs.setdefault('padding',     [dp(28), dp(24)])
        kwargs.setdefault('spacing',     dp(14))
        super().__init__(**kwargs)
        with self.canvas.before:
            Color(*CARD)
            self._rect = RoundedRectangle(radius=[dp(18)], pos=self.pos, size=self.size)
            Color(*BORDER)
            self._line = Line(rounded_rectangle=[self.x, self.y, self.width, self.height, dp(18)], width=1.2)
        self.bind(pos=self._upd, size=self._upd)

    def _upd(self, *_):
        self._rect.pos  = self.pos
        self._rect.size = self.size
        self._line.rounded_rectangle = [self.x, self.y, self.width, self.height, dp(18)]


# ── Separador ─────────────────────────────────────────────────────────────────
class Divider(Widget):
    def __init__(self, **kwargs):
        kwargs.setdefault('size_hint_y', None)
        kwargs.setdefault('height', dp(1))
        super().__init__(**kwargs)
        with self.canvas:
            Color(*BORDER)
            self._line = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=lambda *_: setattr(self._line, 'pos', self.pos),
                  size=lambda *_: setattr(self._line, 'size', self.size))


# ── Indicador de progresso ────────────────────────────────────────────────────
class MyProgressBar(Widget):
    def __init__(self, total, current=0, **kwargs):
        kwargs.setdefault('size_hint_y', None)
        kwargs.setdefault('height', dp(4))
        super().__init__(**kwargs)
        self.total   = total
        self.current = current
        with self.canvas:
            Color(*BORDER)
            self._bg   = Rectangle(pos=self.pos, size=self.size)
            Color(*ACCENT)
            self._fill = Rectangle(pos=self.pos, size=(0, self.height))
        self.bind(pos=self._upd, size=self._upd)

    def _upd(self, *_):
        self._bg.pos  = self.pos
        self._bg.size = self.size
        pct = self.current / self.total
        self._fill.pos  = self.pos
        self._fill.size = (self.width * pct, self.height)

    def set_progress(self, step):
        self.current = step
        self._upd()


# ── Input estilizado ──────────────────────────────────────────────────────────
class StyledInput(TextInput):
    def __init__(self, **kwargs):
        super().__init__(
            multiline=False,
            background_color=(0, 0, 0, 0),
            foreground_color=TEXT,
            cursor_color=ACCENT,
            hint_text_color=(*MUTED[:3], 0.7),
            font_size=dp(18),
            padding=[dp(16), dp(14)],
            size_hint_y=None,
            height=dp(52),
            **kwargs
        )
        with self.canvas.before:
            Color(*INPUT_BG)
            self._bg   = RoundedRectangle(radius=[dp(10)], pos=self.pos, size=self.size)
            Color(*BORDER)
            self._bord = Line(rounded_rectangle=[self.x, self.y, self.width, self.height, dp(10)], width=1.2)
        self.bind(pos=self._upd, size=self._upd, focus=self._on_focus)

    def _upd(self, *_):
        self._bg.pos   = self.pos
        self._bg.size  = self.size
        self._bord.rounded_rectangle = [self.x, self.y, self.width, self.height, dp(10)]

    def _on_focus(self, instance, focused):
        with self.canvas.before:
            if focused:
                Color(*ACCENT)
            else:
                Color(*BORDER)
            self._bord = Line(
                rounded_rectangle=[self.x, self.y, self.width, self.height, dp(10)],
                width=1.8 if focused else 1.2
            )


# ── Botão principal ───────────────────────────────────────────────────────────
class PrimaryButton(Button):
    def __init__(self, **kwargs):
        super().__init__(
            background_color=(0, 0, 0, 0),
            color=TEXT,
            font_size=dp(16),
            bold=True,
            size_hint_y=None,
            height=dp(52),
            **kwargs
        )
        with self.canvas.before:
            Color(*ACCENT)
            self._rect = RoundedRectangle(radius=[dp(12)], pos=self.pos, size=self.size)
        self.bind(pos=self._upd, size=self._upd,
                  on_press=self._press, on_release=self._release)

    def _upd(self, *_):
        self._rect.pos  = self.pos
        self._rect.size = self.size

    def _press(self, *_):
        anim = Animation(opacity=0.75, duration=0.08)
        anim.start(self)

    def _release(self, *_):
        anim = Animation(opacity=1.0, duration=0.12)
        anim.start(self)


# ── Chip de badge ─────────────────────────────────────────────────────────────
class Badge(Label):
    def __init__(self, **kwargs):
        super().__init__(
            font_size=dp(11),
            color=(*ACCENT[:3], 1),
            size_hint=(None, None),
            height=dp(24),
            padding=[dp(10), dp(4)],
            **kwargs
        )
        self.texture_update()
        self.width = self.texture_size[0] + dp(20)
        with self.canvas.before:
            Color(*ACCENT[:3], 0.15)
            self._bg   = RoundedRectangle(radius=[dp(12)], pos=self.pos, size=self.size)
            Color(*ACCENT[:3], 0.4)
            self._bord = Line(rounded_rectangle=[self.x, self.y, self.width, self.height, dp(12)], width=1)
        self.bind(pos=self._upd, size=self._upd)

    def _upd(self, *_):
        self._bg.pos  = self.pos
        self._bg.size = self.size
        self._bord.rounded_rectangle = [self.x, self.y, self.width, self.height, dp(12)]


# ── Linha de resultado ────────────────────────────────────────────────────────
class ResultRow(BoxLayout):
    def __init__(self, label, value, accent=False, **kwargs):
        super().__init__(orientation='horizontal', size_hint_y=None,
                         height=dp(44), **kwargs)
        color = ACCENT2 if accent else TEXT
        lbl = Label(text=label, color=(*MUTED[:3], 1), font_size=dp(13),
                    halign='left', valign='middle')
        lbl.bind(size=lambda w, s: setattr(w, 'text_size', s))
        val = Label(text=value, color=color, font_size=dp(15), bold=True,
                    halign='right', valign='middle')
        val.bind(size=lambda w, s: setattr(w, 'text_size', s))
        self.add_widget(lbl)
        self.add_widget(val)


# ── App principal ─────────────────────────────────────────────────────────────
CAMPOS = [
    ("a",  "Lado  a",              "m",      "Ex: 4.0"),
    ("b",  "Lado  b",              "m",      "Ex: 6.0"),
    ("h",  "Espessura  h",         "m",      "Ex: 0.12"),
    ("p",  "Carga distribuída  p", "kN/m²",  "Ex: 5.0"),
    ("e",  "Módulo de elasticidade E", "kN/m²", "Ex: 20000"),
    ("v",  "Coef. de Poisson  ν",  "—",      "Ex: 0.2"),
]

class SlideApp(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.etapa  = 0
        self.valores = {}

        # fundo animado
        self._bg = AnimatedBackground(size_hint=(1, 1), pos_hint={'x': 0, 'y': 0})
        self.add_widget(self._bg)

        # cartão central
        self._card = Card(
            size_hint=(None, None),
            width=dp(360),
            height=dp(440),
            pos_hint={'center_x': .5, 'center_y': .52},
        )
        self.add_widget(self._card)
        self._build_form()

    # ── Montar formulário ──────────────────────────────────────────────────
    def _build_form(self):
        self._card.clear_widgets()
        key, nome, unidade, hint = CAMPOS[self.etapa]

        # cabeçalho
        header = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(32))
        title = Label(text="CÁLCULO DE LAJES", color=(*MUTED[:3], 1),
                      font_size=dp(11), bold=True, halign='left', valign='middle')
        title.bind(size=lambda w, s: setattr(w, 'text_size', s))
        badge = Badge(text=f"PASSO  {self.etapa+1} / {len(CAMPOS)}")
        header.add_widget(title)
        header.add_widget(badge)
        self._card.add_widget(header)

        # barra de progresso
        self._progress = MyProgressBar(
            total=len(CAMPOS),
            current=self.etapa,
            size_hint_y=None,
            height=dp(4)
        )
        self._card.add_widget(self._progress)
        self._card.add_widget(Widget(size_hint_y=None, height=dp(6)))

        # nome do campo
        lbl_field = Label(
            text=nome,
            color=TEXT,
            font_size=dp(22),
            bold=True,
            size_hint_y=None,
            height=dp(34),
            halign='left',
            valign='middle',
        )
        lbl_field.bind(size=lambda w, s: setattr(w, 'text_size', s))
        self._card.add_widget(lbl_field)

        # unidade
        lbl_unit = Label(
            text=f"Unidade: {unidade}",
            color=(*MUTED[:3], 1),
            font_size=dp(12),
            size_hint_y=None,
            height=dp(20),
            halign='left',
            valign='middle',
        )
        lbl_unit.bind(size=lambda w, s: setattr(w, 'text_size', s))
        self._card.add_widget(lbl_unit)

        self._card.add_widget(Widget(size_hint_y=None, height=dp(4)))

        # input
        self._input = StyledInput(hint_text=hint)
        self._card.add_widget(self._input)

        # mensagem de erro (oculta)
        self._err = Label(
            text="",
            color=(1, 0.35, 0.35, 1),
            font_size=dp(12),
            size_hint_y=None,
            height=dp(18),
        )
        self._card.add_widget(self._err)

        self._card.add_widget(Widget())   # spacer

        # botão
        lbl_btn = "CALCULAR" if self.etapa == len(CAMPOS)-1 else "PRÓXIMO  →"
        self._btn = PrimaryButton(text=lbl_btn)
        self._btn.bind(on_press=self._proximo)
        self._card.add_widget(self._btn)

        # animar entrada
        self._card.opacity = 0
        anim = Animation(opacity=1, duration=0.25)
        anim.start(self._card)
        self._input.focus = True

    # ── Avançar etapa ──────────────────────────────────────────────────────
    def _proximo(self, *_):
        try:
            valor = float(self._input.text.replace(',', '.'))
            if valor <= 0 and self.etapa < 4:
                raise ValueError("não positivo")
        except Exception:
            self._err.text = "⚠  Digite um número válido e positivo."
            return

        key = CAMPOS[self.etapa][0]
        self.valores[key] = valor
        self.etapa += 1

        if self.etapa < len(CAMPOS):
            self._build_form()
        else:
            self._calcular()

    # ── Cálculo ────────────────────────────────────────────────────────────
    def _calcular(self):
        a = self.valores['a']
        b = self.valores['b']
        h = self.valores['h']
        p = self.valores['p']
        e = self.valores['e']
        v = self.valores['v']

        x = a / 2
        y = b / 2
        D = (e * (h**3)) / (12 * (1 - v**2))
        N = 15
        w = Mx = My = Mxy = 0

        for m in range(1, N+1, 2):
            for n in range(1, N+1, 2):
                termo  = (m/a)**2 + (n/b)**2
                seno   = np.sin(m*np.pi*x/a) * np.sin(n*np.pi*y/b)
                cosseno= np.cos(m*np.pi*x/a) * np.cos(n*np.pi*y/b)
                w  += (16*p)/(D*np.pi**6) * (seno/(m*n*termo**2))
                My += (16*p)/(np.pi**4) * (((m/a)**2 + v*(n/b)**2)/(m*n*termo**2)) * seno
                Mx += (16*p)/(np.pi**4) * ((v*(m/a)**2 + (n/b)**2)/(m*n*termo**2)) * seno
                Mxy+= -(16*(1-v)*p)/(np.pi**4*a*b) * (cosseno/termo**2)

        self._show_results(w, Mx, My, Mxy, D)

    # ── Tela de resultados ─────────────────────────────────────────────────
    def _show_results(self, w, Mx, My, Mxy, D):
        self._card.clear_widgets()
        self._card.height = dp(520)

        # título
        t = Label(text="RESULTADOS", color=(*ACCENT[:3], 1),
                  font_size=dp(12), bold=True, size_hint_y=None, height=dp(28),
                  halign='left', valign='middle')
        t.bind(size=lambda w_, s: setattr(w_, 'text_size', s))
        self._card.add_widget(t)
        self._card.add_widget(Divider())
        self._card.add_widget(Widget(size_hint_y=None, height=dp(4)))

        # flecha (destaque)
        flecha_box = BoxLayout(orientation='vertical', size_hint_y=None, height=dp(70))
        lbl_f = Label(text="Flecha máxima", color=(*MUTED[:3], 1),
                      font_size=dp(12), size_hint_y=None, height=dp(22),
                      halign='left', valign='middle')
        lbl_f.bind(size=lambda w_, s: setattr(w_, 'text_size', s))
        val_f = Label(text=f"{w:.4e} m", color=(*ACCENT2[:3], 1),
                      font_size=dp(26), bold=True, size_hint_y=None, height=dp(38),
                      halign='left', valign='middle')
        val_f.bind(size=lambda w_, s: setattr(w_, 'text_size', s))
        flecha_box.add_widget(lbl_f)
        flecha_box.add_widget(val_f)
        self._card.add_widget(flecha_box)

        self._card.add_widget(Divider())
        self._card.add_widget(Widget(size_hint_y=None, height=dp(2)))

        # momentos
        for label, value in [
            ("Momento Mx   (kN·m/m)", f"{Mx:.4f}"),
            ("Momento My   (kN·m/m)", f"{My:.4f}"),
            ("Momento Mxy  (kN·m/m)", f"{Mxy:.4f}"),
            ("Rigidez D    (kN·m)",   f"{D:.2e}"),
        ]:
            self._card.add_widget(ResultRow(label, value))
            self._card.add_widget(Divider())

        self._card.add_widget(Widget())

        # botão reiniciar
        btn_r = PrimaryButton(text="↺  NOVO CÁLCULO")
        btn_r.bind(on_press=self._reiniciar)
        self._card.add_widget(btn_r)

        anim = Animation(opacity=0) + Animation(opacity=1, duration=0.3)
        anim.start(self._card)

    # ── Reiniciar ──────────────────────────────────────────────────────────
    def _reiniciar(self, *_):
        self.etapa   = 0
        self.valores = {}
        self._card.height = dp(440)
        self._build_form()


class CalculoLajesApp(App):
    def build(self):
        self.title = "Cálculo de Lajes"
        Window.size = (400, 700)
        return SlideApp()


if __name__ == '__main__':
    CalculoLajesApp().run()