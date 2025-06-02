from hub import light_matrix, motion_sensor, port
import force_sensor
import color
import color_sensor
import motor
import runloop
import time

sensorEsqNaLinha = False;
sensorDirNalinha = False;

contador = 0

PORTA_SENSOR_ESQ = port.A
PORTA_SENSOR_DIR = port.B
PORTA_SENSOR_CRUZAMENTO = port.E

TEMPO_ENTRE_CRUZ = 1000

PORTA_MOTOR_ESQ = port.C
PORTA_MOTOR_DIR = port.D

NUM_CRUZ = 4

TEMPO_PARAR = 1000

LIMIAR = 50

VELOCIDADE = 400
VELOCIDADE_CURVA = VELOCIDADE

TICTAC_TIME = 400

estavaParaFrente = False
velocidadeFrente = VELOCIDADE

#motor direita = D
#motor esquerda = C invertido


def frente(velocidade):
    motor.run(PORTA_MOTOR_DIR, velocidade)
    motor.run(PORTA_MOTOR_ESQ, -velocidade)

# def ligarMotorGrande():
#    motor.run(PORTA_MOTOR_GRANDE, 1000)

def tras(velocidade):
    motor.run(PORTA_MOTOR_DIR, -velocidade)
    motor.run(PORTA_MOTOR_ESQ, velocidade)

def giroDireita(velocidade):
    motor.run(PORTA_MOTOR_DIR, -velocidade)
    motor.run(PORTA_MOTOR_ESQ, -velocidade)

def giroEsquerda(velocidade):
    motor.run(PORTA_MOTOR_DIR, velocidade)
    motor.run(PORTA_MOTOR_ESQ, velocidade)

def curvaEsquerda(velocidade):
    motor.run(PORTA_MOTOR_DIR, velocidade)
    motor.run(PORTA_MOTOR_ESQ, 0)

def curvaDireita(velocidade):
    motor.run(PORTA_MOTOR_DIR, 0)
    motor.run(PORTA_MOTOR_ESQ, -velocidade)

def parar():
    # motor.run(PORTA_MOTOR_GRANDE, 0)
    motor.run(PORTA_MOTOR_DIR, 0)
    motor.run(PORTA_MOTOR_ESQ, 0)

def estouNaLinha(porta):
    if color_sensor.reflection(porta) < LIMIAR:
        return False
    return True

def atualizarSensores():
    global sensorEsqNaLinha
    global sensorDirNaLinha

    sensorEsqNaLinha = estouNaLinha(PORTA_SENSOR_ESQ)
    sensorDirNaLinha = estouNaLinha(PORTA_SENSOR_DIR)

def seguirLinha():
    global estavaParaFrente
    global velocidadeFrente
    global ultimaAtt
    if not sensorEsqNaLinha and not sensorDirNaLinha:
        frente(VELOCIDADE)
        # ligarMotorGrande()
        estavaParaFrente = True
    elif sensorEsqNaLinha and not sensorDirNaLinha:
        curvaEsquerda(VELOCIDADE)
        #ligarMotorGrande()
        estavaParaFrente = False
    elif not sensorEsqNaLinha and sensorDirNaLinha:
        curvaDireita(VELOCIDADE)
        #ligarMotorGrande()
        estavaParaFrente = False
    else:
        pass

    #incrementa a velocidade gradualmente
    agora = time.ticks_ms()

    if agora >= (ultimaAtt + TICTAC_TIME):
        ultimaAtt = agora
        if estavaParaFrente:
            velocidadeFrente+=50
            if velocidadeFrente > 1110:
                velocidadeFrente = 1110
        else:
            velocidadeFrente = VELOCIDADE

async def main():
    global ultimaAtt
    global contador
    ultimaAtt = time.ticks_ms()
    ultimaAttCruz = time.ticks_ms()
    cont_cruzamento = 0

    light_matrix.write(str(contador))

    while contador < NUM_CRUZ:
        atualizarSensores()
        seguirLinha()
        agora = time.ticks_ms()
        if estouNaLinha(port.E):
            cont_cruzamento += 1
            if cont_cruzamento > 3:
                if agora >(ultimaAttCruz + TEMPO_ENTRE_CRUZ):
                    contador += 1
                    light_matrix.write(str(contador))
                    ultimaAttCruz = agora
        else:
            cont_cruzamento = 0
    agora = time.ticks_ms()
    ultimaAtt = agora
    while agora < ultimaAtt + TEMPO_PARAR:
        agora = time.ticks_ms()
        frente(VELOCIDADE)

runloop.run(main())


