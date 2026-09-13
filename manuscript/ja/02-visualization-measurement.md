# 2. 測定、基底、可視化

[← 量子状態と演算](01-quantum-operations.md) | [次: 回路の構築 →](03-circuit-construction.md)

<a id="measurement-basis"></a>
## 測定と基底

computational（Z）basis測定では$\alpha|0\rangle+\beta|1\rangle$から、0を確率$|\alpha|^2$、1を確率$|\beta|^2$で得て、状態は対応するbasis stateへ射影されます。X basisを測りたいときは測定前に$H$を置き、Y basisなら典型的には$S^\dagger$の後に$H$を置いてZ測定へ変換します。「状態の振幅」と「有限shotsから得たcounts」を区別してください。

Bell state $(|00\rangle+|11\rangle)/\sqrt{2}$の理想Z-basis分布は`00`と`11`が各$1/2$です。$H|-\rangle=|1\rangle$なので、その後のZ測定は1が確定します。

```python
from qiskit import QuantumCircuit

bell = QuantumCircuit(2)
bell.h(0); bell.cx(0, 1)
```

<a id="statevector"></a>
## Statevectorで確かめる

測定を含まないunitary circuitなら次で初期$|0\cdots0\rangle$からの状態を得ます。

```python
import numpy as np
from qiskit.quantum_info import Statevector

psi = Statevector.from_instruction(bell)
assert np.allclose(psi.probabilities(), [0.5, 0.0, 0.0, 0.5])
```

測定は非unitaryで確率的なので、測定入り回路を同じ発想で単一statevectorへ畳み込まないでください。

<a id="bitstrings-counts"></a>
## bitstringとcounts

通常のresult stringはclassical bitの高indexを左、bit 0を右に表示します。`"10"`の右端はc0です。ただしmeasurement mappingが`q0→c1`なら右端がq0とは限りません。複数classical registerでは空白で区切られる場合があり、register構成とmappingを先に確認します。

countsはshotsの度数です。`{'0':760,'1':240}`、1000 shotsなら経験確率$\hat{p}(1)=0.24$。理論確率ではなく標本推定です。

<a id="circuit-drawing"></a>
## 回路を描く

```python
from qiskit.visualization import circuit_drawer

text = bell.draw("text")
# Matplotlibのoptional dependenciesがある環境:
figure = bell.draw("mpl")
```

`draw("mpl")`はMatplotlib回路drawerを選びます。`reverse_bits=True`は表示順を変えるだけでcircuitのbit identityや操作を変えません。

<a id="measurement-plots"></a>
## 測定分布を描く

```python
from qiskit.visualization import plot_histogram, plot_distribution

counts = {"00": 500, "11": 524}
plot_histogram(counts)       # countsの比較
plot_distribution(counts)   # 正規化した分布
```

state plotへcounts辞書を渡す、回路drawerでcountsを描こうとする、という型の取り違えを避けます。

<a id="state-plots"></a>
## 状態を描く

`plot_state_qsphere(psi)`はbasis成分の大きさ（確率）とphaseを表現します。`plot_bloch_multivector(psi)`は各qubitのreduced stateをBloch sphereで表示します。もつれたBell stateでは各単独qubitのBloch vectorが中心に来ますが、全体が「情報のない状態」なのではなく相関が残っています。`plot_state_city`はdensity matrix要素の実部・虚部を棒で示します。

```python
from qiskit.visualization import plot_state_qsphere, plot_bloch_multivector

plot_state_qsphere(psi)
plot_bloch_multivector(psi)
```

## 試験での判断手順

1. 入力はcircuit、state、countsのどれか。
2. 見たいのは配線、標本分布、振幅/phase、各qubitのBloch vectorのどれか。
3. bit orderとmeasurement mappingを分けて読む。

## 章末チェック

1. Bell stateをBloch sphereだけ見て積状態と判定できますか。
2. `"101"`の右端は通常どのclassical bitですか。

答え: 1. できません。qubit間相関も必要です。2. c0。

[← 量子状態と演算](01-quantum-operations.md) | [次: 回路の構築 →](03-circuit-construction.md)
