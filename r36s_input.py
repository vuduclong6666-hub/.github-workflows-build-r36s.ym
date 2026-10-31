#!/usr/bin/env python3
import evdev
from evdev import UInput, ecodes as e
import sys

def main():
    # Tự động quét và tìm thiết bị gamepad trên R36S
    devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
    gamepad = None
    for dev in devices:
        if "gamepad" in dev.name.lower() or "rk" in dev.name.lower() or "joy" in dev.name.lower():
            gamepad = dev
            break
            
    if not gamepad:
        try:
            gamepad = evdev.InputDevice('/dev/input/event0')
        except Exception:
            sys.exit(1)

    # Khởi tạo thiết bị đầu ra ảo (Virtual Mouse & Keyboard)
    cap = {
        e.EV_REL: [e.REL_X, e.REL_Y, e.REL_WHEEL],
        e.EV_KEY: [
            e.BTN_LEFT, e.BTN_RIGHT,
            e.KEY_ENTER, e.KEY_BACKSPACE, e.KEY_ESC, e.KEY_TAB
        ]
    }
    ui = UInput(cap, name="r36s-virtual-input")

    # Vòng lặp đọc sự kiện nút bấm và cần analog
    for event in gamepad.read_loop():
        if event.type == e.EV_ABS:
            if event.code == e.ABS_X:
                val = int((event.value - 128) / 8)
                if abs(val) > 2:
                    ui.write(e.EV_REL, e.REL_X, val)
            elif event.code == e.ABS_Y:
                val = int((event.value - 128) / 8)
                if abs(val) > 2:
                    ui.write(e.EV_REL, e.REL_Y, val)
                    
        elif event.type == e.EV_KEY:
            if event.code == e.BTN_EAST:      # Nút A -> Chuột trái
                ui.write(e.EV_KEY, e.BTN_LEFT, event.value)
            elif event.code == e.BTN_SOUTH:   # Nút B -> Chuột phải
                ui.write(e.EV_KEY, e.BTN_RIGHT, event.value)
            elif event.code == e.BTN_NORTH:   # Nút X -> Phím Enter
                ui.write(e.EV_KEY, e.KEY_ENTER, event.value)
            elif event.code == e.BTN_WEST:    # Nút Y -> Phím Backspace
                ui.write(e.EV_KEY, e.KEY_BACKSPACE, event.value)
            elif event.code == e.BTN_TL:      # Nút L1 -> Phím ESC
                ui.write(e.EV_KEY, e.KEY_ESC, event.value)
                
        ui.syn()

if __name__ == "__main__":
    main()
  
