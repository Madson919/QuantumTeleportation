from qiskit import QuantumCircuit
from qiskit import execute
from qiskit.providers.ibmq import least_busy
from qiskit import QuantumRegister, ClassicalRegister
from math import pi
from qiskit import IBMQ
from qiskit.visualization import plot_histogram, circuit_drawer

# Создание квантовых регистров
alice_reg = QuantumRegister(2, name="alice")
bob_reg = QuantumRegister(1, name="bob")
qc = QuantumCircuit(alice_reg, bob_reg)

# Применение операций на квантовых регистрах
qc.h(alice_reg[1])  # Применение вентиля Адамара (H-вентиль) на втором кубите Алисы
qc.cx(alice_reg[1], bob_reg[0])  # Применение CX-вентиля между вторым кубитом Алисы и кубитом Боба

# Создание классического регистра для измерения
bob_class_reg = ClassicalRegister(1)
qc.add_register(bob_class_reg)

qc.barrier()
qc.rx(pi/4, alice_reg[0])  # Применение вращения по оси X на первом кубите Алисы

qc.barrier()
qc.cx(alice_reg[0], alice_reg[1])  # Применение CX-вентиля между первым и вторым кубитами Алисы
qc.h(alice_reg[0])  # Применение вентиля Адамара (H-вентиль) на первом кубите Алисы
qc.barrier()

qc.cx(alice_reg[1], bob_reg[0])  # Применение CX-вентиля между вторым кубитом Алисы и кубитом Боба
qc.cz(alice_reg[0], bob_reg[0])  # Применение CZ-вентиля между первым кубитом Алисы и кубитом Боба
qc.barrier()
qc.rx(-pi/4, bob_reg[0])  # Применение вращения по оси X на кубите Боба
qc.measure(bob_reg[0], bob_class_reg)  # Измерение кубита Боба и запись результата в классический регистр

# Подключение к аккаунту IBM Quantum
IBMQ.load_account()
provider = IBMQ.get_provider(hub='ibm-q')

# Выбор наименее загруженного доступного бэкэнда
backend = least_busy(provider.backends(simulator=False))
print(backend)

# Выполнение эксперимента на выбранном бэкэнде
job_exp = execute(qc, backend=backend, shots=1024)
exp_result = job_exp.result()
exp_counts = exp_result.get_counts()

exp_measurement_result = exp_result.get_counts(qc)
print(exp_measurement_result)

total_qubits = sum(exp_measurement_result.values())  # Общее количество переданных бит
total_time = job_exp.result().time_taken  # Время выполнения эксперимента в секундах
print("Время выполнения:", total_time, "с")
print("Количество кубитов:", total_qubits)

bit_rate = total_qubits / total_time  # Расчет битрейта (кубит/сек)
print("Битрейт (в кубитах в секунду):", bit_rate)

error_rate = (exp_counts['1'] * 100) / total_qubits  # Расчет экспериментальной частоты ошибок
print("Экспериментальная частота ошибок:", error_rate, "%")

plot_histogram(exp_measurement_result)  # Построение гистограммы результатов измерений
circuit_drawer(qc, output='mpl', filename='circuit.png')  # Визуализация схемы квантовой схемы
