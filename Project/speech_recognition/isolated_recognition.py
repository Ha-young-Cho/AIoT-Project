import time
from Maix import GPIO, I2S
from fpioa_manager import fm
import image, lcd

lcd.init()
# user setting
sample_rate   = 16000
record_time   = 4  #s

fm.register(20,fm.fpioa.I2S0_IN_D0, force=True)
fm.register(18,fm.fpioa.I2S0_SCLK, force=True)
fm.register(19,fm.fpioa.I2S0_WS, force=True)

rx = I2S(I2S.DEVICE_0)
rx.channel_config(rx.CHANNEL_0, rx.RECEIVER, align_mode=I2S.STANDARD_MODE)
rx.set_sample_rate(sample_rate)
print(rx)

from speech_recognizer import isolated_word

sr = isolated_word(dmac=2, i2s=I2S.DEVICE_0, size=10, shift=0) # maix bit set shift=1
print(sr.size())
print(sr)

img = image.Image()

## threshold
sr.set_threshold(0, 0, 10000)

## record and get & set

while True:
  time.sleep_ms(100)
  if sr.Done == sr.record(0):
    data = sr.get(0)
    img.clear()
    img.draw_string(0,120,'Recorded',scale=3)
    lcd.display(img)
    time.sleep_ms(500)
    img.clear()
    break
  if sr.Speak == sr.state():
    img.clear()
    img.draw_string(0,120,'Speak A',scale=3)
    lcd.display(img)
    print('speak A')

#sr.set(1, data)

while True:
  time.sleep_ms(100)
  if sr.Done == sr.record(1):
    data = sr.get(1)
    img.clear()
    img.draw_string(0,120,'Recorded',scale=3)
    lcd.display(img)
    time.sleep_ms(500)
    img.clear()
    break
  if sr.Speak == sr.state():
    print('speak B')
    img.clear()
    img.draw_string(0,120,'Speak B',scale=3)
    lcd.display(img)

print('recognizer')
img.draw_string(0,120,'Start',scale=3)
lcd.display(img)
time.sleep_ms(300)
img.clear()
while True:
  time.sleep_ms(200)
  if sr.Done == sr.recognize():
    res = sr.result()
    print(res[0])
