import time

def timer(minutes, message):
    total_seconds = minutes * 60
    while total_seconds:
        mins, secs = divmod(total_seconds, 60)
        timer_display = f'{mins:02d}:{secs:02d}'
        print(f'\r{message}: {timer_display}', end='')
        time.sleep(1)
        total_seconds -= 1
    print(f'\n{message} terminou!')

def focus_cycle():
    print("Bem-vindo ao método (10+2)*5 para vencer a procrastinação!\n")
    
    for cycle in range(1, 6):
        print(f"\n[Ciclo {cycle}/5] Hora de trabalhar por 10 minutos!")
        timer(10, "Foco total")
        
        if cycle < 5:
            print("\nPausa de 2 minutos. Respira fundo e relaxa um pouco!")
            timer(2, "Pausa")
    
    print("\nParabéns! Completaste os 5 ciclos. Trabalho bem feito! 🎉")

if __name__ == "__main__":
    focus_cycle()
