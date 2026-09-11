"""Build the quantum operations drill notebook with nbformat."""

from pathlib import Path
from textwrap import dedent

import nbformat as nbf


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "notebooks" / "references" / "quantum_operations_drill.ipynb"


def md(text: str):
    return nbf.v4.new_markdown_cell(dedent(text).strip())


def code(text: str):
    return nbf.v4.new_code_cell(dedent(text).strip())


cells = [
    md(
        """
        # Quantum Operations Drill

        ## Goal

        量子演算を「見たことがある」状態から、符号とglobal phaseを含めて再現できる状態へ進めます。

        学習手順:

        1. 各節の問いを紙上で予想する。
        2. NumPyの行列積で厳密値を確認する。
        3. Qiskitの`Statevector`と`Operator`で再確認する。
        4. `assert`が通る理由を自分の言葉で説明する。

        対応資料: `../../references/qiskit-pocket-reference.md`

        このNotebookはlocal計算だけを行い、IBM Quantum accountやQPUを必要としません。
        """
    ),
    md(
        """
        ## Setup

        基準versionはQiskit 2.5.2です。表示されるversionが異なる場合でも数学部分は同じですが、API差分があれば基準versionで再実行してください。
        """
    ),
    code(
        """
        import numpy as np
        import qiskit

        from qiskit.circuit.library import HGate, RZGate, SGate, XGate, YGate, ZGate
        from qiskit.quantum_info import Operator, Pauli, SparsePauliOp, Statevector

        np.set_printoptions(precision=3, suppress=True)
        print("Qiskit version:", qiskit.__version__)
        """
    ),
    md(
        """
        ### Equality helpers

        `exact`は配列成分の完全な一致、`equiv`はglobal phaseまでの同値です。この二つを混同しないことが本Notebookの中心です。
        """
    ),
    code(
        """
        TOL = 1e-10


        def exact_equal(left, right, atol=TOL):
            return bool(np.allclose(np.asarray(left), np.asarray(right), atol=atol, rtol=0))


        def state_equiv(left, right):
            return bool(Statevector(left).equiv(Statevector(right)))


        def operator_equiv(left, right):
            return bool(Operator(left).equiv(Operator(right)))


        def real_if_close(value):
            return np.real_if_close(value, tol=1000).item()
        """
    ),
    md(
        """
        ## Step 1: states and matrices

        まず`|0>`、`|1>`、`|+>`、`|->`、`|+i>`、`|-i>`とPauli/Hadamard行列を定義します。
        """
    ),
    code(
        """
        sqrt2 = np.sqrt(2)

        ket0 = np.array([1, 0], dtype=complex)
        ket1 = np.array([0, 1], dtype=complex)
        plus = np.array([1, 1], dtype=complex) / sqrt2
        minus = np.array([1, -1], dtype=complex) / sqrt2
        plus_i = np.array([1, 1j], dtype=complex) / sqrt2
        minus_i = np.array([1, -1j], dtype=complex) / sqrt2

        I = np.eye(2, dtype=complex)
        X = np.array([[0, 1], [1, 0]], dtype=complex)
        Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
        Z = np.array([[1, 0], [0, -1]], dtype=complex)
        H = np.array([[1, 1], [1, -1]], dtype=complex) / sqrt2
        S = np.diag([1, 1j]).astype(complex)
        Sdg = np.diag([1, -1j]).astype(complex)

        named_states = {
            "|0>": ket0,
            "|1>": ket1,
            "|+>": plus,
            "|->": minus,
            "|+i>": plus_i,
            "|-i>": minus_i,
        }

        for name, state in named_states.items():
            assert np.isclose(np.vdot(state, state), 1)

        assert exact_equal(Operator(XGate()).data, X)
        assert exact_equal(Operator(YGate()).data, Y)
        assert exact_equal(Operator(ZGate()).data, Z)
        assert exact_equal(Operator(HGate()).data, H)
        assert exact_equal(Operator(SGate()).data, S)

        print("All six states are normalized.")
        print("Qiskit gate matrices match the explicit NumPy matrices.")
        """
    ),
    md(
        """
        ## Step 2: exact gate action

        予想してから実行してください。

        - `Y|0>`の係数は`+i`か`-i`か。
        - `Y|1>`の係数はどちらか。
        - `Z|+>`は厳密に`|->`か、余分なglobal phaseを持つか。
        """
    ),
    code(
        """
        exact_action_checks = [
            ("X|0>", X @ ket0, ket1),
            ("X|1>", X @ ket1, ket0),
            ("Y|0>", Y @ ket0, 1j * ket1),
            ("Y|1>", Y @ ket1, -1j * ket0),
            ("Z|+>", Z @ plus, minus),
            ("Z|->", Z @ minus, plus),
            ("H|0>", H @ ket0, plus),
            ("H|1>", H @ ket1, minus),
        ]

        for expression, actual, expected in exact_action_checks:
            passed = exact_equal(actual, expected)
            print(f"{expression:6s} exact: {passed}   vector={actual}")
            assert passed
        """
    ),
    md(
        """
        ### X/Y/Z eigenstates

        固有状態なら、作用結果は元の状態に固有値`+1`または`-1`を掛けたものです。
        """
    ),
    code(
        """
        eigen_checks = [
            ("X|+>", X @ plus, +1 * plus),
            ("X|->", X @ minus, -1 * minus),
            ("Y|+i>", Y @ plus_i, +1 * plus_i),
            ("Y|-i>", Y @ minus_i, -1 * minus_i),
            ("Z|0>", Z @ ket0, +1 * ket0),
            ("Z|1>", Z @ ket1, -1 * ket1),
        ]

        for expression, actual, expected in eigen_checks:
            assert exact_equal(actual, expected)
            print(f"{expression:7s} passed")
        """
    ),
    md(
        """
        ## Step 3: Pauli multiplication

        巡回順`X -> Y -> Z -> X`では`+i`、逆順では`-i`です。
        """
    ),
    code(
        """
        paulis = {"X": X, "Y": Y, "Z": Z}
        expected_products = {
            "XX": I,
            "YY": I,
            "ZZ": I,
            "XY": 1j * Z,
            "YZ": 1j * X,
            "ZX": 1j * Y,
            "YX": -1j * Z,
            "ZY": -1j * X,
            "XZ": -1j * Y,
        }

        for label, expected in expected_products.items():
            actual = paulis[label[0]] @ paulis[label[1]]
            assert exact_equal(actual, expected)

        assert exact_equal(X @ Z, -(Z @ X))
        print("XZ = -ZX:", exact_equal(X @ Z, -(Z @ X)))
        print("XZ = -iY:", exact_equal(X @ Z, -1j * Y))
        print("All nine Pauli products passed.")
        """
    ),
    md(
        """
        ## Step 4: conjugation by H and S

        共役変換`U P U^dagger`はbasis changeとして読むと覚えやすくなります。
        """
    ),
    code(
        """
        conjugation_checks = [
            ("H X H", H @ X @ H, Z),
            ("H Z H", H @ Z @ H, X),
            ("H Y H", H @ Y @ H, -Y),
            ("S X Sdg", S @ X @ Sdg, Y),
            ("S Y Sdg", S @ Y @ Sdg, -X),
            ("S Z Sdg", S @ Z @ Sdg, Z),
        ]

        for expression, actual, expected in conjugation_checks:
            passed = exact_equal(actual, expected)
            print(f"{expression:9s} exact: {passed}")
            assert passed
        """
    ),
    md(
        """
        ## Step 5: rotations and global phase

        `Rz(pi)`と`Z`はphysical actionとしては同じでも、厳密な行列は異なります。
        """
    ),
    code(
        """
        rz_pi = Operator(RZGate(np.pi)).data

        print("Rz(pi) == -iZ exactly:", exact_equal(rz_pi, -1j * Z))
        print("Rz(pi) == Z exactly:  ", exact_equal(rz_pi, Z))
        print("Rz(pi) ~  Z:          ", operator_equiv(rz_pi, Z))

        assert exact_equal(rz_pi, -1j * Z)
        assert not exact_equal(rz_pi, Z)
        assert operator_equiv(rz_pi, Z)

        rz_half_pi = Operator(RZGate(np.pi / 2)).data
        assert exact_equal(rz_half_pi, np.exp(-1j * np.pi / 4) * S)
        print("Rz(pi/2) = exp(-i*pi/4) S exactly.")
        """
    ),
    md(
        """
        ### State equality versus physical equivalence

        `|->`と`i|->`は配列として異なりますが、同じphysical pure stateです。
        """
    ),
    code(
        """
        print("|-> == i|-> exactly:", exact_equal(minus, 1j * minus))
        print("|-> ~  i|->:        ", state_equiv(minus, 1j * minus))

        assert not exact_equal(minus, 1j * minus)
        assert state_equiv(minus, 1j * minus)
        assert exact_equal(Z @ plus, minus)
        assert not exact_equal(Z @ plus, 1j * minus)
        """
    ),
    md(
        """
        ### Controlled operationでは位相を捨てない

        `Z`と`Rz(pi)`はglobal phaseまで同値ですが、controlled版は一般にglobal phaseだけの差ではありません。位相がcontrol分岐間のrelative phaseになるためです。
        """
    ),
    code(
        """
        controlled_z = Operator(ZGate().control()).data
        controlled_rz_pi = Operator(RZGate(np.pi).control()).data

        print("CZ ~ controlled-Rz(pi):", operator_equiv(controlled_z, controlled_rz_pi))
        assert not operator_equiv(controlled_z, controlled_rz_pi)
        """
    ),
    md(
        """
        ## Step 6: expectation values

        定義は`<psi|O|psi>`。固有状態なら期待値は固有値です。
        """
    ),
    code(
        """
        expectation_table = []
        for state_name, state in named_states.items():
            statevector = Statevector(state)
            values = [
                real_if_close(statevector.expectation_value(Operator(pauli)))
                for pauli in (X, Y, Z)
            ]
            expectation_table.append((state_name, *values))

        print("state    <X>   <Y>   <Z>")
        for row in expectation_table:
            print(f"{row[0]:5s} {row[1]:5.1f} {row[2]:5.1f} {row[3]:5.1f}")
        """
    ),
    md(
        """
        ### Two-qubit observable `XX`

        `|+>`はXの`+1`固有状態なので、`|++>`は`X tensor X`の`(+1)(+1)=+1`固有状態です。
        """
    ),
    code(
        """
        plus_plus = Statevector(np.kron(plus, plus))
        xx_expectation = real_if_close(plus_plus.expectation_value(Pauli("XX")))

        print("<++|XX|++> =", xx_expectation)
        assert np.isclose(xx_expectation, 1)
        """
    ),
    md(
        """
        ### Linear combinations with SparsePauliOp

        `SparsePauliOp.from_list([(\"ZI\", 0.5), (\"XX\", -1.0)])`は`0.5 ZI - XX`です。
        """
    ),
    code(
        """
        observable = SparsePauliOp.from_list([("ZI", 0.5), ("XX", -1.0)])
        phi_plus = Statevector([1 / sqrt2, 0, 0, 1 / sqrt2])
        value = real_if_close(phi_plus.expectation_value(observable))

        print("<Phi+| (0.5 ZI - XX) |Phi+> =", value)
        assert np.isclose(value, -1)
        """
    ),
    md(
        """
        ## Step 7: Qiskit ordering

        2-qubit labelは`|q1 q0>`。Pauli labelも右端がq0です。
        """
    ),
    code(
        """
        state_01 = Statevector.from_label("01").data
        xz = Pauli("XZ").to_matrix()

        print("|01> nonzero statevector index:", int(np.argmax(np.abs(state_01))))
        print('Pauli("XZ") == X on q1 tensor Z on q0:', exact_equal(xz, np.kron(X, Z)))
        print('XZ applied to |01>:', xz @ state_01)

        assert np.argmax(np.abs(state_01)) == 1
        assert exact_equal(xz, np.kron(X, Z))
        assert exact_equal(xz @ state_01, -Statevector.from_label("11").data)
        """
    ),
    md(
        """
        ## Checks: six rapid-fire questions

        出力を見る前に、それぞれを紙へ書いてください。

        1. `Y|0>`
        2. `<++|XX|++>`
        3. `XZ`と`ZX`の関係
        4. 厳密な`Z|+>`
        5. 厳密な`Rz(pi)`
        6. `HZH`
        """
    ),
    code(
        """
        answers = [
            "1. Y|0> = i|1>",
            "2. <++|XX|++> = +1",
            "3. XZ = -ZX  (XZ = -iY, ZX = iY)",
            "4. Z|+> = |->",
            "5. Rz(pi) = -iZ",
            "6. HZH = X",
        ]

        print("\\n".join(answers))
        """
    ),
    md(
        """
        ## Next Steps

        1. Kernelを再起動し、出力を見ずに上から実行する。
        2. 各`assert`の右辺を一度消し、自分で復元する。
        3. `X/Y/Z`、`|0>/|1>/|+>/|->/|+i>/|-i>`の組合せを追加する。
        4. `XX/YY/ZZ`と4つのBell状態の期待値表を再生成する。
        5. pocket referenceを閉じ、6問を60秒以内で答える。
        """
    ),
    code(
        """
        # Final consistency checks
        assert exact_equal(Y @ ket0, 1j * ket1)
        assert np.isclose(plus_plus.expectation_value(Pauli("XX")), 1)
        assert exact_equal(X @ Z, -(Z @ X))
        assert exact_equal(Z @ plus, minus)
        assert exact_equal(Operator(RZGate(np.pi)).data, -1j * Z)
        assert exact_equal(H @ Z @ H, X)

        print("All quantum-operations checks passed.")
        """
    ),
]


notebook = nbf.v4.new_notebook(
    cells=cells,
    metadata={
        "kernelspec": {
            "display_name": "Python 3 (ipykernel)",
            "language": "python",
            "name": "python3",
        },
        "language_info": {
            "name": "python",
            "version": "3",
            "mimetype": "text/x-python",
            "codemirror_mode": {"name": "ipython", "version": 3},
            "pygments_lexer": "ipython3",
            "nbconvert_exporter": "python",
            "file_extension": ".py",
        },
    },
)

OUTPUT.parent.mkdir(parents=True, exist_ok=True)
nbf.write(notebook, OUTPUT)
print(f"Created {OUTPUT}")
