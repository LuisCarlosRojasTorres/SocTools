import board
import busio
import digitalio
from PIL import Image, ImageDraw, ImageFont
import adafruit_pcd8544

# 1. Configuração dos pinos GPIO
dc_pin = digitalio.DigitalInOut(board.D24)    # Data/Command
cs_pin = digitalio.DigitalInOut(board.D8)     # Chip Select
reset_pin = digitalio.DigitalInOut(board.D25) # Reset

# 2. Inicialização do barramento SPI e do Display (84x48 pixels)
spi = busio.SPI(board.SCLK, MOSI=board.MOSI)
display = adafruit_pcd8544.PCD8544(spi, dc_pin, cs_pin, reset_pin)

# Ajuste de contraste se a tela ficar fraca ou toda preta (30 a 60 costuma funcionar)
display.bias = 4
display.contrast = 45

# 3. Criar uma imagem em branco (1-bit / monocromática)
image = Image.new("1", (display.width, display.height))
draw = ImageDraw.Draw(image)

# Desenhar um retângulo na borda da tela
draw.rectangle((0, 0, display.width - 1, display.height - 1), outline=255, fill=0)

# Carregar fonte padrão
font = ImageFont.load_default()

# Ecrever textos no buffer de imagem
draw.text((8, 8), "Raspberry Pi", font=font, fill=255)
draw.text((12, 22), "Nokia 5110", font=font, fill=255)
draw.text((18, 34), "Python3", font=font, fill=255)

# 4. Enviar a imagem para a tela
display.image(image)
display.show()